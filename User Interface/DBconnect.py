import cx_Oracle

def get_connection():
    try:
        dsn = cx_Oracle.makedsn(
            "localhost",   # database host"
            1521,          # port 
            service_name=" "  # enter database service name
        )
        conn = cx_Oracle.connect(
            user="system",    # database username
            password="*******", # (edit) database password
            dsn=dsn
        )
        print("Database connected!")
        return conn
    except cx_Oracle.DatabaseError as e:
        print("Database connection failed:", e)
        return None
