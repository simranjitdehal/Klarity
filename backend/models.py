from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    key_hash = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    daily_limit = Column(Integer, default=1000)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reset_date = Column(DateTime, default=datetime.utcnow)

class incoming_log(Base):
    __tablename__ = "incoming_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    raw_log = Column(Text)
    environment = Column(String(50))
    timestamp = Column(DateTime)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    exception_type = Column(String(100))
    exception_message = Column(Text)
    file = Column(String(255))
    line = Column(Integer)
    function = Column(String(100))

    probable_cause = Column(Text)
    fix_summary = Column(Text)
    detailed_steps = Column(Text)
    severity = Column(String(20))
    ai_summary = Column(Text)