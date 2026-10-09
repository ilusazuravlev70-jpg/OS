from src.kernel import kernel_instance as k

def test_allocate_success():
    k.memory_used = 0
    assert k.allocate_memory(100) == True
    assert k.memory_used == 100
    print("[PASS] allocate_memory success")

def test_allocate_fail():
    k.memory_used = 1014
    assert k.allocate_memory(10) == False
    assert k.memory_used == 1014
    print("[PASS] allocate_memory fail")

def test_free_success():
    k.memory_used = 100
    assert k.free_memory(50) == True
    assert k.memory_used == 50
    print("[PASS] free_memory success")

def test_free_fail():
    k.memory_used = 10
    assert k.free_memory(20) == False
    assert k.memory_used == 10
    print("[PASS] free_memory fail")

def test_save_load_state():
    k.memory_used = 123
    k.save_memory_state()
    k.memory_used = 0
    k.load_memory_state()
    assert k.memory_used == 123
    print("[PASS] save/load memory state")

def test_memory_info():
    info = k.memory_info()
    assert 'used' in info and 'limit' in info
    print("[PASS] memory_info")

def test_session_start():
    assert k.start_session('admin') is not None
    assert k.current_user == 'admin'
    print("[PASS] start_session")

def test_session_end():
    k.start_session('admin')
    k.end_session()
    assert k.current_user is None
    print("[PASS] end_session")