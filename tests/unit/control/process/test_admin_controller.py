import pytest

from src.communication.client import Client, ClientType, ClientStatus
from src.control.exceptions.process_execptions import SendCommandStatusCheckFailException
from src.control.process.admin_controller import AdminController
from src.control.process.status_controller import StatusController
from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType
from src.message.command.command_executor import Command


@pytest.mark.parametrize("input_users",
                         [[Client(ClientType.USER, "user_1", None)],
                          [Client(ClientType.ADMIN, "admin_1", None)],
                          [Client(ClientType.USER, "user_1", None), Client(ClientType.USER, "user_2", None)],
                          [Client(ClientType.ADMIN, "admin_1", None), Client(ClientType.ADMIN, "admin_2", None)],
                          [Client(ClientType.USER, "user_1", None), Client(ClientType.USER, "user_2", None),
                           Client(ClientType.ADMIN, "admin_1", None)]])
def test_add_admin_or_user_one_admin(input_users):
    # test cases: 1 user, 1 admin, multiple users, multiple admins, multiple users & 1 admin
    status_controller = StatusController()
    admin_controller = AdminController(status_controller)
    admin = None
    for user in input_users:
        admin_controller.add_admin_or_user(user)
        if user.client_type == ClientType.ADMIN:
            admin = user
    if admin is not None:
        assert admin.name == status_controller.admin.name
    assert status_controller.users == input_users


@pytest.mark.usefixtures("admin_controller_setup")
class TestAdminControllerSuccess:

    @pytest.mark.parametrize(
        "recv_msg_list, expect_command_list",
        [
            (["A-C-L-once"], [Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)]),
            (["A-C-M-set-X100,Y200"],
             [Command(MassCommandType.SET, ClientType.MASS, "Mass_setPos_X100Y200\n", False, False)]),
            (["A-C-M-set-X100,Y200", "A-C-M-move"],
             [Command(MassCommandType.SET, ClientType.MASS, "Mass_setPos_X100Y200\n", False, False),
              Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)]),
            (["A-C-L-stop", "A-C-L-battery"],
             [Command(LevelCommandType.STOP, ClientType.LEVEL, "Lcmd01t\n", False, True),
              Command(LevelCommandType.BATTERY, ClientType.LEVEL, "Lbat\n", False, False)]),

            (["A-C-I-move_level"],
             [Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False),
              Command(LevelCommandType.LEVEL_AUTO, ClientType.LEVEL, "Lcmd01K\n", True, False)],
             ),
        ],
    )
    def test_receive_and_process_command(self, recv_msg_list, expect_command_list, mocker):
        mocker.patch("src.control.process.admin_controller.AdminController.receive_command", return_value=recv_msg_list)
        self.admin_controller.receive_and_process_command()
        for expect_command in expect_command_list:
            input_command = self.admin_controller.get_command_from_queue()
            assert input_command == expect_command

    @pytest.mark.parametrize(
        "input_command_list, expect_client_status_list",
        [
            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)],
             [(ClientType.LEVEL, ClientStatus.BUSY)]),

            ([Command(MassCommandType.SET, ClientType.MASS, "Mass_setPos_X100Y200\n", False, False),
              Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)],
             [(ClientType.MASS, ClientStatus.READY), (ClientType.MASS, ClientStatus.BUSY)]),

            ([Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False),
              Command(MassCommandType.SET, ClientType.MASS, "Mass_setPos_X100Y200\n", False, False)],
             [(ClientType.MASS, ClientStatus.BUSY), (ClientType.MASS, ClientStatus.BUSY)]),

            ([Command(GyroCommandType.STOP, ClientType.GYRO, "Gyro_Stop\n", False, True)],
             [(ClientType.GYRO, ClientStatus.LOCK)]),

            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False),
              Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)],
             [(ClientType.LEVEL, ClientStatus.BUSY), (ClientType.MASS, ClientStatus.BUSY)]),
        ],
    )
    def test_send_command_and_update_individual(self, input_command_list, expect_client_status_list, mocker):
        mocker.patch("src.control.process.admin_controller.AdminController.send_command", return_value=None)
        for input_command, expect_client_status in zip(input_command_list, expect_client_status_list):
            self.admin_controller.add_command_to_queue(input_command)
            self.admin_controller.latest_input_command_type = input_command.command_type
            recipient_type, expect_recipient_status = expect_client_status
            self.admin_controller.send_command_and_update()
            assert self.admin_controller \
                       .status_controller.get_subsystem_status(recipient_type) == expect_recipient_status
            assert self.admin_controller.status_controller.current_integrated_command is None


@pytest.mark.usefixtures("admin_controller_setup_busy_client")
class TestAdminControllerFail:
    @pytest.mark.parametrize(
        "command_list",
        [
            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)]),

            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False),
              Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)]),
        ],
    )
    def test_add_and_verify_command_to_queue_exception(self, command_list):
        with pytest.raises(SendCommandStatusCheckFailException):
            self.admin_controller.add_and_verify_command_to_queue(command_list)
