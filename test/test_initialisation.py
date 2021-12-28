import unittest
from control.initialisation import Initialisation


class TestInitialisation(unittest.TestCase):
    def test_desktop_prototype(self):
        initialisation = Initialisation("desktop_prototype", 6)
        message = initialisation.run()
        self.assertEqual(message, "init2010021000461004600021\n")


if __name__ == '__main__':
    unittest.main()
