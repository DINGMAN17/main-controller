import pytest

from src.communication.client import ClientType
from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType, IntegrationCommandType
from src.message.command.command_executor import LevellingCommandExecutor, Command, MassCommandExecutor, \
    GyroCommandExecutor, IntegrationCommandExecutor


@pytest.mark.parametrize(
    "input_command_type, expect_command",
    [
        (LevelCommandType.LEVEL_ONCE,
         [Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, "Lcmd01L\n", True, False)]),
        (LevelCommandType.STOP, [Command(LevelCommandType.STOP, ClientType.LEVEL, "Lcmd01t\n", False, True)]),
        (LevelCommandType.BATTERY,
         [Command(LevelCommandType.BATTERY, ClientType.LEVEL, "Lbat\n", False, False)]),
    ],
)
def test_level_execute(input_command_type, expect_command):
    # test 3 types of command, busy command, stop command(require system to be locked), normal command
    level_executor = LevellingCommandExecutor()
    level_executor.command_type = input_command_type
    level_executor.execute()
    assert level_executor.command_to_send == expect_command


@pytest.mark.parametrize(
    "input_command_type, expect_command",
    [
        (MassCommandType.MOVE,
         [Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False)]),
        (MassCommandType.STOP, [Command(MassCommandType.STOP, ClientType.MASS, "Mass_stop\n", False, True)]),
        (MassCommandType.GET,
         [Command(MassCommandType.GET, ClientType.MASS, "Mass_getPos\n", False, False)]),
    ],
)
def test_mass_execute(input_command_type, expect_command):
    # test 3 types of command, busy command, stop command(require system to be locked), normal command
    mass_executor = MassCommandExecutor()
    mass_executor.command_type = input_command_type
    mass_executor.execute()
    assert mass_executor.command_to_send == expect_command


@pytest.mark.parametrize(
    "input_command_type, expect_command",
    [
        (GyroCommandType.AUTO_ON,
         [Command(GyroCommandType.AUTO_ON, ClientType.GYRO, "Gyro_AutoOn\n", True, False)]),
        (GyroCommandType.STOP, [Command(GyroCommandType.STOP, ClientType.GYRO, "Gyro_Stop\n", False, True)]),
        (GyroCommandType.GET,
         [Command(GyroCommandType.GET, ClientType.GYRO, "Gyro_GetYaw\n", False, False)]),
    ],
)
def test_gyro_execute(input_command_type, expect_command):
    # test 3 types of command, busy command, stop command(require system to be locked), normal command
    gyro_executor = GyroCommandExecutor()
    gyro_executor.command_type = input_command_type
    gyro_executor.execute()
    assert gyro_executor.command_to_send == expect_command


@pytest.mark.parametrize(
    "input_command_type, expect_command",
    [
        (IntegrationCommandType.MOVE_LEVEL,
         [Command(MassCommandType.MOVE, ClientType.MASS, "Mass_move\n", True, False),
          Command(LevelCommandType.LEVEL_AUTO, ClientType.LEVEL, "Lcmd01K\n", True, False)]),
    ],
)
def test_integrate_execute(input_command_type, expect_command):
    # test 3 types of command, busy command, stop command(require system to be locked), normal command
    integrate_executor = IntegrationCommandExecutor()
    integrate_executor.command_type = input_command_type
    integrate_executor.execute()
    assert integrate_executor.command_to_send == expect_command
