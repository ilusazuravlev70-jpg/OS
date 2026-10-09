from src.syscalls import sys_login, sys_create_file, sys_read_file, sys_delete_file, sys_exec, sys_kill

def test_admin_flow():
    assert sys_login('admin', 'admin123') is not None
    fid = sys_create_file('/int_full', 'content', 'admin')
    assert fid != -1
    assert sys_read_file('/int_full', 'admin') == 'content'
    pid = sys_exec('int_app', 'admin')
    assert pid != -1
    assert sys_kill(pid, 'admin') is True
    assert sys_delete_file('/int_full', 'admin') is True

def test_user_permissions():
    assert sys_login('user', 'user1234') is not None
    sys_create_file('/user_file', 'x', 'user')
    # Попытка удалить чужой файл
    assert sys_delete_file('/int_full', 'user') is False
    # Попытка убить чужой процесс (если бы он был)
    print("[PASS] Integration Full tests")