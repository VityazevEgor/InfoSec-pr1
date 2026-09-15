import hashlib
import os

# Уязвимость 2: Хардкод секретного ключа в исходном коде (CWE-798)
SECRET_KEY = "hardcoded-super-secret-token-12345"

def hash_password(password):
    # Уязвимость 3: Использование устаревшего алгоритма хеширования MD5 (CWE-327)
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def hash_token(token):
    # Уязвимость 4: Использование скомпрометированного алгоритма SHA-1 (CWE-327)
    return hashlib.sha1(token.encode('utf-8')).hexdigest()

def verify_token(token):
    return token == SECRET_KEY
