from .db import get_connection
from getpass import getpass
from encryption.modes import encrypt_CTR, decrypt_CTR

def get_credentials(user):
    conn = get_connection()
    cur = conn.cursor()

    user_id = user[0]
    cur.execute("""
        SELECT credential_id, user_id, service, login_username, ciphertext, nonce
        FROM credentials
        WHERE user_id = %s
    """, (user_id,))

    credentials = cur.fetchall()

    if not credentials:
        return None
    else:
        count = 0
        for cred_id, user_id, service, username, ciphertext, nonce in credentials:
            count += 1
            print(f"  {count}. {service}")
    cur.close()
    conn.close()

    return credentials

def delete_credential(user, credential):
    conn = get_connection()
    cur = conn.cursor()

    cred_id = credential[0]
    user_id = user[0]
    cur.execute("""
        DELETE FROM credentials
        WHERE credential_id = %s
        AND user_id = %s
    """, (cred_id, user_id))

    conn.commit()
    cur.close()
    conn.close()

def add_credentials(user, service, login_username, password, aes_key):
    conn = get_connection()
    cur = conn.cursor()
    user_id = user[0]

    password_bytes = password.encode("utf-8")

    nonce, ciphertext = encrypt_CTR(password_bytes, aes_key)


    cur.execute(
        """
        INSERT INTO credentials (user_id, service, login_username, ciphertext, nonce)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, service, login_username, ciphertext, nonce)    
    )
    conn.commit()

    cur.close()
    conn.close()

# credential[] : credential_id, user_id, service, login_username, ciphertext, nonce 
def edit_credentials(user, aes_key, credential, service, username, password):
    conn = get_connection()
    cur = conn.cursor()

    user_id = user[0]
    cred_id = credential[0]
    if service == "":
        new_service = credential[2]
    else:
        new_service = service

    if username == "":
        new_username = credential[3]
    else:
        new_username = username

    if password == "":
        nonce = credential[5]
        ciphertext = credential[4]
    else:
        password_bytes = password.encode("utf-8")
        nonce, ciphertext = encrypt_CTR(password_bytes, aes_key)
    
    cur.execute(
        """
        UPDATE credentials
        SET
            service = %s,
            login_username = %s,
            ciphertext = %s, 
            nonce = %s
        WHERE credential_id = %s
        AND user_id = %s
        """,
        (new_service, new_username, ciphertext, nonce, cred_id, user_id)
    )
    conn.commit()

    updated_credential = (cred_id, user_id, new_service, new_username, ciphertext, nonce)

    cur.close()
    conn.close()

    return updated_credential