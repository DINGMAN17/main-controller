class Inclinometer:

    @staticmethod
    def check_battery():
        return "Lbat\n"

    @staticmethod
    def request_data():
        return "Lsensor\n"


class Gyro_sensor:

    @staticmethod
    def get_data():
        return "Gyro_GetYaw\n"

    @staticmethod
    def set_zero():
        return "Gyro_Zero\n"


class LoadCell:

    @staticmethod
    def check_condition():
        return "checkLoadcell\n"


class MovingMassPos:
    @staticmethod
    def get_position():
        return "Mass_GetPos\n"


class Vision:
    @staticmethod
    def get_measurement():
        return "Vision_getPos\n"


if __name__ == "__main__":
    sensor = Inclinometer()
