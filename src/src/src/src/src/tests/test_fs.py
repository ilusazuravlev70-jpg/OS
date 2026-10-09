from src.fs import create_file, read_file, write_file, delete_file, list_files, get_owner

def test_create_and_read():
    fid = create_file('/test_unit', 'data', 'admin')
    assert fid != -1
    assert read_file('/test_unit') == 'data'
    assert delete_file('/test_unit') is True

def test_duplicate():
    create_file('/dup', 'x', 'admin')
    assert create_file('/dup', 'y', 'admin') == -1

def test_list():
    create_file('/a', '1', 'admin')
    create_file('/b', '2', 'admin')
    files = list_files('/')
    assert '/a' in files and '/b' in files

def test_write():
    create_file('/w', 'old', 'admin')
    assert write_file('/w', 'new') is True
    assert read_file('/w') == 'new'

def test_owner():
    create_file('/own', 'x', 'admin')
    assert get_owner('/own') == 'admin'