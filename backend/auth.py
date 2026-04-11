import secrets
import hashlib
from db import SessionLocal
from models import APIKey
from datetime import datetime

def generate_api_key():
    return "sk" + secrets.token_hex(16)

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

def create_api_key(user_id:int):
    db = SessionLocal()
    try:
        raw_key = generate_api_key() # generate a random API key
        hashed = hash_api_key(raw_key) # hash it for secure storage

        new_key = APIKey(
            user_id=user_id,
            key_hash = hashed,
            created_at = datetime.utcnow(),
            last_reset_date = datetime.utcnow()
        )
        db.add(new_key)
        db.commit()

        return raw_key # return the raw key to the user
    finally:
        db.close()

def get_user_from_api_key(api_key: str):
    db = SessionLocal()

    try:
        hashed = hash_api_key(api_key)
        # hash incoming key

        key = db.query(APIKey).filter(APIKey.key_hash == hashed).first()
        # find matching key

        if not key or not key.is_active:
            return None
        # invalid or disabled key

        return key.user_id
        # valid → return user

    finally:
        db.close()