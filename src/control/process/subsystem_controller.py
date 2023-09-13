import queue
import threading
import time

from src.communication.client import ClientType, Client, ClientStatus
from src.control.exceptions.network_exceptions import ClientDisconnectException
from src.control.exceptions.process_execptions import NotValidSubsystemException
from src.control.process.paser import Paser
from src.control.process.status_controller import StatusController
from src.hardware.sensors import Vision
from src.message.command.command_executor import MassCommandExecutor, GyroCommandExecutor, LevellingCommandExecutor
from src.message.error.error import NetworkErrorType
from src.message.info.info_invoker import InfoInvoker
from src.message.message import BaseMessageType
from src.utils.logging import LogMessage


class SubsystemController:
    def __init__(self, status_controller: StatusController):
        self.data_queue = queue.Queue()
        self.debug_queue = queue.Queue()
        self.info_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.system_command_queue = queue.Queue()
        self.status_controller = status_controller
        self._lock = threading.Lock()

        self.info_invoker = InfoInvoker()

    def get_latest_info_update(self):
        return self.info_queue.get()

    def get_latest_status_update(self):
        return self.status_controller.get_status_from_queue()

    def get_latest_system_command(self):
        with self._lock:
            if not self.system_command_queue.empty():
                return self.system_command_queue.get()

    def clear_queue(self, queue_type: str = "data"):
        if queue_type == "data":
            queue_type = [self.data_queue]
        elif queue_type == "info":
            queue_type = [self.info_queue]
        elif queue_type == "debug":
            queue_type = [self.debug_queue]
        elif queue_type == "all":
            queue_type = [self.info_queue, self.debug_queue, self.data_queue]
        for queue_to_clear in queue_type:
            with queue_to_clear.mutex:
                queue_to_clear.queue.clear()

    def add_active_subsystem_client(self, client):
        if client.client_type in [ClientType.LEVEL, ClientType.GYRO, ClientType.MASS, ClientType.VISION]:
            self.status_controller.controller_clients[client.client_type] = client
        else:
            raise NotValidSubsystemException()

    def execute_subsystem(self, new_client):
        threading.Thread(target=self.request_data_thread, args=(new_client,)).start()
        threading.Thread(target=self.receive_message_thread, args=(new_client,)).start()

    def request_data_thread(self, client: Client, interval=0.5):
        while client.connected:
            try:
                command = self.get_data(client.client_type)
                if command:
                    client.tcp_service.send_message(command)
                time.sleep(interval)
            except ClientDisconnectException:
                self.handle_subsystem_disconnect(client.client_type)
                break

    def get_data(self, client_type):
        command = None
        if client_type == ClientType.MASS:
            command = MassCommandExecutor.get_position()
        elif client_type == ClientType.GYRO:
            command = GyroCommandExecutor.get_data()
        elif client_type == ClientType.LEVEL:
            command = LevellingCommandExecutor.request_data()
        elif client_type == ClientType.VISION:
            status = self.status_controller.get_subsystem_status(client_type)
            if status == ClientStatus.READY:
                command = Vision.get_measurement()
        return command

    def send_system_command(self, system_cmd):
        recipient = self.status_controller.get_subsystem_client(system_cmd.recipient)
        recipient.tcp_service.send_message(system_cmd.value)
        LogMessage.send_command(system_cmd)

    def receive_message_thread(self, client: Client):
        while client.connected:
            try:
                self.receive_process_message(client)
            except ClientDisconnectException:
                print('subsystem disconnected')

    def receive_process_message(self, client):
        valid_msg_list = client.tcp_service.receive_message()
        [self.process_subsystem_message(msg) for msg in valid_msg_list]

    def process_subsystem_message(self, message: str):
        # e.g. M-INFO-moved
        try:
            message_components = message.split("-")
            msg_type = BaseMessageType(message_components[1])
            if msg_type == BaseMessageType.DATA:
                print(message)
                self.data_queue.put(message + "\n")
            elif msg_type == BaseMessageType.INFO:
                self.process_info(message_components)
            elif msg_type == BaseMessageType.STATUS:
                print(message)
                client_type, client_status = Paser.parse_status_msg_recv(message)
                self.update_status(client_type, client_status)
            elif msg_type == BaseMessageType.DEBUG:
                msg = message + "\n"
                self.debug_queue.put(msg)
        except ValueError as e:
            print(e)

    def process_info(self, msg_components: list):
        try:
            self.info_invoker.msg_components = msg_components
            self.update_incoming_integrated_command()
            output_dict = self.info_invoker.invoke()
            self.update_outgoing_integrated_command()
            output_type, output_msg, output_command, output_status_list = (output_dict.get(key) for key in
                                                                           ["info_type", "info_msg", "command",
                                                                            "status"])
            if output_type is not None:
                # self.update_on_going_task(output_info)
                if output_msg is not None:
                    self.info_queue.put(output_msg)
                else:
                    self.info_queue.put(output_type.value)
            if output_command is not None:
                self.update_system_command(output_command)
            if output_status_list is not None:
                for client_type, client_status in output_status_list:
                    self.update_status(client_type, client_status)
        except (AttributeError, ValueError) as e:
            info_not_classified = "-".join(msg_components) + "\n"
            self.info_queue.put(info_not_classified)

    def update_outgoing_integrated_command(self):
        self.status_controller.current_integrated_command = self.info_invoker.integrated_command

    def update_incoming_integrated_command(self):
        self.info_invoker.integrated_command = self.status_controller.current_integrated_command

    def update_status(self, client_type, client_status):
        self.status_controller.update_and_add_status(client_type, client_status)

    def update_system_command(self, output_command: list):
        for cmd in output_command:
            self.send_system_command(cmd)
            self.system_command_queue.put(cmd)

    def get_update_from_subcontroller(self) -> list:
        update_list = [msg_queue.get() for msg_queue in
                     [self.info_queue, self.error_queue, self.data_queue, self.debug_queue, self.status_controller.status_queue] if
                     not msg_queue.empty()]
        return update_list

    def handle_subsystem_disconnect(self, client_type: ClientType):
        error = self.get_error_type(client_type)
        self.status_controller.system_error = error
        self.error_queue.put(error.value)

    def get_error_type(self, client_type):
        error_type = None
        if client_type == ClientType.GYRO:
            error_type = NetworkErrorType.GYRO_DISCONNECT
        elif client_type == ClientType.MASS:
            error_type = NetworkErrorType.MASS_DISCONNECT
        elif client_type == ClientType.LEVEL:
            error_type = NetworkErrorType.LEVEL_DISCONNECT
        elif client_type == ClientType.VISION:
            error_type = NetworkErrorType.VISION_DISCONNECT
        return error_type
