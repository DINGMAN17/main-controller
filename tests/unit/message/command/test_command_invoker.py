import pytest

from src.communication.client import ClientType
from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType
from src.message.command.command_executor import Command
from src.message.command.command_invoker import CommandInvoker


@pytest.mark.parametrize(
    "input_command_msg, expect_command",
    [
        ("A-C-L-once",
         [Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)]),
        ("A-C-L-stop",
         [Command(LevelCommandType.STOP, ClientType.LEVEL, "Lcmd01t\n", False, True)]),
        ("A-C-L-up_a-10",
         [Command(LevelCommandType.UP_AUTO, ClientType.LEVEL, "Lcmd06AW0049\n", True, False)]),
        ("A-C-L-battery",
         [Command(LevelCommandType.BATTERY, ClientType.LEVEL, "Lbat\n", False, False)]),
        ("A-C-M-set-X100,Y200",
         [Command(MassCommandType.SET, ClientType.MASS, "Mass_setPos_X100Y200\n", False, False)]),
        ("A-C-M-move",
         [Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)]),
        ("A-C-M-stop",
         [Command(MassCommandType.STOP, ClientType.MASS, "Mass_stop\n", False, True)]),
        ("A-C-G-stop",
         [Command(GyroCommandType.STOP, ClientType.GYRO, "Gyro_Stop\n", False, True)]),
        ("A-C-G-auto_on",
         [Command(GyroCommandType.AUTO_ON, ClientType.GYRO, "Gyro_AutoOn\n", True, False)]),
        ("A-C-G-auto_off",
         [Command(GyroCommandType.AUTO_OFF, ClientType.GYRO, "Gyro_AutoOff\n", True, False)]),

        ("A-C-I-move_level",
         [Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False),
          Command(LevelCommandType.LEVEL_AUTO, ClientType.LEVEL, "Lcmd01K\n", True, False)]),
    ],
)
def test_command_invoker_invoke_individual_success(input_command_msg, expect_command):
    # test 3 types of command, busy command, stop command(require system to be locked), normal command
    command_invoker = CommandInvoker()
    command_invoker.msg_components = input_command_msg
    command_invoker.invoke()
    commands_list = command_invoker.commands_to_send
    assert commands_list == expect_command
