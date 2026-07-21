# SecureDB Password Manager

## Overview
A command-line password manager written in Python that securely stores credentials using PostgreSQL and a custom implementation of AES-256 in CTR mode, originally written by me in Java, and now ported to Python years later.

I created this project to learn the principles behind security for secure credential storage and to better understand the software responsible for protecting my own sensitive information.

## Features
 - User registration and authentication with Argon2 password hashing
 - Add, edit, view, and delete credentials, with clipboard copy support
 - AES-CTR and are encrypted using a key derived from the user's master password via PBKDF2
 - Encryptd passwords are stored as ciphertext and nonce pairs in PostgreSQL
 - Dockerized PostgreSQL database for persistent data storage

## Technologies
 - Python (psycopg)
 - PostgreSQL
 - Docker
 - Cryptography (AES, Argon2, PBKDF2)

## Installation
1. Clone the repository
2. Install dependencies
3. Start PostgreSQL
4. Run the application

## Usage

## Project Structure

authentication/
database/
encryption/
menus/

## Security Notes
- Master passwords are hashed using Argon2 before storage.
- Stored credentials are encrypted with AES-CTR.
- Passwords are never stored or shown in plaintext and are only displayed when explicitly requested by the user.
- The application clears the terminal display and terminates the active user session on logout.


