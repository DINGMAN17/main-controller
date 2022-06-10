import pytest

from src.communication.client import ClientType, ClientStatus
from src.message.command.command import LevelCommandType, IntegrationCommandType
from src.message.info.info import AdminInfoType
from src.message.info.info_invoker import InfoInvoker


class TestInfoInvoker:
    @pytest.mark.parametrize(
        "input_info_msg, expect_results",
        [
            ("M-INFO-MOVED", (AdminInfoType.M_MOVE_DONE, [(ClientType.MASS, ClientStatus.READY)])),
            ("M-INFO-STOPPED", (AdminInfoType.M_STOP_DONE, [(ClientType.MASS, ClientStatus.READY)])),
            ("M-INFO-POSSET", (AdminInfoType.M_POS_DONE, [])),

            ("G-INFO-AUTOON", (AdminInfoType.G_AUTO_ON_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            ("G-INFO-STOPPED", (AdminInfoType.G_STOP_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            ("G-INFO-AUTOOFFSELECT", (AdminInfoType.G_AUTO_OFF_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            ("G-INFO-CENTERED", (AdminInfoType.G_CENTER_DONE, [(ClientType.GYRO, ClientStatus.READY)])),

            ("L-INFO-LevellingFinish", (AdminInfoType.L_LEVEL_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            ("L-INFO-Stopped", (AdminInfoType.L_STOP_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            ("L-INFO-AutoMoveFinish", (AdminInfoType.L_MOVE_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            ("L-INFO-InitFinish", (AdminInfoType.L_INIT_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            ("L-INFO-Bat-5", (AdminInfoType.L_BATTERY_ENOUGH, [])),
            ("L-INFO-Bat-3", (AdminInfoType.L_BATTERY_LOW, [])),
        ]
    )
    def test_info_invoke_1_controller(self, input_info_msg, expect_results):
        info_invoker = InfoInvoker()
        info_invoker.msg_components = input_info_msg.split("-")
        outputs = info_invoker.invoke()
        expect_output_info, expect_output_status = expect_results
        assert outputs['info_type'] == expect_output_info
        if expect_output_status:
            assert outputs['status'] == expect_output_status

    @pytest.mark.parametrize(
        "input_info_msg, expect_results",
        [
            ("M-INFO-MOVED", (AdminInfoType.I_MASS_MOVE_DONE, None, [LevelCommandType.STOP])),
            ("M-INFO-STOPPED", (AdminInfoType.I_MASS_STOP_DONE, None, [LevelCommandType.STOP])),
            ("L-INFO-Stopped", (AdminInfoType.I_KEEP_LEVEL_STOP_DONE, None, [LevelCommandType.LEVEL_ONCE])),
            ("L-INFO-LevellingFinish", (AdminInfoType.I_LEVEL_ONCE_DONE, [(ClientType.MASS, ClientStatus.READY),
                                                                          (ClientType.LEVEL, ClientStatus.READY)],
                                        None)),
        ]
    )
    def test_info_invoke_integrate_command(self, input_info_msg, expect_results):
        info_invoker = InfoInvoker()
        info_invoker.msg_components = input_info_msg.split("-")
        info_invoker.integrated_command = IntegrationCommandType.MOVE_LEVEL
        info_invoker.invoke()
        expect_info, expect_status, expect_command_list = expect_results
        assert info_invoker.get_output_info() == expect_info
        if info_invoker.get_output_status() is not None:
            assert info_invoker.get_output_status() == expect_status
            assert info_invoker.integrated_command is None
        if expect_command_list is not None:
            for output_cmd, expect_cmd_type in zip(info_invoker.get_output_command(), expect_command_list):
                assert output_cmd.command_type == expect_cmd_type
