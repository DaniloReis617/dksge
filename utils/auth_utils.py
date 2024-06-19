import hashlib
from utils.db_utils import register_user, authenticate_user
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    hashed_password = hash_password(password)
    user = authenticate_user(username, hashed_password)
    if user:
        return True
    return False

def register(username, password):
    hashed_password = hash_password(password)
    register_user(username, hashed_password)
