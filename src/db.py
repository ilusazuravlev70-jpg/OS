import sqlite3
import os

# Путь к файлу базы данных
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'os.sqlite')

def get_connection():
    """Возвращает соединение с базой данных"""
    conn = sqlite3.connect(DB_PATH)
    # Это нужно, чтобы данные из базы возвращались в виде словаря (удобно читать)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создает таблицы при первом запуске"""
    if not os.path.exists(DB_PATH):
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица процессов
            cursor.execute('''
                CREATE TABLE processes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    state TEXT NOT NULL,
                    owner_id INTEGER,
                    memory_kb INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            ''')
            
            # Таблица файлов
            cursor.execute('''
                CREATE TABLE files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    content TEXT,
                    owner_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            ''')
            
            # Журнал системных вызовов
            cursor.execute('''
                CREATE TABLE syscalls_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    args TEXT,
                    user TEXT,
                    status TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Вставляем администратора по умолчанию (пароль: admin)
            import hashlib
            admin_hash = hashlib.sha256('admin'.encode()).hexdigest()
            cursor.execute("INSERT INTO users (login, password_hash, role) VALUES (?, ?, ?)", 
                         ('admin', admin_hash, 'admin'))
            conn.commit()

# --- ТВОИ НОВЫЕ УНИВЕРСАЛЬНЫЕ ФУНКЦИИ (CRUD) ---

def execute_insert(table_name: str, data: dict) -> int:
    """Добавляет запись в таблицу и возвращает ID новой строки"""
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    values = tuple(data.values())
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid

def execute_select(table_name: str, where: dict = None, limit: int = None) -> list:
    """Ищет и возвращает данные из таблицы"""
    sql = f"SELECT * FROM {table_name}"
    values = ()
    if where:
        conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
        sql += f" WHERE {conditions}"
        values = tuple(where.values())
    if limit:
        sql += f" LIMIT {limit}"
        
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        return [dict(row) for row in cursor.fetchall()]

def execute_update(table_name: str, data: dict, where: dict) -> bool:
    """Обновляет данные в таблице"""
    set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
    where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    values = tuple(data.values()) + tuple(where.values())
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0

def execute_delete(table_name: str, where: dict) -> bool:
    """Удаляет данные из таблицы"""
    where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
    sql = f"DELETE FROM {table_name} WHERE {where_clause}"
    values = tuple(where.values())
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0

# Блок для быстрой проверки (можно запустить файл отдельно)
if __name__ == "__main__":
    init_db()
    print("База инициализирована. Проверка функций:")
    
    # Проверка INSERT
    new_id = execute_insert('users', {'login': 'test_user', 'password_hash': 'hash', 'role': 'user'})
    print(f"Добавлен пользователь с ID: {new_id}")
    
    # Проверка SELECT
    user = execute_select('users', {'login': 'admin'})
    print(f"Нашли админа: {user}")
    
    # Проверка UPDATE
    updated = execute_update('users', {'role': 'super_admin'}, {'login': 'admin'})
    print(f"Обновили роль админа: {updated}")
    
    # Проверка DELETE
    deleted = execute_delete('users', {'login': 'test_user'})
    print(f"Удалили тестового пользователя: {deleted}")