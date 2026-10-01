from src import syscalls

def run_tests():
    # Тест 1: гость не может удалить файл админа
    result = syscalls.sys_delete_file("/admin_secret.txt", "guest")
    if result is False:
        print("[PASS] guest не может удалить файл admin")
    else:
        print("[FAIL] guest почему-то удалил файл")

    # Тест 2: гость не может убить процесс
    result = syscalls.sys_kill(999, "guest")
    if result is False:
        print("[PASS] guest не может убить процесс")
    else:
        print("[FAIL] guest убил процесс")

if __name__ == "__main__":
    run_tests()