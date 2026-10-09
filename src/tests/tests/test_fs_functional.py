from src.fs import create_file, read_file, write_file, delete_file, list_files, get_owner
from src.db import execute_select

def test_create_and_read():
    fid = create_file('/ft_fs_1', 'data', 'admin')
    assert fid != -1
    assert read_file('/ft_fs_1') == 'data'
    assert delete_file('/ft_fs_1') is True

def test_read_missing():
    assert read_file('/nope') == ""

def test_write():
    create_file('/ft_fs_2', 'old', 'admin')
    assert write_file('/ft_fs_2', 'new') is True
    assert read_file('/ft_fs_2') == 'new'

def test_duplicate():
    create_file('/dup', 'x', 'admin')
    assert create_file('/dup', 'y', 'admin') == -1

def test_list():
    create_file('/a', '1', 'admin')
    create_file('/b', '2', 'admin')
    files = list_files('/')
    assert '/a' in files and '/b' in files

def test_owner():
    create_file('/own', 'x', 'admin')
    assert get_owner('/own') == 'admin'

def test_info():
    create_file('/info', 'x', 'admin')
    info = get_owner('/info')
    assert info is not None
    print("[PASS] Functional FS tests")