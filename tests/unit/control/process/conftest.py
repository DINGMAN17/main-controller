import pytest

from src.communication.client import ClientType, Client, ClientStatus
from src.control.process.admin_controller import AdminController
from src.control.process.status_controller import StatusController
from src.control.process.subsystem_controller import SubsystemController
from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType
from src.message.command.command_executor import Command


def create_client(client_type: ClientType, client_status: ClientStatus, name=None):
    client = Client(client_type=client_type, name=name, socket=None)
    client.status = client_status
    return client


def create_command(command_info: tuple):
    command_type, recipient, output, busy_command, lock_system = command_info
    return Command(command_type, recipient, output, busy_command, lock_system)


clients_to_add = ([(ClientType.LEVEL, ClientStatus.READY), (ClientType.GYRO, ClientStatus.BUSY)],
                  [(ClientType.MASS, ClientStatus.LOCK), (ClientType.GYRO, ClientStatus.BUSY)])

command_to_add = ((LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "", True, False),
                  (MassCommandType.SET, ClientType.MASS, "", True, False),
                  (GyroCommandType.STOP, ClientType.GYRO, "", False, True))

full_config_to_add = ([(ClientType.MASS, ClientStatus.READY), (ClientType.GYRO, ClientStatus.READY),
                       (ClientType.LEVEL, ClientStatus.READY), (ClientType.ADMIN, ClientStatus.READY)],)


@pytest.fixture(params=clients_to_add)
def controller_clients(request):
    return request.param


@pytest.fixture(params=command_to_add)
def controller_command(request):
    return request.param


@pytest.fixture(params=full_config_to_add)
def full_config(request):
    return request.param


@pytest.fixture()
def status_controller_with_all_clients(full_config, controller_command, request):
    # setup status controller with initial clients
    status_controller = StatusController()
    for client in full_config:
        new_client = create_client(client[0], client[1])
        if new_client.client_type == ClientType.ADMIN:
            status_controller.admin = new_client
        else:
            status_controller.add_controller_client(new_client)
    command = create_command(controller_command)
    request.cls.status_controller = status_controller
    request.cls.all_clients = full_config
    request.cls.command = command
    yield

    status_controller.controller_clients = {}
    status_controller.admin = None


@pytest.fixture()
def status_controller_with_controller_clients(controller_clients, request):
    # setup status controller with initial clients
    status_controller = StatusController()
    for client in controller_clients:
        new_client = create_client(client[0], client[1])
        status_controller.add_controller_client(new_client)
    request.cls.status_controller = status_controller
    request.cls.controller_clients = controller_clients
    yield

    status_controller.controller_clients = {}


@pytest.fixture()
def status_controller_with_command(controller_command, request):
    # setup status controller with initial clients
    status_controller = StatusController()
    command = create_command(controller_command)
    request.cls.status_controller = status_controller
    request.cls.command = command
    yield

    status_controller.controller_clients = {}


@pytest.fixture()
def admin_controller_setup(request, full_config):
    status_controller = StatusController()
    admin_controller = AdminController(status_controller)
    for client in full_config:
        new_client = create_client(client[0], client[1])
        if new_client.client_type == ClientType.ADMIN:
            admin_controller.status_controller.admin = new_client
        else:
            admin_controller.status_controller.add_controller_client(new_client)
    request.cls.admin_controller = admin_controller
    yield


@pytest.fixture()
def subsystem_controller_setup(request, full_config):
    status_controller = StatusController()
    subsystem_controller = SubsystemController(status_controller)
    for client in full_config:
        new_client = create_client(client[0], client[1])
        if new_client.client_type != ClientType.ADMIN:
            subsystem_controller.add_active_subsystem_client(new_client)
    request.cls.subsystem_controller = subsystem_controller
    yield
