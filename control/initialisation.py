import json

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
        with open('ppvc.json') as json_file:
            ppvc_database = json.load(json_file)
        return ppvc_database[ppvc_type]

    @staticmethod
    def add_parameter(ppvc_dict):
        # TODO: allow add parameter from UI?
        with open('ppvc.json', 'w') as fp:
            json.dump(ppvc_dict, fp)

    def run(self):
        calculated_adjustments = list(self.calculate())
        valid_adjustments = [value if self.result_check(value) else 0 for value in calculated_adjustments]
        message = self.encrypt_message(valid_adjustments)
        return message

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

    def result_check(self, adjustment):
        # make sure the adjustment is safety
        threshold = 50
        return np.abs(adjustment) <= threshold

    def encrypt_message(self, valid_adjustments):
        # TODO: settle message format
        message = ""
        return message


if __name__ == "__main__":
    initialisation = Initialisation("desktop_prototype", 6)
    initialisation.run()

