from enum import Enum


class BaseInfoType(Enum):
    pass

class AdminInfoType(BaseInfoType):
    M_POS_DONE = "A-INFO-moving mass position set successfully\n"
    M_MOVE_DONE = "A-INFO-moving mass reached position\n"
    M_STOP_DONE = "A-INFO-moving mass stopped successfully\n"

    L_BATTERY_ENOUGH = "A-INFO-levelling inclinometer has enough battery:\n"
    L_BATTERY_LOW = "A-INFO-please charge battery, levelling inclinometer has low battery:\n"
    L_LEVEL_DONE = "A-INFO-auto-levelling finished\n"
    L_STOP_DONE = "A-INFO-levelling winches stopped\n"
    L_MOVE_DONE = "A-INFO-levelling auto move finished\n"
    L_INIT_DONE = "A-INFO-levelling initialisation finished\n"
    L_CABLE_INIT_DONE = "A-INFO-levelling cable initialisation finished\n"

    G_ZERO_DONE = "A-INFO-gyro sensor is zeroed successfully\n"
    G_STOP_DONE = "A-INFO-gyro stopped successfully\n"
    G_AUTO_ON_DONE = "A-INFO-gyro auto mode is on! stabilizing will be done automatically\n"
    G_AUTO_OFF_DONE = "A-INFO-gyro auto mode is off!\n"
    G_CENTER_DONE = "A-INFO-gyro is centered successfully\n"

    I_MASS_MOVE_DONE = "A-INFO-moving mass reached position, please wait for auto-levelling\n"
    I_MASS_STOP_DONE = "A-INFO-moving mass stopped successfully, please wait for auto-levelling\n"
    I_KEEP_LEVEL_STOP_DONE = "A-INFO-Keep levelling stopped, level once starts now\n"
    I_LEVEL_ONCE_DONE = "A-level once done, system ready\n"
    I_MASS_E_STOP = "A-INFO-moving mass E_stopped successfully\n"
    I_LEVEL_E_STOP = "A-INFO-level system E_stopped successfully\n"
    I_GYRO_E_STOP = "A-INFO-gyro E_stopped successfully\n"


class MassInfoType(BaseInfoType):
    MOVE_DONE = "MOVED"
    STOP_DONE = "STOPPED"
    SET_DONE = "POSSET"


class LevelInfoType(BaseInfoType):
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
