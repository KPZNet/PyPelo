import PyPelo

if __name__ == '__main__':
    status, userID, sessionID = PyPelo.PeloLogin('KenCeglia@hotmail.com', 'Tyrant@12k')
    status, rideList = PyPelo.DumpRidesToJSONFile(userID, sessionID, 2)
    print(f"Complete Successfully : {status}")