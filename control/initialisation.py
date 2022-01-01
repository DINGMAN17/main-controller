import json
import math

import numpy as np


class Initialisation:
    """
    calculate the steps for each motor to initiate initial levelling
    """

    def __init__(self, ppvc_type, pulley_num):
        self.params = Initialisation.read_parameters(ppvc_type)
        self.params["pulley_num"] = pulley_num

    @staticmethod
    def read_parameters(ppvc_type):
        with open('/Users/manding/work/LiftingFrame/software/mainController/control/ppvc.json') as json_file:
            ppvc_database = json.load(json_file)
        return ppvc_database[ppvc_type]

    @staticmethod
    def add_parameter(ppvc_dict):
        # TODO: allow add parameter from UI?
        with open('/Users/manding/work/LiftingFrame/software/mainController/control/ppvc.json', 'w') as fp:
            json.dump(ppvc_dict, fp)

    def distance2steps(self, distance):
        """
        convert distance adjustments to steps adjustments for winches
        :param distance: int
        :return: step: str
        """
        sign = "1" if distance < 0 else "0"
        step = int(360 * np.abs(distance) / (2 * math.pi * 0.07))
        return sign + str(step).zfill(4)

    def run(self):
        calculated_adjustments = list(self.calculate())
        if self.result_check(calculated_adjustments):
            valid_adjustments = [self.distance2steps(value) for value in calculated_adjustments]
            msg = self.encrypt_message(valid_adjustments)
        else:
            raise ValueError("Initialization cannot be done due to adjustments exceeding the threshold")
        return msg

    def calculate(self):
        M2_1 = np.sin(2 * np.deg2rad(self.params['lifting_angle_left']))
        M2_2 = self.params['ppvc_mass'] / (self.params['frame_mass'] + self.params['ppvc_mass'])
        M2_3 = self.params['ppvc_width'] / self.params['frame_width'] * (2 * self.params['CG_offset_width'] - 1)
        M2_4 = np.sin(0.5 * np.arcsin(M2_1 * M2_2 * M2_3))
        M2_5 = self.params['frame_width'] * 2 * self.params['pulley_num'] / np.cos(np.deg2rad(self.params['pulley_angle_left']))
        rope_adjusted_width = M2_4 * M2_5

        M1_1 = np.sin(2 * np.deg2rad(self.params['lifting_angle_front']))
        M1_3_1 = (2 * self.params['CG_offset_length'] * self.params['ppvc_length'] * self.params['pulley_num'] +
                  self.params['frame_length'] - self.params['frame_length'] * self.params['pulley_num'])
        M1_3_2 = (self.params['pulley_num'] * (self.params['frame_length'] - 2 * self.params['lifting_offset']))
        M1_4 = np.sin(0.5 * np.arcsin(M1_1 * M2_2 * M1_3_1 / M1_3_2))
        M1_5 = self.params['frame_length'] / 2 * self.params['pulley_num'] / \
               np.cos(np.deg2rad(self.params['pulley_angle_front']))
        rope_adjusted_length = M1_4 * M1_5

        motor_1 = -0.5 * rope_adjusted_length - 0.5 * rope_adjusted_width
        motor_2 = 0.5 * rope_adjusted_length - 0.5 * rope_adjusted_width
        motor_3 = -0.5 * rope_adjusted_length + 0.5 * rope_adjusted_width
        motor_4 = 0.5 * rope_adjusted_length + 0.5 * rope_adjusted_width

        return motor_1, motor_2, motor_3, motor_4

    def result_check(self, adjustments):
        # make sure the adjustment is safety
        threshold = 50
        return all(np.abs(adjustment) <= threshold for adjustment in adjustments)

    def encrypt_message(self, adjustments):
        # TODO: settle message format
        adjustments_str = "".join(adjustments)
        msg = "Linit" + str(len(adjustments_str)) + adjustments_str + "\n"
        return msg


if __name__ == "__main__":
    initialisation = Initialisation("1ton_prototype", 6)
    message = initialisation.run()
    print(message)

