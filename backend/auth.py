import bcrypt
from db import get_db_connection

def resolve_org_id(api_key: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, api_key_hash FROM organizations")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in rows:
        if row["api_key_hash"] is None:
            continue

        if bcrypt.checkpw(api_key.encode(), row["api_key_hash"].encode()):
            return row["id"]
        
    return None

#request auth function
def authenticate_request(api_key: str):
    if not api_key:
        raise PermissionError("API key is missing")
    
    ord_id = resolve_org_id(api_key)
    if ord_id is None:
        raise PermissionError("Invalid API key")
    
    return ord_id