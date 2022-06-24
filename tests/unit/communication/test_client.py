import pytest

from src.communication.client import Client, ClientType
from src.control.exceptions.process_execptions import NotValidSubsystemException, UnknownClientException


@pytest.mark.parametrize(
    "input_id_msg, expect_client_type",
    [
        ("IDlevel", ClientType.LEVEL),
        ("IDl", ClientType.LEVEL),
        ("IDG", ClientType.GYRO),
        ("IDGYRO", ClientType.GYRO),
        ("IDMASS", ClientType.MASS),
        ("IDadmin", ClientType.ADMIN),
        ("IDuser", ClientType.USER),
    ],
)
def test_identify_client_success(input_id_msg, expect_client_type):
    assert Client.identify_client(input_id_msg) == expect_client_type
    assert ClientType.LEVEL.name in ClientType.__members__


def test_identify_client_invalid_subsystem_exception():
    invalid_client_msg = "IDY"
    with pytest.raises(NotValidSubsystemException):
        Client.identify_client(invalid_client_msg)


def test_identify_client_invalid_msg_exception():
    invalid_client_msg = "iidY"
    with pytest.raises(UnknownClientException):
        Client.identify_client(invalid_client_msg)
