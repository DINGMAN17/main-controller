from datetime import datetime

from src.communication.control_server import ControlServer
from src.utils.logging import create_one_logger


# TODO: other setup to do?
def setup():
    setup_logger()


# TODO: put all the user define values in a separate file, e.g. filenames, socket address
def setup_logger():
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename_data = "docs/log/server_data_" + timestamp + ".log"
    filename_main = "docs/log/server_main_" + timestamp + ".log"
    filename_err = "docs/log/server_error_" + timestamp + ".log"
    filename_task = "docs/log/server_task_" + timestamp + ".log"
    filename_command = "docs/log/server_command_" + timestamp + ".log"
    create_one_logger("data", filename_data)
    create_one_logger("main", filename_main)
    create_one_logger("warning", filename_err)
    create_one_logger("task", filename_task)
    create_one_logger("command", filename_command)


def run():
    setup()
    ControlServer(socket_address=('127.0.0.1', 8080), timeout=86400).run() # 192.168.1.3


if __name__ == "__main__":
    run()