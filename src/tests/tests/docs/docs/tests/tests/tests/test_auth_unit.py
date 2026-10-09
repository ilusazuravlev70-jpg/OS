from src.auth import hash_password, check_credentials, register_user, change_password
import os

def test_hash_password():
    h = hash_password("secret")
    assert len(h) == 64
    assert h != "secret"
    print("[PASS] hash_password")

def test_check_valid():
    # Предполагается, что admin:secret уже есть в БД
    assert check_credentials("admin", "secret") == True
    print("[PASS] check_credentials valid")

def test_check_invalid():
    assert check_credentials("admin", "123") == False
    print("[PASS] check_credentials invalid")

def test_register():
    # Очистка или проверка уникальности
    if register_user("temp_user", "123"):
        assert check_credentials("temp_user", "123") == True
        print("[PASS] register_user")
    else:
        print("[SKIP] register_user (already exists)")

def test_change_password():
    # Проверка смены пароля для существующего пользователя
    if change_password("admin", "new_pass"):
        assert check_credentials("admin", "new_pass") == True
        print("[PASS] change_password")
    else:
        print("[FAIL] change_password")

def test_check_guest():
    assert check_credentials("guest", "") == False
    print("[PASS] check_guest")

def test_register_duplicate():
    # admin уже есть
    assert register_user("admin", "123") == False
    print("[PASS] register_duplicate")

def test_hash_consistency():
    h1 = hash_password("same")
    h2 = hash_password("same")
    assert h1 == h2
    print("[PASS] hash_consistency")