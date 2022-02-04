import threading
from enum import Enum

from message.command.command import Command


class TaskStatus(Enum):
    YET_TO_START = "wait"
    ON_GOING = "ongoing"
    DONE = "done"
    FAIL = "fail"


class Task:
    def __init__(self, command: Command):
        self.command = command
        self.task_status = TaskStatus.ON_GOING
        self.lock = threading.Lock()

    def set_task_status(self, status: TaskStatus):
        with self.lock:
            self.task_status = status

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.command == other.command and self.task_status == other.task_status
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Tasks:
    def __init__(self):
        self.prev_tasks = {}
        self.ongoing_tasks = {}
        self.future_tasks = {}
        self.lock = threading.Lock()

    def get_current_tasks(self) -> dict:
        with self.lock:
            return self.ongoing_tasks

    def get_prev_tasks(self) -> dict:
        with self.lock:
            return self.prev_tasks

    def get_future_tasks(self) -> dict:
        with self.lock:
            return self.future_tasks

    def finish_task(self, task: Task):
        self.modify_tasks(task, self.ongoing_tasks, self.prev_tasks)

    def start_task(self, task: Task):
        self.modify_tasks(task, self.future_tasks, self.ongoing_tasks)

    def modify_tasks(self, task: Task, tasks_to_delete: dict, tasks_to_add: dict):
        with self.lock:
            controller_type = task.command.recipient
            tasks_to_add[controller_type] = task
            tasks_to_delete.pop(controller_type, None)

    def add_future_tasks(self, task: Task) -> None:
        with self.lock:
            controller_type = task.command.recipient
            self.future_tasks[controller_type] = task

