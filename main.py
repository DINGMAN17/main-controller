import logging
from datetime import datetime

from communication.control_server import ControlServer


def setup():
    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = "log/server_" + timestamp + ".log"
    logging.basicConfig(filename=filename, filemode='w', format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def run():
    setup()
    ControlServer(timeout=86400).run()


if __name__ == "__main__":
    run()
