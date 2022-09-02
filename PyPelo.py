from ctypes.wintypes import PLONG
import json
from urllib import response
import requests


def testfunc(inValue):
    return inValue + 1
    

def readinsample100():
    status = False
    data = []
    with open('rides_sample100.json') as f:
        data = json.load(f)

    if len(data) != 0:
        status = True
    return status, data

class PeloPerson:
	username_or_email = ''
	password = ''
        
def ConstructHeader(sessionID):
    cookie = f"peloton_session_id={sessionID}"
    headers = {
    "Content-Type": "application/json",
    "Cookie" : cookie,
    "accept" : "application/json",
    "origin" : "https://members.onepeloton.com",
    "accept-language" : "en-US,en;q=0.9",
    "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "referer" : "https://members.onepeloton.com/profile/workouts",
    "authority": "api.onepeloton.com",
    "x-requested-with" : "XmlHttpRequest",
    "peloton-platform" : "web",
    }
    return headers

def PeloLogin(user, pw):
    status = False
    userID = ""
    sessionID = ""
    urlLogin = "https://api.onepeloton.com/auth/login"

    PPerson = PeloPerson()
    PPerson.username_or_email = user
    PPerson.password = pw
    PPersonPayload = json.dumps(PPerson.__dict__)
    headers = {
        "Content-Type": "application/json",
        }
    response = requests.request(method="POST", 
                        url=urlLogin, 
                        data=PPersonPayload, 
                        headers=headers)
    if response.status_code == 200:
        status = True
        data = response.json()
        userID = data['user_id'] 
        sessionID = data['session_id'] 
    return status, userID, sessionID

def GetRideList(userID, sessionID, pageSize, maxRides):
    status = False
    retData = []
    pageNum = 0
    totRidesSoFar = 0

    pageLimit = pageSize
    if maxRides < pageLimit : pageLimit = maxRides
    bContinueQuery = True

    while bContinueQuery:
        urlLogin = f"https://api.onepeloton.com/api/user/{userID}/workouts?joins=ride&limit={pageLimit}&page={pageNum}"

        headers = ConstructHeader(sessionID)
        response = requests.request(method="GET", 
                            url=urlLogin, 
                            headers=headers)
        
        if response.status_code == 200:
            status = True 
            data = response.json()
            retData += data['data']

            totRidesSoFar += data['count']
            pageNum += 1

            if data['show_next'] == False or totRidesSoFar >= maxRides :
                bContinueQuery = False
        else:
            bContinueQuery = False
            retData.clear

    return status, retData
    
def GetWorkoutEvent(sessionID, rideID):
    status = False
    retData = []

    urlLogin = f"https://api.onepeloton.com/api/ride/{rideID}/details"

    headers = ConstructHeader(sessionID)
    response = requests.request(method="GET", 
                        url=urlLogin, 
                        headers=headers)
    if response.status_code == 200:
        status = True 
        retData = response.json()

    return status, retData

def GetWorkoutDetails(sessionID, rideID, secondsPerObservation):
    status = False
    retData = []

    urlLogin = f"https://api.onepeloton.com/api/workout/{rideID}/performance_graph?every_n={secondsPerObservation}"

    headers = ConstructHeader(sessionID)
    response = requests.request(method="GET", 
                        url=urlLogin, 
                        headers=headers)
    if response.status_code == 200:
        status = True 
        retData = response.json()

    return status, retData

def GetWorkoutUserDetails(sessionID, rideID):
    status = False
    retData = []

    urlLogin = f"https://api.onepeloton.com/api/workout/{rideID}"

    headers = ConstructHeader(sessionID)
    response = requests.request(method="GET", 
                        url=urlLogin, 
                        headers=headers)
    if response.status_code == 200:
        status = True 
        retData = response.json()

    return status, retData

def GetRides(userID, sessionID, maxRides, secondsPerObservation = 60):
    pageSize = 25
    status, rides = GetRideList(userID, sessionID, pageSize, maxRides)
    if status == True:
        for ride in rides:
            status, rideEvent = GetWorkoutEvent(sessionID, ride['ride']['id'])
            ride['workoutEvent'] = rideEvent

            status, workoutDetails = GetWorkoutDetails(sessionID, ride['id'], secondsPerObservation)
            ride['workoutDetails'] = workoutDetails

            status, workoutUserDetails = GetWorkoutUserDetails(sessionID, ride['id'])
            ride['workoutUserDetails'] = workoutUserDetails

    return status, rides

def DumpRidesToJSONFile(userID, sessionID, numRides, secondsPerObservation = 60):
    status, rideList = GetRides(userID, sessionID, numRides)
    if status == True:
        with open("rides.json", "w") as outfile:
            json.dump(rideList, outfile)
    return status, rideList

if __name__ == "__main__":
    #status, userID, sessionID = PeloLogin('KenCeglia@hotmail.com', 'Denver.12k')
    #status, rideList = GetRides(userID, sessionID, 25, 5)

    status = True
