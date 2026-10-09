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

def execute_update(query: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount

def execute_delete(query: str, params: tuple = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount

def create_file(path: str, content: str, owner: str) -> int:
    existing = execute_select("SELECT id FROM files WHERE path = ?", (path,))
    if existing:
        return -1
    return execute_insert("INSERT INTO files (path, content, owner) VALUES (?, ?, ?)", (path, content, owner))

def read_file(path: str) -> str:
    result = execute_select("SELECT content FROM files WHERE path = ?", (path,))
    return result[0]['content'] if result else ""

def write_file(path: str, content: str) -> bool:
    count = execute_update("UPDATE files SET content = ? WHERE path = ?", (content, path))
    return count > 0

def delete_file(path: str) -> bool:
    count = execute_delete("DELETE FROM files WHERE path = ?", (path,))
    return count > 0

def list_files(prefix: str = "/") -> List[str]:
    if not prefix.endswith("/"):
        prefix += "/"
    result = execute_select("SELECT path FROM files WHERE path LIKE ?", (f"{prefix}%",))
    return [row['path'] for row in result]

def get_owner(path: str) -> Optional[str]:
    result = execute_select("SELECT owner FROM files WHERE path = ?", (path,))
    return result[0]['owner'] if result else None

def get_file_info(path: str) -> Optional[Dict]:
    result = execute_select("SELECT id, path, content, owner FROM files WHERE path = ?", (path,))
    return result[0] if result else None