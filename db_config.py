import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="dentist",     
        user="postgres",       
        password="1403",    
        host="localhost",
        port="5432"
    )
