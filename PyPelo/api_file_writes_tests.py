# Python code to demonstrate working of unittest
import unittest
import PyPelo

class TestAPIWrites(unittest.TestCase):

    def setUp(self):
        self.status, self.userID, self.sessionID = PyPelo.PeloLogin('KenCeglia@hotmail.com', 'Tyrant@12k')

    def test_writejsontofile(self):
        self.status, self.rideList = PyPelo.DumpRidesToJSONFile(self.userID, self.sessionID, 10)
        self.assertEqual(self.status, True)


if __name__ == '__main__':
    unittest.main()