import re
import secrets
import string
import hashlib

from railways.models import User, Bookings
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
