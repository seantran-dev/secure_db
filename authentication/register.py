# register a new user to the database

from argon2 import PasswordHasher
import os
from database.users import create_user, get_user
from getpass import getpass


def register(username, email, password):

    ph = PasswordHasher()
    password_hash = ph.hash(password)
    kdf_salt = os.urandom(16)

    create_user(
        username, 
        email,
        password_hash,
        kdf_salt
    )