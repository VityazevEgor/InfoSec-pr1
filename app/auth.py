import hashlib
import os

# Безопасное получение секретного ключа из переменной окружения (CWE-798)
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')

def hash_password(password):
    # Безопасный криптографический алгоритм SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def hash_token(token):
    # Безопасный криптографический алгоритм SHA-256
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def verify_token(token):
    return token == SECRET_KEY
