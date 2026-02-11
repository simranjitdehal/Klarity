import secrets
import bcrypt

def generate_api_key() -> str:
    return secrets.token_hex(20)

def hash_api_key(api_key: str) -> str:
    hashed = bcrypt.hashpw(api_key.encode(), bcrypt.gensalt())
    return hashed.decode()

def verify_api_key(api_key: str, hashed: str) -> bool:
    return bcrypt.checkpw(api_key.encode(), hashed.encode())
