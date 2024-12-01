from datetime import datetime, timedelta

temp_storage = {}

def store_temp_data(token: str, hashed_password: str):
    """Store token and hashed password with expiration time.
    """
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    temp_storage[token] = {"hashed_password": hashed_password, "expires_at": expiration_time}

def retrieve_temp_data(token: str):
    """Retrieve hashed password if token is valid and not expired.
    """
    data = temp_storage.get(token)
    if data and data["expires_at"] > datetime.utcnow():
        return data["hashed_password"]
    return None

def delete_temp_data(token: str):
    """Delete temporary token and password storage.
    """
    temp_storage.pop(token, None)