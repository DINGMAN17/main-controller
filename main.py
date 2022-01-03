import logging

from communication.control_server import ControlServer


def setup():
    logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def run():
    setup()
    ControlServer(timeout=86400).run()


if __name__ == "__main__":
    run()
