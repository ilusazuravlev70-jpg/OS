            elif cmd == "create":
                path = input("Путь: ")
                content = input("Содержимое: ")
                fid = sys_create_file(path, content, current_user)
                if fid == -1:
                    print("Файл с таким путём уже существует")
                else:
                    print(f"Создан файл с id={fid}")

            elif cmd == "cat":
                if not arg:
                    print("Укажите путь к файлу")
                else:
                    content = sys_read_file(arg, current_user)
                    if content:
                        print(content)
                    else:
                        print("(файл пуст или не существует)")

            elif cmd == "ls":
                files = sys_list_files(arg or "/", current_user)
                if not files:
                    print("(нет файлов)")
                else:
                    for f in files:
                        print(f" {f}")

            elif cmd == "run":
                if not arg:
                    print("Укажите имя программы")
                else:
                    pid = sys_exec(arg, current_user)
                    if pid == -1:
                        print("Не удалось запустить: нет свободной памяти")
                    else:
                        print(f"Запущен процесс с PID={pid}")

            elif cmd == "kill":
                if not arg:
                    print("Укажите PID процесса")
                else:
                    try:
                        pid = int(arg)
                    except ValueError:
                        print("PID должен быть числом")
                        continue
                    if sys_kill(pid, current_user):
                        print(f"Процесс {pid} завершён")
                    else:
                        print(f"Не удалось завершить процесс {pid}")

            elif cmd == "mem":
                from src.db import execute_select
                mem_state = execute_select("SELECT used, limit FROM memory_state ORDER BY id DESC LIMIT 1")[0]
                print(f"Использовано: {mem_state['used']} / {mem_state['limit']} МБ")
                print(f"Свободно: {mem_state['limit'] - mem_state['used']} МБ")