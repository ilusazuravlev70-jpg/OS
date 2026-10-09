# Чек-лист функциональности (День 7)

## База данных (db.py)
[ ] execute_select возвращает список словарей.
[ ] execute_insert возвращает автоинкремент ID.
[ ] execute_update возвращает количество затронутых строк.
[ ] Подключение к БД не падает при отсутствии файла.

## Ядро (kernel.py)
[ ] allocate_memory возвращает False при лимите 1024 МБ.
[ ] free_memory корректно уменьшает счетчик.
[ ] save_memory_state записывает данные в таблицу memory_state.
[ ] load_memory_state считывает данные при старте.

## Аутентификация (auth.py)
[ ] hash_password использует SHA-256 (длина 64).
[ ] check_credentials находит пользователя в БД.
[ ] check_credentials возвращает False для гостя.
[ ] register_user хэширует пароль перед вставкой.
[ ] change_password обновляет хэш в БД.

## Файловая система (fs.py)
[ ] create_file возвращает -1 для дубликата.
[ ] read_file возвращает пустую строку для отсутствующего файла.
[ ] delete_file возвращает True при успешном удалении.
[ ] get_owner возвращает None для отсутствующего файла.

## Планировщик (scheduler.py)
[ ] create_process возвращает -1 при нехватке памяти.
[ ] schedule_round_robin выбирает первый процесс из очереди.
[ ] terminate_process освобождает память в ядре.

## Системные вызовы (syscalls.py)
[ ] sys_create_file логирует статус 'check' и 'OK'.
[ ] sys_delete_file проверяет права владельца.
[ ] sys_exec передает лимит памяти ядру.
[ ] sys_kill возвращает False для несуществующего PID.