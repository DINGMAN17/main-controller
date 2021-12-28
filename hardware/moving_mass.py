class MovingMass:
    @staticmethod
    def check_condition():
        # TODO: CHECK WITH SIM-TECH WHETHER THIS FUNCTION CAN BE IMPLEMENTED
        return ""

    @staticmethod
    def init():
        return "Mass_Init\n"

    @staticmethod
    def set_movement(x_position, y_position):
        return "Mass_setPos_" + str(x_position) + str(y_position) + "\n"

    @staticmethod
    def move():
        return "Mass_move\n"

    @staticmethod
    def stop():
        return "Mass_stop\n"


