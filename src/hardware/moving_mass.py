class MovingMass:
    @staticmethod
    def check_condition():
        # TODO: CHECK WITH SIM-TECH WHETHER THIS FUNCTION CAN BE IMPLEMENTED
        return ""

    @staticmethod
    def set_movement(x_position, y_position):
        return "Mass_SetPos_" + str(x_position) + str(y_position) + "\n"

    @staticmethod
    def move():
        return "Mass_Move\n"

    @staticmethod
    def stop():
        return "Mass_Stop\n"
