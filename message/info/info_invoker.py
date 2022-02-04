import logging

from communication.client import ClientType
from message.info.info_executor import *


class InfoInvoker:
    @staticmethod
    def invoke(message: str):
        # e.g. M-INFO-moved; L-INFO-BAT-4
        try:
            output_dict = dict()
            msg_components = message.split("-")
            client_type = ClientType(msg_components[0])
            if client_type == ClientType.MASS:
                info = MassInfoType(msg_components[2])
                output_dict = MassInfoExecutor.execute(info)
            elif client_type == ClientType.LEVEL:
                info = LevelInfoType(msg_components[2])
                output_dict = LevelInfoExecutor.execute(info, msg_components)
            elif client_type == ClientType.GYRO:
                info = GyroInfoType(msg_components[2])
                output_dict = GyroInfoExecutor.execute(info)
            return output_dict
        except ValueError as e:
            logging.exception("wrong info message %s", message)
