import os
import hashlib
from utils.password_config import PASSWORD_CONFIG, is_password_complex
from django.contrib.auth.password_validation import CommonPasswordValidator



def hash_password(raw_password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 100000)
    return salt + hashed_password


def check_password(raw_password, stored_password):
    salt = stored_password[:32]
    stored_hashed_password = stored_password[32:]
    hashed_password = hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 100000)
    return stored_hashed_password == hashed_password


def is_password_unique(user, new_password):
    from users.models import PasswordHistory

    history = PasswordHistory.objects.filter(user=user).order_by('-created_at')[:PASSWORD_CONFIG['history_limit']]
    for record in history:
        if check_password(new_password, record.password):
            return False
    return True



def is_password_in_django_common_passwords(password):
    validator = CommonPasswordValidator()
    try:
        validator.validate(password)
        return False
    except:
        return True


def validate_password(password, user=None):
    errors = []
    errors.extend(is_password_complex(password))


    if is_password_in_django_common_passwords(password):
        errors.append("Password is too common, please choose another one.")

    if user and not is_password_unique(user, password):
        errors.append("You cannot reuse your previous passwords.")

    return errors

