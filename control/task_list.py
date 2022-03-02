import threading
from enum import Enum

from typing import Dict, Optional

from communication.client import ClientType
from message.command.command import IntegrationCommandType, BaseCommandType
from message.command.command_executor import Command
from utils import LogMessage


class TaskStatus(Enum):
    WAIT = "wait"
    ON_GOING = "ongoing"
    DONE = "done"
    FAIL = "fail"
    INTERRUPT = "stop"


class Task:
    def __init__(self, command: Command, task_status: TaskStatus = TaskStatus.ON_GOING):
        self._command = command
        self._task_status = task_status
        self.lock = threading.Lock()

    @property
    def task_status(self):
        with self.lock:
            return self._task_status

    @task_status.setter
    def task_status(self, status: TaskStatus):
        with self.lock:
            self._task_status = status

    @property
    def command(self):
        with self.lock:
            return self._command

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.command == other.command and self._task_status == other._task_status
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Tasks:
    def __init__(self):
        self._prev_tasks = {}
        self._ongoing_tasks = {}
        self._current_integrated_command = None
        self._future_tasks = {}
        self.lock = threading.RLock()

    @property
    def current_integrated_command(self):
        with self.lock:
            return self._current_integrated_command

    @current_integrated_command.setter
    def current_integrated_command(self, command: Optional[BaseCommandType]):
        with self.lock:
            if isinstance(command, IntegrationCommandType):
                self._current_integrated_command = command
            elif command is None:
                self._current_integrated_command = None

    @property
    def ongoing_tasks(self) -> dict:
        with self.lock:
            return self._ongoing_tasks

    def add_ongoing_task(self, task: Task):
        with self.lock:
            controller_type = task.command.recipient
            self.ongoing_tasks[controller_type] = task
            LogMessage.update_current_task(Tasks.show_dict(self.ongoing_tasks))

    @property
    def future_tasks(self) -> dict:
        with self.lock:
            return self._future_tasks

    def add_future_task(self, task: Task):
        with self.lock:
            controller_type = task.command.recipient
            self.future_tasks[controller_type] = task
            LogMessage.update_future_task(Tasks.show_dict(self.future_tasks))

    def clear_future_tasks(self):
        with self.lock:
            self.future_tasks.clear()

    @property
    def prev_tasks(self) -> dict:
        with self.lock:
            return self._prev_tasks

    def update_e_stop(self):
        with self.lock:
            self.clear_future_tasks()
            for (_, task) in self.ongoing_tasks.items():
                task.task_status = TaskStatus.FAIL
        LogMessage.update_future_task(self.future_tasks)

    def finish_task(self, controller_type: ClientType):
        with self.lock:
            task = self.ongoing_tasks.get(controller_type, None)
            task.task_status = TaskStatus.DONE
            self.modify_tasks(task, self.prev_tasks, self.ongoing_tasks)
        LogMessage.update_current_task(Tasks.show_dict(self.ongoing_tasks))
        LogMessage.update_prev_task(Tasks.show_dict(self.prev_tasks))

    def start_task(self, command: Command):
        # check if the task is in future task list
        with self.lock:
            task = self.future_tasks.get(command.recipient, None)
            if task is not None and task.command == command:
                self.start_existing_task(task)
                LogMessage.update_future_task(self.future_tasks)
            else:
                new_task = Task(command)
                self.start_new_task(new_task)
        LogMessage.update_current_task(Tasks.show_dict(self.ongoing_tasks))

    def start_new_task(self, task: Task):
        self.modify_tasks(task, self._ongoing_tasks)

    def start_existing_task(self, task: Task):
        task.task_status = TaskStatus.ON_GOING
        self.modify_tasks(task, self._ongoing_tasks, self._future_tasks)

    def modify_tasks(self, task: Task, tasks_to_add: dict, tasks_to_delete: dict = None):
        controller_type = task.command.recipient
        tasks_to_add[controller_type] = task
        if tasks_to_delete is not None:
            tasks_to_delete.pop(controller_type, None)

    @staticmethod
    def show_dict(tasks_dict: Dict[ClientType, Task]):
        tasks_dict = {key.name: value.command.command_type.name for (key, value) in tasks_dict.items()}
        return tasks_dict


