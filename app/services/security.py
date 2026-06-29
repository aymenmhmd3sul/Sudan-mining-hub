from passlib.hash import sha256_crypt

# -------- PASSWORD HASHING --------

def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return sha256_crypt.verify(password, hashed)
