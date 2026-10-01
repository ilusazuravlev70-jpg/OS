def get_user_role(username):
    from src.db import get_connection
    with get_connection() as conn:
        user = conn.execute("SELECT role FROM users WHERE login = ?", (username,)).fetchone()
        return user['role'] if user else None

def check_permission(action, username):
    # Пока простая логика: admin может всё, остальные — только своё
    role = get_user_role(username)
    if role == 'admin':
        return True
    # Здесь будет логика для обычных пользователей
    return False 