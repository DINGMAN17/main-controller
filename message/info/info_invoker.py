import logging

from communication.client import ClientType
from message.info.info import *
from message.info.info_executor import MassInfoExecutor


class InfoInvoker:
    @staticmethod
    def invoke(message):
        # e.g. M-INFO-moved
        try:
            output_info = None
            output_command = None
            msg_components = message.split("-")
            client_type = ClientType(msg_components[0])
            if client_type == ClientType.MASS:
                info = MassInfoType(msg_components[-1])
                output_info, output_command = MassInfoExecutor.execute(info)
            elif client_type == ClientType.LEVEL:
                info = LevelInfoType(msg_components[-1])

            return output_info, output_command
        except ValueError as e:
            logging.exception("wrong info message %s", message)
