import logging
import threading
from typing import Optional

from src.communication.client import ClientType
from src.message.command.command import IntegrationCommandType
from src.message.info.info import BaseInfoType, MassInfoType, LevelInfoType, GyroInfoType
from src.message.info.info_executor import LevelInfoExecutor, MassInfoExecutor, GyroInfoExecutor, IntegratedInfoExecutor


# TODO: resolve unknown info
class InfoInvoker:
    def __init__(self):
        self.level_executor = LevelInfoExecutor()
        self.mass_executor = MassInfoExecutor()
        self.gyro_executor = GyroInfoExecutor()
        self.integration_executor = IntegratedInfoExecutor()
        self._msg_components: Optional[list] = None
        self._info_type: Optional[BaseInfoType] = None
        self._integrated_command: Optional[IntegrationCommandType] = None
        self.output_dict = dict()
        self.lock = threading.Lock()

    @property
    def msg_components(self):
        return self._msg_components

    @msg_components.setter
    def msg_components(self, msg):
        self._msg_components = msg

    @property
    def integrated_command(self):
        return self._integrated_command

    @integrated_command.setter
    def integrated_command(self, command):
        self._integrated_command = command

    def get_output_status(self):
        return self.output_dict.get('status')

    def get_output_info(self):
        return self.output_dict.get('info_type')

    def get_output_command(self):
        return self.output_dict.get('command')

    def invoke(self):
        # e.g. M-INFO-moved; L-INFO-BAT-4
        try:
            client_type = ClientType(self.msg_components[0])
            self.get_info_type(client_type)
            if self._integrated_command is None:
                if client_type == ClientType.MASS:
                    self.process_info(self.mass_executor)
                elif client_type == ClientType.LEVEL:
                    self.process_info(self.level_executor)
                elif client_type == ClientType.GYRO:
                    self.process_info(self.gyro_executor)
            else:
                self.integration_executor.integrated_command = self._integrated_command
                self.process_info(self.integration_executor)
                self.update_integrated_command()
            return self.output_dict
        except ValueError as e:
            logging.exception("wrong info message %s", "-".join(self.msg_components))

    def process_info(self, executor):
        executor.reset(self._info_type, self._msg_components)
        self.output_dict = executor.execute()

    def update_integrated_command(self):
        # integrated operation done, clear command
        output_status = self.get_output_status()
        if (self._integrated_command is not None) and (output_status is not None):
            self._integrated_command = self.integration_executor.integrated_command = None

    def get_info_type(self, client_type):
        if client_type == ClientType.MASS:
            self._info_type = MassInfoType(self.msg_components[2])
        elif client_type == ClientType.LEVEL:
            self._info_type = LevelInfoType(self.msg_components[2])
        elif client_type == ClientType.GYRO:
            self._info_type = GyroInfoType(self.msg_components[2])
