class Inclinometer:

    @staticmethod
    def check_battery():
        return "bat\n"


class Gyro_sensor:

    @staticmethod
    def check_condition():
        return "checkGyro\n"

    @staticmethod
    def get_data():
        return "Gyro_getYaw\n"

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
        return "Mass_getPos\n"


if __name__ == "__main__":
    sensor = Inclinometer()
    print(sensor.check_condition())
