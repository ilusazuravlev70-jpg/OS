from src.db import execute_select, execute_insert, execute_update, execute_delete

def test_select():
    result = execute_select("SELECT 1 as val", ())
    assert result == [{'val': 1}]
    print("[PASS] execute_select")

def test_insert():
    # Используем временную таблицу или гарантируем очистку
    rowid = execute_insert("INSERT INTO files (path, content, owner) VALUES ('/t1', 'c', 'u')", ())
    assert isinstance(rowid, int) and rowid > 0
    print("[PASS] execute_insert")

def test_update():
    execute_insert("INSERT INTO files (path, content, owner) VALUES ('/t2', 'old', 'u')", ())
    count = execute_update("UPDATE files SET content = 'new' WHERE path = '/t2'", ())
    assert count == 1
    print("[PASS] execute_update")

def test_delete():
    execute_insert("INSERT INTO files (path, content, owner) VALUES ('/t3', 'c', 'u')", ())
    count = execute_delete("DELETE FROM files WHERE path = '/t3'", ())
    assert count == 1
    print("[PASS] execute_delete")

def test_select_empty():
    result = execute_select("SELECT * FROM files WHERE path = '/nope'", ())
    assert result == []
    print("[PASS] execute_select empty")

def test_connection():
    # Просто проверяем, что функция возвращает объект
    from src.db import get_connection
    conn = get_connection()
    assert conn is not None
    conn.close()
    print("[PASS] get_connection")