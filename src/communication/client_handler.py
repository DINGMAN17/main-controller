from src.control.execution.system_execution import SystemExecution


class ClientHandler:

    def __init__(self):
        self.execution = SystemExecution()

    def run(self, client_socket):
        new_client = self.execution.identify_client(client_socket)
        self.execution.activate_process(new_client)
