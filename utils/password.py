from passlib.hash import bcrypt

def secure_password(password) -> None:
    hasher = bcrypt.using(rounds=13)
    hashed_password = hasher.hash(password)

    return hashed_password