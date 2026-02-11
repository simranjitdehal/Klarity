from db import get_db_connection

def main():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email FROM organizations LIMIT 1;")
    row = cursor.fetchone()

    print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
