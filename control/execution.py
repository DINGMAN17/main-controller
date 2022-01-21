import queue

from control.task_list import Tasks


class Execution:
    def __init__(self):
        self.admin = None
        self.users = []
        self.controller_clients = {}
        self.data_queue = queue.Queue()
        self.info_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.warning_queue = queue.Queue()
        self.emergency_queue = queue.Queue()
        self.tasks_list = Tasks()

    def get_client_status(self):
        pass

    def get_active_clients(self):
        pass