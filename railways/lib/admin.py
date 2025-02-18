import hashlib
import os
import secrets
import string
import time

from railways.models import AdminAPIKeys, Train
from django.conf import settings
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

# We generate the API Keys for authorities using
# the current timestamp.
def generate_new_key(initial=False):
    if not initial:
        timestamp = str(int(time.time()))
        AUTH_TOKEN = timestamp[-settings.ADMIN_API_KEY_LENGTH:]
    else:
        API_KEY = os.getenv("INITIAL_API_KEY")

    HASHED_KEY = hash_api_key(API_KEY)
    API, created = AdminAPIKeys.objects.get_or_create(hashed_key=HASHED_KEY)
    
    return API_KEY


def hash_api_key(API_KEY):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(API_KEY.encode('utf-8'))
    return sha256_hash.hexdigest()


def check_if_key_exists(API_KEY):
    key_hash = hash_api_key(API_KEY)
    api_key_exists = AdminAPIKeys.objects.filter(hashed_key=key_hash).exists()

    return api_key_exists


def maybe_add_train_data(source, destination, seats, API_KEY):
    # We assume the path is one way in this project.
    if source < 0 or destination < 0 or destination <= source:
        return JsonResponse(
            {"error": "Invalid path"}, status=400
        )
    
    if seats <= 0:
        return JsonResponse(
            {"error": "At least one seat must be picked!"}, status=400
        )

    is_api__key_valid = check_if_key_exists(API_KEY)

    if not is_api__key_valid:
        return JsonResponse(
            {"error": "Invalid API Key"}, status=400
        )
    
    Train.objects.create(source=source, destination=destination, seats=seats)
    return JsonResponse(
        {"success": f"Train successfully added"}
    )

