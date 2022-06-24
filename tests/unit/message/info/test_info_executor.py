import pytest

from src.communication.client import ClientStatus, ClientType
from src.message.command.command import IntegrationCommandType, LevelCommandType
from src.message.info.info import AdminInfoType, MassInfoType, LevelInfoType, GyroInfoType
from src.message.info.info_executor import MassInfoExecutor, LevelInfoExecutor, GyroInfoExecutor, IntegratedInfoExecutor


class TestMassInfoExecutor:
    @pytest.mark.parametrize(
        "input_info_type, expect_results",
        [
            (MassInfoType.MOVE_DONE, (AdminInfoType.M_MOVE_DONE, [(ClientType.MASS, ClientStatus.READY)])),
            (MassInfoType.STOP_DONE, (AdminInfoType.M_STOP_DONE, [(ClientType.MASS, ClientStatus.READY)])),
            (MassInfoType.SET_DONE, (AdminInfoType.M_POS_DONE, [])),
        ]
    )
    def test_mass_info_execute(self, input_info_type, expect_results):
        mass_executor = MassInfoExecutor()
        mass_executor.reset(input_info_type)
        output_results = mass_executor.execute()
        expect_output_info, expect_output_status = expect_results
        assert output_results['info_type'] == expect_output_info
        if expect_output_status:
            assert output_results['status'] == expect_output_status


class TestLevelInfoExecutor:
    @pytest.mark.parametrize(
        "input_info_type, expect_results",
        [
            (LevelInfoType.LEVEL_DONE, (AdminInfoType.L_LEVEL_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            (LevelInfoType.STOP_DONE, (AdminInfoType.L_STOP_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            (LevelInfoType.AUTO_MOVE_DONE, (AdminInfoType.L_MOVE_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),
            (LevelInfoType.INIT_DONE, (AdminInfoType.L_INIT_DONE, [(ClientType.LEVEL, ClientStatus.READY)])),

        ],
    )
    def test_execute(self, input_info_type, expect_results):
        level_executor = LevelInfoExecutor()
        level_executor.reset(input_info_type)
        output_results = level_executor.execute()
        expect_output_info, expect_output_status = expect_results
        assert output_results['info_type'] == expect_output_info
        assert output_results['status'] == expect_output_status

    @pytest.mark.parametrize(
        "input_info_msg, expect_info_type",
        [
            ("L-INFO-Bat-5", AdminInfoType.L_BATTERY_ENOUGH),
            ("L-INFO-Bat-3", AdminInfoType.L_BATTERY_LOW),
        ],
    )
    def test_execute_battery(self, input_info_msg, expect_info_type):
        msg_components = input_info_msg.split("-")
        level_executor = LevelInfoExecutor()
        level_executor.reset(LevelInfoType.BATTERY, msg_components)
        output_results = level_executor.execute()
        assert output_results['info_type'] == expect_info_type
        assert output_results['info_msg'] == expect_info_type.value.strip() + msg_components[-1] + "\n"


class TestGyroInfoExecutor:
    @pytest.mark.parametrize(
        "input_info_type, expect_results",
        [
            (GyroInfoType.AUTO_ON_DONE, (AdminInfoType.G_AUTO_ON_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            (GyroInfoType.STOP_DONE, (AdminInfoType.G_STOP_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            (GyroInfoType.AUTO_OFF_DONE, (AdminInfoType.G_AUTO_OFF_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
            (GyroInfoType.CENTER_DONE, (AdminInfoType.G_CENTER_DONE, [(ClientType.GYRO, ClientStatus.READY)])),
        ],
    )
    def test_executor(self, input_info_type, expect_results):
        gyro_executor = GyroInfoExecutor()
        gyro_executor.reset(input_info_type)
        output_results = gyro_executor.execute()
        expect_output_info, expect_output_status = expect_results
        assert output_results['info_type'] == expect_output_info
        assert output_results['status'] == expect_output_status


class TestIntegratedInfoExecutor:
    @pytest.mark.parametrize(
        "input_info_type, expect_results",
        [
            (MassInfoType.MOVE_DONE, (AdminInfoType.I_MASS_MOVE_DONE, None, [LevelCommandType.STOP])),
            (MassInfoType.STOP_DONE, (AdminInfoType.I_MASS_STOP_DONE, None, [LevelCommandType.STOP])),
            (LevelInfoType.STOP_DONE, (AdminInfoType.I_KEEP_LEVEL_STOP_DONE, None, [LevelCommandType.LEVEL_ONCE])),
            (LevelInfoType.LEVEL_DONE,
             (AdminInfoType.I_LEVEL_ONCE_DONE, [(ClientType.MASS, ClientStatus.READY),
                                                (ClientType.LEVEL, ClientStatus.READY)], None)),
        ]
    )
    def test_execute(self, input_info_type, expect_results):
        integrated_command = IntegrationCommandType.MOVE_LEVEL
        integrate_executor = IntegratedInfoExecutor()
        integrate_executor.integrated_command = integrated_command
        integrate_executor.reset(input_info_type)
        output_dict = integrate_executor.execute()
        expect_info, expect_status, expect_command_list = expect_results
        assert output_dict['info_type'] == expect_info
        if expect_status is not None:
            assert output_dict['status'] == expect_status
        if expect_command_list is not None:
            for output_cmd, expect_cmd_type in zip(output_dict['command'], expect_command_list):
                assert output_cmd.command_type == expect_cmd_type
