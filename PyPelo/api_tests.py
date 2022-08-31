# Python code to demonstrate working of unittest
import unittest
import PyPelo

class TestAuthentications(unittest.TestCase):

    def setUp(self):
        pass

    def test_login_success(self):
        status, userID, sessionID = PyPelo.PeloLogin('KenCeglia@hotmail.com', 'Tyrant@12k')
        self.assertEqual(status, True)

    def test_login_fail(self):
        status, userID, sessionID = PyPelo.PeloLogin('KenCeglia@hotmail.com', 'XXX')
        self.assertEqual(status, False)

class TestAPIs(unittest.TestCase):

    def setUp(self):
        self.status, self.userID, self.sessionID = PyPelo.PeloLogin('KenCeglia@hotmail.com', 'Tyrant@12k')

    def test_rides(self):
        self.status, self.rideList = PyPelo.GetRides(self.userID, self.sessionID, 5, 5)
        self.assertEqual(self.status, True)

    def test_ridelist_onepage(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 25, 5)
        self.assertEqual(self.status, True)

    def test_ridelist_multiplepage(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 1, 3)
        self.assertEqual(self.status, True)

    def test_ridelist_fitpage(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 2, 2)
        self.assertEqual(self.status, True)

    def test_workout_event(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 2, 2)
        self.assertEqual(self.status, True)

    def test_workout_details(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 2, 2)
        self.assertEqual(self.status, True)

    def test_workout_user_details(self):
        self.status, self.rideList = PyPelo.GetRideList(self.userID, self.sessionID, 2, 2)
        self.assertEqual(self.status, True)



if __name__ == '__main__':
    unittest.main()