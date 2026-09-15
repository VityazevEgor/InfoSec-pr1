import hashlib
import os

# Уязвимость 2: Хардкод секретного ключа в исходном коде (CWE-798)
SECRET_KEY = "hardcoded-super-secret-token-12345"

def hash_password(password):
    # Безопасный криптографический алгоритм SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def hash_token(token):
    # Безопасный криптографический алгоритм SHA-256
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def verify_token(token):
    return token == SECRET_KEY
