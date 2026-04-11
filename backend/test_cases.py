from db import SessionLocal
from models import User
from auth import create_api_key, get_user_from_api_key

# 1. create user
db = SessionLocal()

user = User(
    username="User2",
    email="user2@example.com",
    password_hash="passuser2"
)

db.add(user)
db.commit()

print("USER ID:", user.id)

db.close()

# 2. generate API key
key = create_api_key(user.id)
print("API KEY:", key)

# 3. validate API key
user_id = get_user_from_api_key(key)
print("VALIDATED USER ID:", user_id)