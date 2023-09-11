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

    @staticmethod
    def manual_move_Xplus():
        return "Mass_JogXPlus\n"

    @staticmethod
    def manual_move_Xminus():
        return "Mass_JogXMinus\n"

    @staticmethod
    def manual_Move_Xstop():
        return "Mass_JogXStop\n"

    @staticmethod
    def manual_Move_Yplus():
        return "Mass_JogYPlus\n"

    @staticmethod
    def manual_Move_Yminus():
        return "Mass_JogYMinus\n"

    @staticmethod
    def manual_Move_Ystop():
        return "Mass_JogYStop\n"

    @staticmethod
    def anti_sway_on():
        return "Mass_AntiSwayOn\n"

    @staticmethod
    def anti_sway_off():
        return "Mass_AntiSwayOff\n"
