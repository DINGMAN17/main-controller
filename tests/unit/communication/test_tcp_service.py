import pytest

from src.communication.tcp_service import TcpService


@pytest.mark.parametrize(
    "recv_msg, expect_msg",
    [
        ("A-C-L-LEVELONCE\nA-C-L-BATTERY", ["A-C-L-LEVELONCE", "A-C-L-BATTERY"]),
        ("   A-C-L-LEVELONCE\n  A-C-L-BATTERY ", ["A-C-L-LEVELONCE", "A-C-L-BATTERY"]),
        ("A-C-L-LEVELONCE\n  ", ["A-C-L-LEVELONCE"])
    ],
)
def test_receive_message(recv_msg, expect_msg, mocker):
    mock_socket = mocker.patch("src.communication.tcp_service.TcpService.socket")
    mock_socket.recv.return_value = recv_msg.encode()
    result = TcpService().receive_message()
    assert result == expect_msg
