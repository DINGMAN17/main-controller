from enum import Enum
from typing import Optional

from src.communication.client import ClientType, ClientStatus
from src.control.process.system_controller import SystemController


class SystemStatus(Enum):
    """
        An Enum of status of the intelligent system.

        Attributes:
        INITIALIZING: The system is going through the process of starting up.
        CHECKING: The system is going through a safety check for the sub-systems
        RUNNING: The system is functioning as intended and is performing the tasks it was designed for.
        FAILED: The system has experienced a critical error and is not functioning as intended.
        SAFE MODE: The system is reduced to limited functions, only safety features and stop command are allowed
        EMERGSTOPPED: The system is stopped due to an emergency.
    """
    INITIALIZING = "initializing"
    CHECKING = "checking"
    RUNNING = "running"
    FAILED = "failed"
    SAFEMODE = "safe mode"
    EMERGSTOPPED = "emergency stop"


class IntegratedStatusController:
    def __init__(self, system_controller: SystemController):
        self.system_controller: SystemController = system_controller
        self._system_status: Optional[SystemStatus] = None
        self._system_error = None

    @property
    def system_status(self):
        return self._system_status

    @system_status.setter
    def system_status(self, new_status: SystemStatus):
        self._system_status = new_status

    @property
    def system_error(self):
        return self._system_error

    @system_error.setter
    def system_error(self, new_error):
        self._system_error = new_error

    def check_system_status(self, required_status: SystemStatus) -> bool:
        return self.system_status == required_status

    def check_subsystem_status(self, subsystem: ClientType, required_status: ClientStatus) -> bool:
        current_subsystem_status = self.system_controller.get_subsystem_status(subsystem)
        return current_subsystem_status == required_status



