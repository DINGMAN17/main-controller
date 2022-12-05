class Gyroscope:

    @staticmethod
    def stop():
        return "Gyro_Stop\n"

    @staticmethod
    def on_auto():
        return "Gyro_AutoOn\n"

    @staticmethod
    def off_auto():
        return "Gyro_AutoOff\n"

    @staticmethod
    def move_angle(angle):
        return "Gyro_MoveDeltaAngleOn" + angle + "\n"

    @staticmethod
    def move_angle_stop():
        return "Gyro_MoveDeltaAngleOff\n"

    @staticmethod
    def center():
        return "Gyro_Center\n"

    @staticmethod
    def check_condition():
        return "Gyro_CheckSystem\n"
