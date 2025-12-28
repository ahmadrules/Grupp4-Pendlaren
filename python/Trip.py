from typing import List
from pydantic import BaseModel
from Leg import Leg

class Trip():
    fromStop: str
    toStop: str
    totalTime: str
    legs: List[Leg]

    def __init__(self, fromStop, fromTime, toStop, toTime, totalTime, legs: List[Leg]):
        self.fromStop = fromStop
        self.fromTime = fromTime
        self.toStop = toStop
        self.toTime = toTime
        self.totalTime = totalTime
        self.legs = legs