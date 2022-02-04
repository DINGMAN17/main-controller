from control.initialisation import Initialisation


def test_desktop_prototype():
    database_file = "/Users/manding/work/LiftingFrame/software/mainController/control/ppvc.json"
    initialisation = Initialisation("1ton_prototype", 6, database_file)
    message = initialisation.run()
    assert message == "Linit2000314000931009310314\n"
