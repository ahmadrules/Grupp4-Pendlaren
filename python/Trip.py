from typing import List
from pydantic import BaseModel
from Leg import Leg

class Trip():
    def __init__(self, fromStop, fromTime, toStop, toTime, totalTime, totalSeconds, legs: List[Leg]):
        self.playlistUrl = None
        self.playlistImage = None
        self.fromStop = fromStop
        self.fromTime = fromTime
        self.toStop = toStop
        self.toTime = toTime
        self.totalTime = totalTime
        self.totalSeconds = totalSeconds
        self.legs = legs