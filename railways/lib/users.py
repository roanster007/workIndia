import re
import secrets
import string
import hashlib

from railways.models import User, Bookings, Train
from django.db import transaction
from django.db.models import Sum, F, Q
from django.http import JsonResponse
from django.utils.timezone import now as timezone_now

def maybe_register_user(email, password):
    if not is_valid_email(email):
        return JsonResponse(
            {"error": "Invalid email!"}, status=400
        )
    
    user, created = User.objects.get_or_create(email=email, password=password)

    if not created:
        return JsonResponse(
            {"error": "User already exists, please login!"}, status=400
        )
    
    return JsonResponse({"success": "Successfully registered! Please login to get auth token!"})


def login_user(email, password):
    if not is_valid_email(email):
        return JsonResponse(
            {"error": "Invalid email!"}, status=400
        )
    
    user = User.objects.filter(email=email, password=password).first()

    if user is not None:
        AUTH_TOKEN = generate_auth_token(user)
        return JsonResponse({"success": f"Successful Login! Auth Token - {AUTH_TOKEN}"})
    
    return JsonResponse(
        {"error": "User doesn't exist, Please login!"}, status=400
    )

# RI==TODO: Update this to a timestamp.
def generate_auth_token(user):
    characters = string.ascii_letters + string.digits
    AUTH_TOKEN = ''.join(secrets.choice(characters) for _ in range(ADMIN_API_KEY_LENGTH))
    
    sha256_hash = hashlib.sha256()
    sha256_hash.update(AUTH_TOKEN.encode('utf-8'))
    user.auth_token = AUTH_TOKEN
    user.token_issued = timezone_now()

    user.save(["auth_token", "token_issued"])
    return AUTH_TOKEN


def is_valid_email(email):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(EMAIL_REGEX, email) is not None


def maybe_get_booking_details(auth_token, bookind_id):
    user = User.objects.filter(auth_token=auth_token).first()

    if user is None:
        return JsonResponse(
            {"error": "Invalid Auth token!"}, status=400
        )
    
    booking = Bookings.objects.filter(id=booking_id, user=user).first()

    if booking is None:
        return JsonResponse(
            {"error": "No booking exists with the given credentials"}, status=400
        )
    
    booking_info = booking.to_dict()

    return JsonResponse(booking_info)


# TODO: Offload the tasks to a celery worker so that
# the job becomes asynchronous.
def maybe_process_booking(
    auth_token,
    train_id,
    source,
    destination,
    seats
):
    user = User.objects.filter(auth_token=auth_token).first()

    if user is None:
        return JsonResponse(
            {"error": "Invalid Auth token!"}, status=400
        )
    
    available_seats = Train.objects.filter(id=train_id).select_related("seats").first()

    if available_seats is None:
        return JsonResponse(
            {"error": "Train ID does not exist!"}, status=400
        )
    
    # We first aggregate all the booked seats between point A
    # and B such that the source or destination is between point
    # A and B.
    #
    # This allows us to estimate available seats for entirity of
    # the journey.
    booked_seats = Bookings.objects.filter(
        Q(source__gte=source, source__lte=destination) |
        Q(destination__gte=source, destination__lte=destination)
    ).aggregate(
        booked = Sum("seats")
    )

    if available_seats - booked_seats < seats:
        return JsonResponse(
            {"error": "Insufficient seats"}, status=400
        )
    
    # We want the transaction to be atomic -- if one step fails,
    # entire transaction fails.
    with transaction.atomic():
        # We lock rows to prevent races
        train = Train.objects.select_for_update().get(id=train_id)

            booking = Bookings.objects.create(
            user=user,
            train_id=train_id,
            source=source,
            destination=destination,
            seats=seats,
        )
    
    return JsonResponse(booking.to_dict())