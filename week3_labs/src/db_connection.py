import mysql.connector

def connect_db():
    db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "admin",
    database = "fletapp"
    )

    return db

# if __name__ == "__main__":
#     conn = connect_db()
#     if conn:
#         print("✅ Connection successful!")
#         print("Server info:", conn.get_server_info())
#         cursor = conn.cursor()
#         cursor.execute("SELECT DATABASE();")
#         record = cursor.fetchone()
#         print("Connected to database:", record)
#         cursor.close()
#         conn.close()
#     else:
#         print("❌ Connection failed!")
