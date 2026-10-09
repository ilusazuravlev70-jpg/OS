class Kernel:
    # ... ваш существующий код инициализации ...

    def save_memory_state(self):
        from src.db import execute_update, execute_insert
        execute_update("DELETE FROM memory_state", ())
        execute_insert("INSERT INTO memory_state (used, limit) VALUES (?, ?)", (self.memory_used, self.memory_limit))

    def load_memory_state(self):
        from src.db import execute_select
        state = execute_select("SELECT used FROM memory_state ORDER BY id DESC LIMIT 1")
        if state:
            self.memory_used = state[0]['used']

    # Вызывайте save_memory_state в конце allocate_memory и free_memory
    def allocate_memory(self, mb: int) -> bool:
        if self.memory_used + mb > self.memory_limit:
            return False
        self.memory_used += mb
        self.save_memory_state()
        return True

    def free_memory(self, mb: int) -> bool:
        if self.memory_used - mb < 0:
            return False
        self.memory_used -= mb
        self.save_memory_state()
        return True