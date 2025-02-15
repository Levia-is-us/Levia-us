import threading


class TaskManager:
    """
    TaskManager is a class that manages the tasks for the user.
    Implemented as a Singleton pattern with thread safety.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TaskManager, cls).__new__(cls)
                cls._instance.tasks = {}
                cls._instance.current_tasks = {}
                cls._instance.task_lock = threading.Lock()
        return cls._instance

    def init_tasks(self, tasks, user_id="local"):
        if not isinstance(tasks, list):
            raise ValueError("tasks must be a list of dicts")
        if not all(isinstance(task, dict) for task in tasks):
            raise ValueError("task must be a dict")
        with self.task_lock:
            self.tasks[user_id] = tasks
            self.current_tasks[user_id] = 0

    def update_task(self, task, user_id="local"):
        with self.task_lock:
            if user_id not in self.tasks:
                self.init_tasks(user_id)
            self.tasks[user_id].append(task)

    def get_current_task(self, user_id="local"):
        with self.task_lock:
            return self.tasks[user_id][self.current_tasks[user_id]]

    def get_next_task(self, user_id="local"):
        with self.task_lock:
            self.current_tasks[user_id] += 1
            return self.tasks[user_id][self.current_tasks[user_id]]

    def get_all_tasks(self, user_id="local"):
        with self.task_lock:
            return self.tasks[user_id].copy()

    def get_current_task_index(self, user_id="local"):
        with self.task_lock:
            return self.current_tasks[user_id]

    def get_total_tasks(self, user_id="local"):
        with self.task_lock:
            return len(self.tasks[user_id])

    def get_task_by_index(self, index, user_id="local"):
        with self.task_lock:
            return self.tasks[user_id][index]
