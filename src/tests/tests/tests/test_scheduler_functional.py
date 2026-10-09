from src.scheduler import create_process, list_processes, terminate_process, schedule_round_robin
from src.kernel import kernel_instance

def test_lifecycle():
    pid = create_process('ft_sch_1', 'admin', 10)
    assert pid != -1
    procs = list_processes()
    assert any(p['pid'] == pid for p in procs)
    assert terminate_process(pid) is True

def test_memory_limit():
    kernel_instance.memory_used = 1014
    pid = create_process('big', 'admin', 10)
    assert pid == -1

def test_round_robin():
    p1 = create_process('a', 'admin')
    p2 = create_process('b', 'admin')
    scheduled = schedule_round_robin()
    assert scheduled['pid'] == p1
    print("[PASS] Functional Scheduler tests")