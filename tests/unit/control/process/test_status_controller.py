import pytest

from src.communication.client import ClientType, ClientStatus
from src.control.exceptions.process_execptions import IntendedClientDoesNotExistException, \
    IntendedClientIsNotConnectedException


@pytest.mark.usefixtures("status_controller_with_controller_clients")
class TestSubsystemStatus:
    def test_get_subsystem_status_success(self):
        for client_info in self.controller_clients:
            client_type, expect_client_status = client_info
            result = self.status_controller.get_subsystem_status(client_type)
            assert result == expect_client_status

    def test_get_subsystem_status_not_exist_exception(self):
        if ClientType.MASS not in self.status_controller.controller_clients.keys():
            with pytest.raises(IntendedClientDoesNotExistException):
                self.status_controller.get_subsystem_status(ClientType.MASS)

    def test_get_subsystem_status_not_connected_exception(self):
        for client_info in self.controller_clients:
            client_type = client_info[0]
            self.status_controller.update_subsystem_connection_state(connection_state=False, subsystem_type=client_type)
            with pytest.raises(IntendedClientIsNotConnectedException):
                self.status_controller.get_subsystem_status(client_type)


@pytest.mark.usefixtures("status_controller_with_command")
class TestUpdateRecipientStatus:
    def test_update_recipient_status_after_sending_command(self, mocker):
        mocker.patch("src.control.process.status_controller.StatusController.update_and_add_status",
                     return_value=None)
        update_status, new_status = self.status_controller.update_recipient_status_after_sending_command(self.command)
        if self.command.busy_command:
            expect_update_status, expect_new_status = True, ClientStatus.BUSY
        elif self.command.lock_system:
            expect_update_status, expect_new_status = True, ClientStatus.LOCK
        else:
            expect_update_status, expect_new_status = False, None
        assert update_status == expect_update_status
        assert new_status == expect_new_status


@pytest.mark.usefixtures("status_controller_with_all_clients")
class TestWithAdmin:
    def test_update_recipient_status_after_sending_command(self, mocker):
        log = mocker.patch("src.utils.logging.LogMessage", autospec=True)
        log.update_client_status.return_value = None
        _, new_status = self.status_controller.update_recipient_status_after_sending_command(self.command)
        if new_status is not None:
            # check whether the sub_controller status has been updated
            assert new_status == self.status_controller.controller_clients[self.command.recipient].status
            # check the status update is in the queue
            status_msg = self.status_controller.status_queue.get()
            assert new_status.name.lower() in status_msg
