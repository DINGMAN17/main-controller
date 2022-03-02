import logging
import threading

from message.info.info_executor import *


class InfoInvoker:
    def __init__(self, ):
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

    def invoke(self):
        # e.g. M-INFO-moved; L-INFO-BAT-4
        try:
            with self.lock:
                client_type = ClientType(self.msg_components[0])
                self.get_info_type(client_type)
                if self._integrated_command is None:
                    if client_type == ClientType.MASS:
                        self.output_dict = MassInfoExecutor.execute(self._info_type)
                    elif client_type == ClientType.LEVEL:
                        self.output_dict = LevelInfoExecutor.execute(self._info_type)
                    elif client_type == ClientType.GYRO:
                        self.output_dict = GyroInfoExecutor.execute(self._info_type)
                else:
                    self.output_dict = IntegratedInfoExecutor.execute(self._info_type, self._integrated_command)
                    self.update_integrated_command()
                return self.output_dict
        except ValueError as e:
            logging.exception("wrong info message %s", "-".join(self.msg_components))

    def update_integrated_command(self):
        # integrated operation done, clear command
        if self.output_dict.get("status", None) is not None:
            self.integrated_command = None

    def get_info_type(self, client_type):
        if client_type == ClientType.MASS:
            self._info_type = MassInfoType(self.msg_components[2])
        elif client_type == ClientType.LEVEL:
            self._info_type = LevelInfoType(self.msg_components[2])
        elif client_type == ClientType.GYRO:
            self._info_type = GyroInfoType(self.msg_components[2])
