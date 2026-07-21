import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="secure_db",
        user="sean",
        password="sparky"
    )