from enum import Enum


class BaseInfoType(Enum):
    pass


class AdminInfoType(BaseInfoType):
    M_POS_DONE = "A-INFO-moving mass position set successfully\n"
    M_MOVE_DONE = "A-INFO-moving mass reached position\n"
    M_MOVE_HOME = "A-INFO-moving mass is in home position"
    M_STOP_DONE = "A-INFO-moving mass stopped successfully\n"
    M_MOVE_IN_PROGRESS = "A-INFO-moving mass is moving, please wait patiently\n"
    M_ANTISWAY_ON = "A-INFO-anti sway is on, you can choose to turn it off manually\n"
    M_ANTISWAY_OFF = "A-INFO-anti sway process is now completed\n"
    M_ANTISWAY_AUTO_FINISH = "A-INFO-ANTISWAYAUTODONE"

    L_BATTERY_ENOUGH = "A-INFO-levelling inclinometer has enough battery:\n"
    L_BATTERY_LOW = "A-INFO-please charge battery, levelling inclinometer has low battery:\n"
    L_LEVEL_DONE = "A-INFO-auto-levelling is finished\n"
    L_STOP_DONE = "A-INFO-levelling winches stopped\n"
    L_MOVE_DONE = "A-INFO-levelling auto move finished\n"
    L_INIT_DONE = "A-INFO-levelling initialisation finished\n"
    L_CABLE_INIT_DONE = "A-INFO-levelling cable initialisation finished\n"
    L_AUTO_LEVEL_ON = "A-INFO-auto levelling is on, you can choose to turn it off manually\n"
    L_MANUAL_MOVE_DONE = "A-INFO-manual move is done\n"

    G_ZERO_DONE = "A-INFO-gyro sensor is zeroed successfully\n"
    G_STOP_DONE = "A-INFO-gyro stopped successfully\n"
    G_AUTO_ON_DONE = "A-INFO-gyro auto mode is on! stabilizing will be done automatically\n"
    G_AUTO_OFF_DONE = "A-INFO-gyro auto mode is off!\n"
    G_CENTER_DONE = "A-INFO-gyro is centered successfully\n"
    G_AUTO_ANGLE_DONE = "A-INFO-angle is adjusted successfully\n"
    G_AUTO_ANGLE_ON = "A-INFO-angle is being adjusted now\n"

    I_MASS_MOVE_DONE = "A-INFO-moving mass reached position, please wait for auto-levellingAutoMove\n"
    I_MASS_STOP_DONE = "A-INFO-moving mass stopped successfully, please wait for auto-levellingAutoMove\n"
    I_KEEP_LEVEL_STOP_DONE = "A-INFO-Keep levellingAutoMove stopped, level once starts now\n"
    I_LEVEL_ONCE_DONE = "A-level once done, system ready\n"
    I_MASS_E_STOP = "A-INFO-moving mass E_stopped successfully\n"
    I_LEVEL_E_STOP = "A-INFO-level system E_stopped successfully\n"
    I_GYRO_E_STOP = "A-INFO-gyro E_stopped successfully\n"


class MassInfoType(BaseInfoType):
    MOVE_DONE = "MOVED"
    MOVE_IN_PROGRESS = "MOVING"
    STOP_DONE = "STOPPED"
    SET_DONE = "POSSET"
    ANTI_SWAY_ON_DONE = "ANTISWAYON"
    ANTI_SWAY_OFF_DONE = "ANTISWAYCOMPLETED"
    MOVE_HOME = "HOMED"
    #TODO: check whether anti sway auto done can be received
    MOVE_ANTI_SWAY_AUTO_DONE = "ANTISWAYAUTODONE"


class LevelInfoType(BaseInfoType):
    AUTO_LEVEL_ON = "AutoLevellingOn"
    MANUAL_MOVE_DONE = "ManualMoveFinish"
    LEVEL_DONE = "LevellingFinish"
    STOP_DONE = "Stopped"
    AUTO_MOVE_DONE = "AutoMoveFinish"
    BATTERY = "Bat"
    INIT_DONE = "InitFinish"
    CABLE_INIT_DONE = "CableInitFinish"


class GyroInfoType(BaseInfoType):
    ZERO_DONE = "ZEROED"
    STOP_DONE = "STOPPED"
    AUTO_ON_DONE = "AUTOON"
    AUTO_OFF_DONE = "AUTOOFFSELECT"
    CENTER_DONE = "CENTERED"
    AUTO_ANGLE_ON = "MOVEDELTAANGLEON"
    AUTO_ANGLE_OFF = "MOVEDELTAANGLEOFF"
