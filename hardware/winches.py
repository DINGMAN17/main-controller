import math

from control.initialisation import Initialisation


class Winches:

    @staticmethod
    def initialisation(ppvc_type="1ton_prototype", pulley_num=6):
        ppvc_init = Initialisation(ppvc_type, pulley_num)
        return ppvc_init.run()

    @staticmethod
    def check_condition():
        return "Lcheck05Winch\n"

    @staticmethod
    def up_auto(distance):
        return "Lcmd06AW" + Winches.distance2steps(distance) + "\n"

    @staticmethod
    def down_auto(distance):
        return "Lcmd06AS" + Winches.distance2steps(distance) + "\n"

    @staticmethod
    def stop():
        return "Lcmd01t\n"

    @staticmethod
    def down_manual():
        return "Lcmd02Ms\n"

    @staticmethod
    def up_manual():
        return "Lcmd02Mw\n"

    @staticmethod
    def level_once():
        return "Lcmd01L\n"

    @staticmethod
    def level_auto():
        return "Lcmd01K\n"

    # only for winch testing
    @staticmethod
    def level_continue():
        return "Lcontinue\n"

    # only for winch testing
    @staticmethod
    def get_count():
        return "Lcount\n"

    # only for winch testing
    @staticmethod
    def move():
        return "Lmove\n"

    # only for winch testing
    @staticmethod
    def cable_init():
        return "Lcable_init\n"

    @staticmethod
    def distance2steps(distance):
        pulley_num = 6
        steps = int(360 * distance * pulley_num / (2 * math.pi * 70))
        return str(steps).zfill(4)



