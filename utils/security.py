import bcrypt
import secrets
import string

def hash_password(password : str) -> str :
    '''Хэш пароля перед записью в бд'''
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes,salt).decode("utf-8")
    return hashed

def check_password(plain_password : str, hashed_password : str) -> bool :
    '''Проверка совпадения пароля с хэшем из базы'''
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def generate_secure_password(length=12) -> str :
    '''Генерация случайного пароля для root'''
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(characters) for _ in range(length))