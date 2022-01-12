import logging


class LogMessage:
    @staticmethod
    def add_client(client_name):
        logging.info("%s is added", client_name)

    @staticmethod
    def wrong_client():
        err = "ERROR: wrong client type"
        logging.exception(err)
        return err

    @staticmethod
    def disconnect(client_name=None):
        if client_name is None:
            client_name = "Unidentified client"
        logging.exception("%s is disconnected from server", client_name)

    @staticmethod
    def bad_request(data=""):
        err = "ERROR: bad request/format" + data
        logging.exception(err)
        return err

    @staticmethod
    def send_command(command):
        logging.info("command sent to sub-controller: %s", command)

    @staticmethod
    def remove_user():
        logging.info("Connection error while sending data to user, remove user from list")

    @staticmethod
    def send_to_user(data):
        logging.info("sent to user-%s", data)

    @staticmethod
    def receive_data(data):
        logging.info("sensor data-%s", data)