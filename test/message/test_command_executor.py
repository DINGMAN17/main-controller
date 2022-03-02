from communication.client import ClientType
from hardware.winches import Winches
from message.command.command import LevelCommandType
from message.command.command_executor import LevellingCommandExecutor, Command


def test_create_command_success():
    command_to_send = LevellingCommandExecutor.execute(LevelCommandType.LEVEL_ONCE)
    correct_command = Command(LevelCommandType.LEVEL_ONCE, ClientType.LEVEL, Winches.level_once(), True)
    assert command_to_send == correct_command
