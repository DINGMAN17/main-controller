from communication.client import ClientType
from control.task_list import Task, TaskStatus
from message.command.command import Command, MassCommandType

command1 = Command(MassCommandType.MOVE, ClientType.MASS)
command2 = Command(MassCommandType.STOP, ClientType.MASS)
task1 = Task(command1)
task2 = Task(command2)


def test_task_equal_true():
    assert task1 == task1


def test_task_equal_status_false():
    task1.set_task_status(TaskStatus.YET_TO_START)
    task1_new = Task(command1)
    assert task1 != task1_new


def test_task_equal_command_false():
    assert task1 != task2



