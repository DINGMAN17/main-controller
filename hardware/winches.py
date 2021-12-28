import math

from control.initialisation import Initialisation


class Winches:

    @staticmethod
    def initialisation(ppvc_type="1ton_prototype", pulley_num=6):
        ppvc_init = Initialisation(ppvc_type, pulley_num)
        return ppvc_init.run()

    @staticmethod
    def check_condition():
        return "check05Winch\n"

    @staticmethod
    def up_auto(distance):
        return "cmd06AW" + Winches.distance2steps(distance) + "\n"

    @staticmethod
    def down_auto(distance):
        return "cmd06AS" + Winches.distance2steps(distance) + "\n"

    @staticmethod
    def stop():
        return "cmd01t\n"

    @staticmethod
    def down_manual():
        return "cmd02Ms\n"

    @staticmethod
    def up_manual():
        return "cmd02Mw\n"

    @staticmethod
    def level_once():
        return "cmd01L\n"

    @staticmethod
    def level_auto():
        return "cmd01K\n"

    @staticmethod
    def level_continue():
        # only for winch testing
        return "continue\n"

    @staticmethod
    def distance2steps(distance):
        pulley_num = 6
        steps = 360 * distance * pulley_num / (2 * math.pi * 70)
        return str(steps)



