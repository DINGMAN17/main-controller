from enum import Enum


class AdminInfoType(Enum):
    M_POS_DONE = "A-INFO-moving mass position set successfully"
    M_MOVE_DONE = "A-INFO-moving mass reached position, please wait for auto-levelling"
    M_STOP_DONE = "A-INFO-moving mass stopped successfully, please wait for auto-levelling"

    L_BATTERY = "A-INFO-levelling inclinometer has enough battery: "
    L_LEVEL_DONE = "A-INFO-auto-levelling finished"
    L_STOP_DONE = "A-INFO-levelling winches stopped"
    L_MOVE_DONE = "A-INFO-levelling auto move finished"
    L_INIT_DONE = "A-INFO-levelling initialisation is finished"

    G_ZERO_DONE = "A-INFO-gyro sensor is zeroed successfully"
    G_STOP_DONE = "A-INFO-gyro stopped successfully"
    G_AUTO_ON_DONE = "A-INFO-gyro auto mode is on! stabilizing will be done automatically"
    G_AUTO_OFF_DONE = "A-INFO-gyro auto mode is off!"
    G_CENTER_DONE = "A-INFO-gyro is centered successfully"


class MassInfoType(Enum):
    MOVE_DONE = "MOVED"
    STOP_DONE = "STOPPED"
    SET_DONE = "POSSET"


class LevelInfoType(Enum):
    LEVEL_DONE = "LevellingFinish"
    STOP_DONE = "Stopped"
    AUTO_MOVE_DONE = "AutoMoveFinish"
    BATTERY = "Bat"
    INIT_DONE = "InitFinish"


class GyroInfoType(Enum):
    ZERO_DONE = "ZEROED"
    STOP_DONE = "STOPPED"
    AUTO_ON_DONE = "AUTOON"
    AUTO_OFF_DONE = "AUTOOFFSELECT"
    CENTER_DONE = "CENTERED"
