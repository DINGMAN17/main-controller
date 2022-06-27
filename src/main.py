from datetime import datetime

from src.communication.control_server import ControlServer
from src.utils.logging import setup_logger


def setup():
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename_data = "docs/log/server_data_" + timestamp + ".log"
    filename_main = "docs/log/server_main_" + timestamp + ".log"
    filename_err = "docs/log/server_error_" + timestamp + ".log"
    filename_task = "docs/log/server_task_" + timestamp + ".log"
    filename_command = "docs/log/server_command_" + timestamp + ".log"
    setup_logger("data", filename_data)
    setup_logger("main", filename_main)
    setup_logger("warning", filename_err)
    setup_logger("task", filename_task)
    setup_logger("command", filename_command)


def run():
    setup()
    ControlServer(socket_address=('172.23.9.252', 8080), timeout=86400).run()


if __name__ == "__main__":
    run()
