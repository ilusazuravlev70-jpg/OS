from src.scheduler import create_process, list_processes, terminate_process, schedule_round_robin
from src.kernel import kernel_instance

def test_process_lifecycle():
    pid = create_process('test_app', 'admin', 10)
    assert pid != -1
    procs = list_processes()
    assert any(p['pid'] == pid for p in procs)
    assert terminate_process(pid) is True
    assert not any(p['pid'] == pid for p in list_processes())

def test_memory_limit():
    kernel_instance.memory_used = 0
    kernel_instance.save_memory_state()
    assert create_process('small', 'admin', 10) != -1
    assert create_process('huge', 'admin', 2000) == -1

def test_round_robin():
    p1 = create_process('a', 'admin')
    p2 = create_process('b', 'admin')
    scheduled = schedule_round_robin()
    assert scheduled['pid'] == p1
    procs = list_processes()
    state_p1 = next(p for p in procs if p['pid'] == p1)['state']
    state_p2 = next(p for p in procs if p['pid'] == p2)['state']
    assert state_p1 == 'running'
    assert state_p2 == 'ready'