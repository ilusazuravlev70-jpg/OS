from src import syscalls

def main():
    current_user = "guest"
    prompt = f"{current_user}@studyos"
    
    print("=== Welcome to StudyOS ===")
    print("Type 'help' for commands.")
    
    while True:
        try:
            command = input(f"{prompt} > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nИспользуйте 'exit' для выхода.")
            continue

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "help":
            print("Доступные команды: help, echo, users, whoami, login, create, ls, ps, exit")
        
        elif cmd == "echo":
            print(syscalls.sys_echo(" ".join(args)))
            
        elif cmd == "users":
            for user in syscalls.sys_get_users():
                print(f"{user['login']} ({user['role']})")
                
        elif cmd == "whoami":
            print(syscalls.sys_whoami())
            
        elif cmd == "login":
            login = input("Login: ")
            password = input("Password: ")
            if syscalls.sys_login(login, password):
                current_user = login
                prompt = f"{current_user}@studyos"
                print("Вход выполнен.")
            else:
                print("Ошибка доступа.")
                
        elif cmd == "create":
            path = input("Path: ")
            content = input("Content: ")
            fid = syscalls.sys_create_file(path, content)
            print(f"Файл создан с ID: {fid}")
            
        elif cmd == "ls":
            for fname in syscalls.sys_list_files("."):
                print(fname)
                
        elif cmd == "ps":
            for proc in syscalls.sys_ps():
                print(proc)
                
        elif cmd == "exit":
            print("Выключение...")
            syscalls.sys_shutdown()
            break
            
        else:
            print(f"Неизвестная команда: {cmd}")

if __name__ == "__main__":
    main()