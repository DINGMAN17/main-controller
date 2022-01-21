import queue


class Tasks:
    def __init__(self):
        self.tasks_dict = {}
        self.init_tasks()

    def init_tasks(self):
        self.tasks_dict['prev'] = queue.Queue()
        self.tasks_dict['now'] = queue.Queue()
        self.tasks_dict['next'] = queue.Queue()

    def get_current_tasks(self):
        pass

    def get_prev_tasks(self):
        pass

    def get_future_tasks(self):
        pass

    def modify_future_tasks(self):
        pass