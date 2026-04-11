from db import engine, Base
from models import User, APIKey, incoming_log

Base.metadata.create_all(bind=engine)