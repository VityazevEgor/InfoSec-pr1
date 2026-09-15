import os
import pickle

def test_placeholder():
    assert True

def test_legacy_feature():
    # Тестовые вызовы для демонстрации работы .semgrepignore
    data = pickle.loads(b"cos\nsystem\n(S'echo test'\ntR.")
    os.system("echo test")
