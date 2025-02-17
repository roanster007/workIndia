import hashlib
import os
import secrets
import string

from railways.models import AdminAPIKeys
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

def generate_new_key(initial=False):
    characters = string.ascii_letters + string.digits

    if not initial:
        API_KEY = ''.join(secrets.choice(characters) for _ in range(ADMIN_API_KEY_LENGTH))
    else:
        API_KEY = os.getenv("INITIAL_API_KEY")

    HASHED_KEY = hash_api_key(API_KEY)
    API, created = AdminAPIKeys.objects.get_or_create(hashed_key=HASHED_KEY)

    if not created:
        generate_new_key()
    
    return API_KEY


def hash_api_key(API_KEY):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(API_KEY.encode('utf-8'))
    return sha256_hash.hexdigest()


def check_if_key_exists(API_KEY):
    key_hash = hash_api_key(API_KEY)
    api_key_exists = AdminAPIKeys.objects.filter(hashed_key=key_hash).exists()

    return api_key_exists
