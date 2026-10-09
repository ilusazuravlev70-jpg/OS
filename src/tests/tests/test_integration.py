import os
import sqlite3
import time
from src import shell, auth, fs, scheduler, syscalls, kernel

DB_PATH = 'db/os.sqlite'

def setup_db():
    # Сброс базы перед тестами для чистоты
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    from src import db
    # Предполагается, что в db.py есть функция init_db()
    if hasattr(db, 'init_db'):
        db.init_db()
    else:
        # Если init_db нет, просто подключаемся (таблицы уже созданы)
        conn = sqlite3.connect(DB_PATH)
        conn.close()

def test_full_user_flow():
    setup_db()
    # 1. Регистрация и вход (если есть регистрация, иначе сразу login)
    # Здесь предполагаем, что пользователь 'user' уже создан в таблице users
    # Проверяем вход
    assert auth.check_credentials('user', 'password') == True
    
    # 2. Создание файла через системный вызов
    fid = syscalls.sys_create_file('/int_test.txt', 'integration', 'user')
    assert fid != -1
    
    # 3. Чтение файла
    content = syscalls.sys_read_file('/int_test.txt', 'user')
    assert content == 'integration'
    
    # 4. Запуск процесса
    pid = syscalls.sys_exec('test_app', 'user')
    assert pid != -1
    
    # 5. Проверка списка процессов
    procs = syscalls.sys_ps('user')
    assert any(p['pid'] == pid for p in procs)
    
    # 6. Завершение процесса
    assert syscalls.sys_kill(pid, 'user') == True
    
    # 7. Проверка освобождения памяти
    mem = kernel.kernel_instance.memory_used
    # Память процесса (допустим 10 МБ) должна освободиться
    assert mem < 1024 
    
    # 8. Удаление файла
    assert syscalls.sys_delete_file('/int_test.txt', 'user') == True
    
    # 9. Проверка логов
    from src.db import execute_select
    logs = execute_select("SELECT name FROM syscalls_log")
    names = [log['name'] for log in logs]
    assert 'sys_create_file' in names
    assert 'sys_read_file' in names
    assert 'sys_exec' in names
    assert 'sys_kill' in names
    assert 'sys_delete_file' in names

def test_permission_isolation():
    setup_db()
    # Admin создает файл
    syscalls.sys_create_file('/admin_secret', 'data', 'admin')
    # User пытается удалить
    result = syscalls.sys_delete_file('/admin_secret', 'user')
    assert result == False
    
    # Проверка, что файл на месте
    files = fs.list_files('/')
    assert '/admin_secret' in files

def test_memory_limit_integration():
    setup_db()
    from src.kernel import kernel_instance
    kernel_instance.memory_used = 1014  # Оставим 10 МБ
    kernel_instance.save_memory_state()
    
    # Попытка создать процесс на 20 МБ должна провалиться
    pid = syscalls.sys_exec('big_app', 'admin', 20)
    assert pid == -1