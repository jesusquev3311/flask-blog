from passlib.hash import bcrypt

def secure_password(password) -> None:
    hasher = bcrypt.using(rounds=13)
    hashed_password = hasher.hash(password)

    return hashed_password

def check_password(password, hash_key):
    result = bcrypt.verify(password, hash_key)

    return result 
