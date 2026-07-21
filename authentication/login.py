# 1. authenticate user
# 2. unlock vault

from argon2 import PasswordHasher
import hashlib
from getpass import getpass
from database.users import get_user
from database.credentials import get_credentials


ph = PasswordHasher()

def authenticate(username, password):
    user = get_user(username)
    if user is None: 
        return None
    
    try:
        ph.verify(user[3], password)
    except:
        return None
    
    return user

def derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000,
        dklen=32
    )

def login(username, password):
    user = authenticate(username, password)

    if user is None: 
        return None, None
    key = derive_key(password, user[6])
    print()

    return user, key

