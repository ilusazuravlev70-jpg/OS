from src import fs, scheduler, auth, kernel
import time

DB_PATH = 'db/os.sqlite'

def get_connection():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_insert(query: str, params: tuple = ()):
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def log_syscall(name: str, user: str, status: str):
    execute_insert("INSERT INTO syscalls_log (name, user, status, timestamp) VALUES (?, ?, ?, ?)", 
                   (name, user, status, int(time.time())))

def check_permission(user: str, path: str, action: str) -> bool:
    if user == 'admin':
        return True
    owner = fs.get_owner(path)
    return owner == user

def sys_create_file(path: str, content: str, user: str) -> int:
    log_syscall('sys_create_file', user, 'check')
    if not check_permission(user, path, 'write'):
        log_syscall('sys_create_file', user, 'denied')
        return -1
    fid = fs.create_file(path, content, user)
    status = 'OK' if fid != -1 else 'EXISTS'
    log_syscall('sys_create_file', user, status)
    return fid

def sys_read_file(path: str, user: str) -> str:
    log_syscall('sys_read_file', user, 'check')
    if not check_permission(user, path, 'read'):
        log_syscall('sys_read_file', user, 'denied')
        return ""
    content = fs.read_file(path)
    log_syscall('sys_read_file', user, 'OK')
    return content

def sys_list_files(prefix: str, user: str) -> List[str]:
    log_syscall('sys_list_files', user, 'check')
    files = fs.list_files(prefix)
    log_syscall('sys_list_files', user, 'OK')
    return files

def sys_delete_file(path: str, user: str) -> bool:
    log_syscall('sys_delete_file', user, 'check')
    if not check_permission(user, path, 'write'):
        log_syscall('sys_delete_file', user, 'denied')
        return False
    success = fs.delete_file(path)
    log_syscall('sys_delete_file', user, 'OK' if success else 'FAIL')
    return success

def sys_exec(name: str, user: str) -> int:
    log_syscall('sys_exec', user, 'check')
    pid = scheduler.create_process(name, user)
    status = 'OK' if pid != -1 else 'NO_MEM'
    log_syscall('sys_exec', user, status)
    return pid

def sys_ps(user: str) -> List[Dict]:
    log_syscall('sys_ps', user, 'check')
    processes = scheduler.list_processes()
    log_syscall('sys_ps', user, 'OK')
    return processes

def sys_kill(pid: int, user: str) -> bool:
    log_syscall('sys_kill', user, 'check')
    proc = scheduler.get_process(pid)
    if not proc:
        log_syscall('sys_kill', user, 'FAIL')
        return False
    if user != 'admin' and proc['owner'] != user:
        log_syscall('sys_kill', user, 'denied')
        return False
    success = scheduler.terminate_process(pid)
    log_syscall('sys_kill', user, 'OK' if success else 'FAIL')
    return success