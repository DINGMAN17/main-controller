from datetime import datetime

from communication.control_server import ControlServer
from utils import setup_logger


def setup():
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename_data = "log/server_data_" + timestamp + ".log"
    filename_main = "log/server_main_" + timestamp + ".log"
    filename_err = "log/server_error_" + timestamp + ".log"
    filename_task = "log/server_task_" + timestamp + ".log"
    setup_logger("data", filename_data)
    setup_logger("main", filename_main)
    setup_logger("warning", filename_err)
    setup_logger("task", filename_task)


def run():
    setup()
    ControlServer(timeout=86400).run()


if __name__ == "__main__":
    run()

# TODO: fix gyro status update after execution
# TODO: remove UTF8 control characters from gyro message