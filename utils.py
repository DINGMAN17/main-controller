import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class LogMessage:

    @staticmethod
    def start_server(address: tuple, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("SERVER Listening at (%s, %s), ready to accept clients", address[0], address[1])

    @staticmethod
    def new_unidentified_client(address: tuple, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("new client connected at (%s, %s), wait for identification", address[0], address[1])

    @staticmethod
    def add_client(client_name, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("%s is added", client_name)

    @staticmethod
    def wrong_client(log_name="warning"):
        log = logging.getLogger(log_name)
        err = "ERROR: wrong client type"
        log.exception(err)
        return err

    @staticmethod
    def disconnect(client_name=None, log_name="main"):
        log = logging.getLogger(log_name)
        if client_name is None:
            client_name = "Unidentified client"
        log.exception("%s is disconnected from server", client_name)

    @staticmethod
    def command_sent_fail(log_name="warning"):
        log = logging.getLogger(log_name)
        err_msg = "intended client is not connected"
        log.exception(err_msg)
        return err_msg

    @staticmethod
    def bad_request(data="", log_name="warning"):
        log = logging.getLogger(log_name)
        err = "ERROR: bad request/format" + data
        log.exception(err)
        return err

    @staticmethod
    def wrong_command(message, log_name="warning"):
        log = logging.getLogger(log_name)
        log.exception("wrong command %s", message)

    @staticmethod
    def send_command(command, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("command sent to {}: {}".format(command.recipient.name, command.command_type.name))

    @staticmethod
    def remove_user(log_name="main"):
        log = logging.getLogger(log_name)
        log.info("Connection warning while sending data to user, remove user from list")

    @staticmethod
    def send_to_user(data, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("sent to user-%s", data)

    @staticmethod
    def receive_data(data, log_name="data"):
        log = logging.getLogger(log_name)
        log.info("data-%s", data)

    @staticmethod
    def update_client_status(client, status, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("status of {} has been updated to: {}".format(client, status))

    @staticmethod
    def update_future_task(future_tasks, log_name="task"):
        log = logging.getLogger(log_name)
        log.info("future tasks: {}".format(future_tasks))

    @staticmethod
    def update_current_task(ongoing_tasks, log_name="task"):
        log = logging.getLogger(log_name)
        log.info("ongoing tasks: {}".format(ongoing_tasks))

    @staticmethod
    def update_prev_task(prev_tasks, log_name="task"):
        log = logging.getLogger(log_name)
        log.info("previous tasks: {}".format(prev_tasks))