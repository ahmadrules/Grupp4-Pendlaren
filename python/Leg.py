from pydantic import BaseModel

class Leg:
    fromStop: str
    fromTime: str
    toStop: str
    toTime: str

    def __init__(self, fromStop, fromTime, toStop, toTime, totalTime):
        self.fromStop = fromStop
        self.fromTime = fromTime
        self.toStop = toStop
        self.toTime = toTime
        self.totalTime = totalTime