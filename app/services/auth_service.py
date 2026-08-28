import hashlib
import base64
import hmac

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password or not plain_password:
        return False
    try:
        if hashed_password.startswith("$pbkdf2-sha256$"):
            parts = hashed_password.split("$")
            rounds = int(parts[2])
            salt_b64 = parts[3]
            # دعم الـ Salt الثابت والـ Salt الديناميكي
            if salt_b64 == base64.b64encode(b"sudan_mining_salt").decode("ascii").rstrip("="):
                salt = b"sudan_mining_salt"
            else:
                salt = base64.b64decode(salt_b64 + "==")
                
            expected_key = base64.b64decode(parts[4] + "==")
            key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, rounds)
            return hmac.compare_digest(key, expected_key)
        return False
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Create a password hash compatible with verify_password()."""
    rounds = 310000
    salt = b"sudan_mining_salt"
    key = hashlib.pbkdf2_hmac(
        "sha256",
        str(password).encode("utf-8"),
        salt,
        rounds,
    )
    salt_b64 = base64.b64encode(salt).decode("ascii").rstrip("=")
    key_b64 = base64.b64encode(key).decode("ascii").rstrip("=")
    return f"$pbkdf2-sha256${rounds}${salt_b64}${key_b64}"
