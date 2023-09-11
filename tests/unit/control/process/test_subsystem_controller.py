import pytest

from src.communication.client import ClientType
from src.message.command.command import LevelCommandType, IntegrationCommandType
from src.message.info.info import AdminInfoType


@pytest.mark.usefixtures("subsystem_controller_setup")
class TestSubsystemController:
    @pytest.mark.parametrize(
        "input_client_type, expect_message",
        [
            (ClientType.LEVEL, "Lsensor\n"),
            (ClientType.GYRO, "Gyro_GetYaw\n"),
            (ClientType.MASS, "Mass_getPos\n"),
        ],
    )
    def test_get_data(self, input_client_type, expect_message):
        output_msg = self.subsystem_controller.get_data(input_client_type)
        assert output_msg == expect_message

    @pytest.mark.parametrize(
        "input_info_msg, expect_results",
        [
            ("M-INFO-MOVED", (AdminInfoType.M_MOVE_DONE.value, "M-STATUS-ready")),
            ("M-INFO-STOPPED", (AdminInfoType.M_STOP_DONE.value, "M-STATUS-ready")),
            ("M-INFO-POSSET", (AdminInfoType.M_POS_DONE.value, None)),

            ("G-INFO-AUTOON", (AdminInfoType.G_AUTO_ON_DONE.value, "G-STATUS-ready")),
            ("G-INFO-STOPPED", (AdminInfoType.G_STOP_DONE.value, "G-STATUS-ready")),
            ("G-INFO-AUTOOFFSELECT", (AdminInfoType.G_AUTO_OFF_DONE.value, "G-STATUS-ready")),
            ("G-INFO-CENTERED", (AdminInfoType.G_CENTER_DONE.value, "G-STATUS-ready")),

            ("L-INFO-LevellingFinish", (AdminInfoType.L_LEVEL_DONE.value, "L-STATUS-ready")),
            ("L-INFO-Stopped", (AdminInfoType.L_STOP_DONE.value, "L-STATUS-ready")),
            ("L-INFO-AutoMoveFinish", (AdminInfoType.L_MOVE_DONE.value, "L-STATUS-ready")),
            ("L-INFO-InitFinish", (AdminInfoType.L_INIT_DONE.value, "L-STATUS-ready")),
            ("L-INFO-Bat-5", ("A-INFO-levellingAutoMove inclinometer has enough battery:5\n", None)),
            ("L-INFO-Bat-3", ("A-INFO-please charge battery, levellingAutoMove inclinometer has low battery:3\n", None)),
        ],
    )
    def test_process_subsystem_message_single_info(self, input_info_msg, expect_results):
        self.subsystem_controller.process_info(input_info_msg.split("-"))
        output_info_msg = self.subsystem_controller.get_latest_info_update()
        output_status_msg = self.subsystem_controller.get_latest_status_update()
        assert output_info_msg == expect_results[0]
        if output_status_msg is not None:
            assert output_status_msg == expect_results[1]

    @pytest.mark.parametrize(
        "input_info_msg, expect_results",
        [
            ("M-INFO-MOVED", (AdminInfoType.I_MASS_MOVE_DONE.value, None, LevelCommandType.STOP)),
            ("M-INFO-STOPPED", (AdminInfoType.I_MASS_STOP_DONE.value, None, LevelCommandType.STOP)),
            ("L-INFO-Stopped", (AdminInfoType.I_KEEP_LEVEL_STOP_DONE.value, None, LevelCommandType.LEVEL_ONCE)),
            ("L-INFO-LevellingFinish", (AdminInfoType.I_LEVEL_ONCE_DONE.value, ["M-STATUS-ready", "L-STATUS-ready"],
                                        None)),
        ]
    )
    def test_process_subsystem_message_integrated_info(self, input_info_msg, expect_results):
        self.subsystem_controller.system_controller.current_integrated_command = IntegrationCommandType.MOVE_LEVEL
        self.subsystem_controller.update_incoming_integrated_command()
        self.subsystem_controller.process_info(input_info_msg.split("-"))
        output_info_msg = self.subsystem_controller.get_latest_info_update()
        output_command = self.subsystem_controller.get_latest_system_command()
        output_status = self.subsystem_controller.get_latest_status_update()
        expect_info, expect_status, expect_command_type = expect_results
        assert output_info_msg == expect_info
        if output_status is not None:
            status_list = []
            while output_status is not None:
                status_list.append(output_status)
                output_status = self.subsystem_controller.get_latest_status_update()
            assert status_list == expect_status
        if output_command is not None:
            assert output_command.command_type == expect_command_type
