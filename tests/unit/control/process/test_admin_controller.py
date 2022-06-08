import pytest

from src.communication.client import Client, ClientType, ClientStatus
from src.control.exceptions.process_execptions import SendCommandStatusCheckFailException
from src.control.process.admin_controller import AdminController
from src.control.process.status_controller import StatusController
from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType, IntegrationCommandType
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
class TestAdminController:

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
    def test_receive_and_process_command_individual(self, recv_msg_list, expect_command_list, mocker):
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
    def test_send_and_verify_command_individual_success(self, input_command_list, expect_client_status_list, mocker):
        mocker.patch("src.control.process.admin_controller.AdminController.send_command", return_value=None)
        for input_command, expect_client_status in zip(input_command_list, expect_client_status_list):
            self.admin_controller.add_command_to_queue(input_command)
            recipient_type, expect_recipient_status = expect_client_status
            self.admin_controller.send_and_verify_command()
            assert self.admin_controller \
                       .status_controller.get_subsystem_status(recipient_type) == expect_recipient_status
            assert self.admin_controller.status_controller.current_integrated_command is None

    @pytest.mark.parametrize(
        "input_integrated_command_list, expect_client_status_list",
        [
            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)],
             [(ClientType.LEVEL, ClientStatus.BUSY)]),
        ],
    )
    def test_send_and_verify_command_integrated_success(self, input_integrated_command_list, expect_client_status_list, mocker):
        mocker.patch("src.control.process.admin_controller.AdminController.send_command", return_value=None)

    @pytest.mark.parametrize(
        "input_command_list, expect_client_status_list",
        [
            ([Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False),
              Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)],
             [(ClientType.LEVEL, ClientStatus.BUSY), (ClientType.LEVEL, None)]),

            ([Command(LevelCommandType.STOP, ClientType.LEVEL, "", False, True),
              Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)],
             [(ClientType.LEVEL, ClientStatus.LOCK), (ClientType.LEVEL, None)]),
        ],
    )
    def test_send_command_status_exception(self, input_command_list, expect_client_status_list, mocker):
        mocker.patch("src.control.process.admin_controller.AdminController.send_command", return_value=None)
        for input_command, expect_client_status in zip(input_command_list, expect_client_status_list):
            self.admin_controller.add_command_to_queue(input_command)
            recipient_type, expect_recipient_status = expect_client_status
            if expect_recipient_status is None:
                with pytest.raises(SendCommandStatusCheckFailException):
                    self.admin_controller.send_and_verify_command()
            else:
                self.admin_controller.send_and_verify_command()
