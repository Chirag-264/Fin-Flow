import bcrypt
import jwt
import datetime

SECRET_KEY = "e5b7a9d9f34c6f1a3d2b5c9f8a7e6d1c4b3a2f9e8d7c6b5a1e2d3f4c5b6a7d8e"  # Replace with a secure key

def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    """Verifies a password against a hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt_token(user_id, expires_in=3600):
    """Generates a JWT token for user authentication."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    payload = {"user_id": user_id, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token):
    """Decodes a JWT token and verifies its authenticity."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
