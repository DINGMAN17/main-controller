from control.system_execution import SystemExecution


class ClientHandler:

    def __init__(self):
        self.execution = SystemExecution()

    def run(self, client_socket):
        self.execution.identify_client(client_socket)
        self.execution.start_client()