def test_save_memory_state_unit():
    from src.kernel import Kernel
    from src.db import execute_select
    import os
    
    # Сброс состояния
    if os.path.exists('db/os.sqlite'):
        os.remove('db/os.sqlite')
    from src import db
    db.init_db()
    
    k = Kernel()
    k.allocate_memory(100)
    k.save_memory_state()
    
    states = execute_select('SELECT used FROM memory_state')
    assert len(states) >= 1
    assert states[0]['used'] == 100
    print("[PASS] save_memory_state unit test")