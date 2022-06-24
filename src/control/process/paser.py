from src.communication.client import ClientType, ClientStatus


class Paser:
    @staticmethod
    def parse_status_msg_send(recipient: ClientType, status: ClientStatus) -> str:
        return '{recipient}-STATUS-{status}\n'.format(recipient=recipient.value, status=status.name.lower())

    @staticmethod
    def parse_status_msg_recv(status_msg: str) -> (ClientType, ClientStatus):
        msg_components = status_msg.split("-")
        client_type = ClientType(msg_components[0])
        client_status = ClientStatus(msg_components[-1].lower())
        return client_type, client_status

