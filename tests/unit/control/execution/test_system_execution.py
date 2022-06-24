import pytest

from src.communication.client import ClientType
from src.control.execution.system_execution import SystemExecution


@pytest.mark.parametrize(
    "input_id_msg, expect_client_type",
    [
        ("IDlevel", ClientType.LEVEL),
        ("IDmass", ClientType.MASS),
        ("IDadmin", ClientType.ADMIN),
        ("IDuser", ClientType.USER),
    ],
)
def test_create_client(mocker, input_id_msg, expect_client_type):
    system_execution = SystemExecution()
    mocker.patch("src.control.execution.system_execution.SystemExecution.get_id_message", return_value=input_id_msg)
    system_execution.create_client()
    output_client_type = system_execution.new_client.client_type
    assert output_client_type == expect_client_type


@pytest.mark.parametrize(
    "input_id_msgs, expect_client_types",
    [
        (["IDlevel"], [ClientType.LEVEL]),
        (["IDmass"], [ClientType.MASS]),
        (["IDadmin"], [ClientType.ADMIN]),
        (["IDuser"], [ClientType.USER]),
        (["IDlevel", "IDmass", "IDgyro", "IDadmin", "IDuser"],
         [ClientType.LEVEL, ClientType.MASS, ClientType.GYRO, ClientType.ADMIN, ClientType.USER]),
    ],
)
def test_identify_client(mocker, input_id_msgs, expect_client_types):
    system_execution = SystemExecution()
    for id_msg in input_id_msgs:
        mocker.patch("src.control.execution.system_execution.SystemExecution.get_id_message", return_value=id_msg)
        system_execution.identify_client()
    admin = system_execution.get_admin()
    sub_controllers = system_execution.get_controllers()
    users = system_execution.get_users()
    for expect_client_type in expect_client_types:
        if expect_client_type == ClientType.ADMIN:
            assert admin.client_type == expect_client_type
        elif expect_client_type == ClientType.USER:
            assert len(users) > 0
        else:
            assert expect_client_type in sub_controllers
