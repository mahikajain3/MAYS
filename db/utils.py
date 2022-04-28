from hashlib import sha256
import secrets
import string

INVALID_LOGIN_MSG = "Your email and password combination is invalid."
SALT_LEN = 256


def hash_pw(salt: str, pw: str) -> str:
    """
    Hashes password.
    """
    salted_password = pw + salt
    return sha256(salted_password.encode('utf-8')).hexdigest()


def gen_salt() -> str:
    alphanum = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphanum) for _ in range(SALT_LEN))