from communication.client import ClientType
from control.task_list import Task, TaskStatus, Tasks
from message.command.command import MassCommandType
from message.command.command_executor import Command

command1 = Command(MassCommandType.MOVE, ClientType.MASS, "", True)
command2 = Command(MassCommandType.STOP, ClientType.MASS, "", False)
task1 = Task(command1)
task2 = Task(command2)


def test_start_task_exist_success():
    task_list = Tasks()
    future_task = Task(command1, TaskStatus.WAIT)
    task_list.add_future_task(future_task)

    task_list.start_task(command1)
    future_tasks = task_list.future_tasks
    ongoing_tasks = task_list.ongoing_tasks
    assert future_tasks.get(ClientType.MASS, None) is None
    assert ongoing_tasks.get(ClientType.MASS) == Task(command1, TaskStatus.ON_GOING)


def test_start_task_new_no_future_task_success():
    task_list = Tasks()
    future_task = Task(command1, TaskStatus.WAIT)
    task_list.add_future_task(future_task)
    future_tasks = task_list.future_tasks
    ongoing_tasks = task_list.ongoing_tasks
    task_list.start_task(command2)
    assert future_tasks.get(ClientType.MASS, None) == future_task
    assert ongoing_tasks.get(ClientType.MASS) == Task(command2, TaskStatus.ON_GOING)


def test_start_task_new_with_future_task_success():
    task_list = Tasks()
    future_tasks = task_list.future_tasks
    assert future_tasks.get(ClientType.MASS, None) is None
    ongoing_tasks = task_list.ongoing_tasks
    task_list.start_task(command1)
    assert future_tasks.get(ClientType.MASS, None) is None
    assert ongoing_tasks.get(ClientType.MASS) == Task(command1, TaskStatus.ON_GOING)


def test_finish_task_success():
    task_list = Tasks()
    ongoing_tasks = task_list.ongoing_tasks
    prev_tasks = task_list.prev_tasks
    task_list.start_task(command1)
    assert prev_tasks.get(ClientType.MASS, None) is None
    assert ongoing_tasks.get(ClientType.MASS) == Task(command1, TaskStatus.ON_GOING)
    task_list.finish_task(ClientType.MASS)
    assert ongoing_tasks.get(ClientType.MASS, None) is None
    assert prev_tasks.get(ClientType.MASS) == Task(command1, TaskStatus.DONE)

# def test_task_equal_true():
#     assert task1 == task1
#
#
# def test_task_equal_status_false():
#     task1.task_status = TaskStatus.WAIT
#     task1_new = Task(command1)
#     assert task1 != task1_new
#
#
# def test_task_equal_command_false():
#     assert task1 != task2
