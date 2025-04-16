import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="dentist",     # change if needed
        user="postgres",        # <- your PostgreSQL username
        password="1403",    # <- your PostgreSQL password
        host="localhost",
        port="5432"
    )
