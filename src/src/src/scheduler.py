import sqlite3
from typing import List, Dict, Optional

DB_PATH = 'db/os.sqlite'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_select(query: str, params: tuple = ()) -> List[Dict]:
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def execute_insert(query: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def execute_delete(query: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount

def create_process(name: str, owner: str, memory_mb: int = 0) -> int:
    from src import kernel
    if not kernel.kernel_instance.allocate_memory(memory_mb):
        return -1
    return execute_insert("INSERT INTO processes (name, state, owner, memory_used) VALUES (?, 'ready', ?, ?)", 
                          (name, owner, memory_mb))

def list_processes() -> List[Dict]:
    return execute_select("SELECT pid, name, state, owner, memory_used FROM processes")

def get_process(pid: int) -> Optional[Dict]:
    result = execute_select("SELECT pid, name, state, owner, memory_used FROM processes WHERE pid = ?", (pid,))
    return result[0] if result else None

def terminate_process(pid: int) -> bool:
    from src import kernel
    proc = get_process(pid)
    if not proc:
        return False
    kernel.kernel_instance.free_memory(proc['memory_used'])
    count = execute_delete("DELETE FROM processes WHERE pid = ?", (pid,))
    return count > 0

def schedule_round_robin() -> Optional[Dict]:
    processes = execute_select("SELECT * FROM processes WHERE state = 'ready' ORDER BY pid ASC LIMIT 1")
    if not processes:
        return None
    proc = processes[0]
    execute_update("UPDATE processes SET state = 'running' WHERE pid = ?", (proc['pid'],))
    execute_update("UPDATE processes SET state = 'ready' WHERE pid != ? AND state = 'running'", (proc['pid'],))
    return proc