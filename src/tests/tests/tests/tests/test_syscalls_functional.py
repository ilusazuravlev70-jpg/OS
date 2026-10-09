from src.syscalls import (sys_create_file, sys_read_file, sys_delete_file, 
                          sys_list_files, sys_exec, sys_kill, sys_ps, sys_login)
from src.db import execute_select

def test_create_log():
    sys_login('admin', 'admin123')
    fid = sys_create_file('/ft_sys_1', 'x', 'admin')
    assert fid != -1
    logs = execute_select('syscalls_log', {'syscall_name': 'sys_create_file'})
    assert logs[-1]['status'] == 'OK'

def test_delete_denied():
    sys_create_file('/admin_file', 'x', 'admin')
    sys_login('user', 'user1234')
    assert sys_delete_file('/admin_file', 'user') is False
    logs = execute_select('syscalls_log', {'syscall_name': 'sys_delete_file'})
    assert logs[-1]['status'] == 'DENIED'

def test_exec_memory():
    from src.kernel import kernel_instance
    before = kernel_instance.memory_used
    pid = sys_exec('ft_app', 'admin', 10)
    assert pid != -1
    assert kernel_instance.memory_used > before
    sys_kill(pid, 'admin')
    print("[PASS] Functional Syscalls tests")