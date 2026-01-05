from pydantic import BaseModel

class Leg:
     def __init__(self, fromStop, fromTime, toStop, toTime, totalTime, modeOfTravel, routeNumber):
        self.fromStop = fromStop
        self.fromTime = fromTime
        self.toStop = toStop
        self.toTime = toTime
        self.totalTime = totalTime
        self.modeOfTravel = modeOfTravel
        self.routeNumber = routeNumber