import re
import secrets
import string
import hashlib
import time

from django.conf import settings
from django.db import transaction
from django.db.models import Sum, F, Q
from django.http import JsonResponse
from django.utils.timezone import now as timezone_now
from railways.models import User, Bookings, Train
from railways.tasks.celery import process_booking_information
from railways.lib.train_manager import TrainManager


def maybe_register_user(email, password):
    if not is_valid_email(email):
        return JsonResponse({"error": "Invalid email!"}, status=400)

    user, created = User.objects.get_or_create(email=email, password=password)

    if not created:
        return JsonResponse(
            {"error": "User already exists, please register!"}, status=400
        )

    return JsonResponse(
        {"success": "Successfully registered! Please login to get auth token!"}
    )


def login_user(email, password):
    if not is_valid_email(email):
        return JsonResponse({"error": "Invalid email!"}, status=400)

    user = User.objects.filter(email=email, password=password).first()

    if user is not None:
        AUTH_TOKEN = generate_user_auth_token(user)
        return JsonResponse({"success": f"Successful Login! Auth Token - {AUTH_TOKEN}"})

    return JsonResponse({"error": "User doesn't exist, Please login!"}, status=400)


# We are using the current timestamp to generate auth
# tokens.
def generate_user_auth_token(user):
    timestamp = str(int(time.time()))
    AUTH_TOKEN = timestamp[-settings.USER_AUTH_KEY_LENGTH :]

    sha256_hash = hashlib.sha256()
    sha256_hash.update(AUTH_TOKEN.encode("utf-8"))
    user.auth_token = AUTH_TOKEN
    user.token_issued = timezone_now()

    user.save(update_fields=["auth_token", "token_issued"])
    return AUTH_TOKEN


def is_valid_email(email):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(EMAIL_REGEX, email) is not None


def maybe_get_booking_details(auth_token, booking_id):
    user = User.objects.filter(auth_token=auth_token).first()

    if user is None:
        return JsonResponse({"error": "Invalid Auth token!"}, status=400)

    booking = Bookings.objects.filter(id=booking_id, user=user).first()

    if booking is None:
        return JsonResponse(
            {"error": "No booking exists with the given credentials"}, status=400
        )

    booking_info = booking.to_dict()

    return JsonResponse(booking_info)


# We offload the load on server by validating each booking
# and adding it to the BOOKING_PROCESSING_QUEUE, where the
# Booking is finally processed asynchronously by celery workers
# and updated.
#
# Users are returned with Bookings object, from which they
# can check status of their booking.
def maybe_process_booking(auth_token, train_id, source, destination, seats):
    # We assume the path is one way in this project.
    if source < 0 or destination < 0 or destination <= source:
        return JsonResponse({"error": "Invalid path"}, status=400)

    if seats <= 0:
        return JsonResponse({"error": "At least one seat must be picked!"}, status=400)

    user = User.objects.filter(auth_token=auth_token).first()

    # if user is None:
    #     return JsonResponse({"error": "Invalid Auth token!"}, status=400)
    

    train_manager = TrainManager()
    num_seats_available = train_manager.trains.get(train_id, 0)

    if seats > num_seats_available:
        return JsonResponse({"error": "Insufficient seats available in train!"}, status=400)

    # After we verify all the details, we create a Bookings
    # row which contains the status of the booking, which
    # users can use to check status of booking.
    booking = Bookings.objects.create(
        user=user,
        train_id=train_id,
        source=source,
        destination=destination,
        seats=seats,
        status=Bookings.PENDING,
    )

    process_booking_information.apply_async(
        args=[booking.to_dict()], queue=settings.BOOKING_PROCESSING_QUEUE
    )

    return JsonResponse(
        {
            "success": f"Your booking id {booking.id} is in process. Please check the status after some time using the id."
        }
    )


def maybe_get_available_seats(source, destination):
    # We assume the path is one way in this project.
    if source < 0 or destination < 0 or destination <= source:
        return JsonResponse({"error": "Invalid path"}, status=400)
    
    available_trains = []
    train_manager = TrainManager()

    for train_id, seg_tree in train_manager.trains.items():
        num_seats_available = seg_tree.query(0, source, destination)

        if num_seats_available > 0:
            available_trains.append({"train_id": f"{train_id}", "seats": f"{num_seats_available}"})
    
    return JsonResponse({"trains": available_trains})
