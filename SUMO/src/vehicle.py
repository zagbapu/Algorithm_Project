import traci


class Vehicle():

    def __init__(self, vehicle):
        self._active = True
        self._acceleration = traci.vehicle.getAcceleration(vehicle)
        self._length = traci.vehicle.getLength(vehicle)
        self._maxSpeed = traci.vehicle.getMaxSpeed(vehicle)
        self._name = vehicle
        self._route = traci.vehicle.getRoute(vehicle)
        self._previouslySetValues = dict()

    def __str__(self):
        return self.getName() + " : " + self.getSpeed() + " m/s"

    def __repr__(self):
        return self.getName()

    def getAcceleration(self):
        return self._acceleration

    def isActive(self):
        return self._active

    def isInIntersection(self):
        pos = self.getPosition()
        x = pos[0]
        y = pos[1]
        if 90 < x < 110 and 90 < y < 110:
            return True
        return False

    def getEdge(self):
        return traci.vehicle.getRoadID(self.getName())

    def getLane(self):
        return traci.vehicle.getLaneID(self.getName())

    def getLaneIndex(self):
        return traci.vehicle.getLaneIndex(self.getName())

    def getLanePosition(self):
        return traci.vehicle.getLanePosition(self.getName())

    def getLanePositionFromFront(self):
        return traci.lane.getLength(self.getLane()) - self.getLanePosition()

    def getLeader(self):
        return traci.vehicle.getLeader(self.getName(), 50)

    def getLength(self):
        return self._length

    def getMaxSpeed(self):
        return self._maxSpeed

    def getName(self):
        return self._name

    def getPosition(self):
        return traci.vehicle.getPosition(self.getName())

    def getRemainingRoute(self):
        return self._route[traci.vehicle.getRouteIndex(self.getName()):]

    def getRoute(self):
        return self._route

    def getSpeed(self):
        return traci.vehicle.getSpeed(self.getName())

    def setColor(self, color):
        self._setAttr("setColor", color)

    def setInActive(self):
        self._active = False

    def setImperfection(self, imperfection):
        self._setAttr("setImperfection", imperfection)

    def setMinGap(self, minGap):
        self._setAttr("setMinGap", minGap)

    def setTargetLane(self, lane):
        traci.vehicle.changeLane(self.getName(), lane, 0.5)

    def setTau(self, tau):
        self._setAttr("setTau", tau)

    def setSpeed(self, speed):
        self._setAttr("setSpeed", speed)

    def setSpeedMode(self, speedMode):
        self._setAttr("setSpeedMode", speedMode)

    def setSpeedFactor(self, speedFactor):
        self._setAttr("setSpeedFactor", speedFactor)

    def _setAttr(self, attr, arg):
        # Only set an attribute if the value is different from the previous value set
        # This improves performance
        if self.isActive():
            if attr in self._previouslySetValues:
                if self._previouslySetValues[attr] == arg:
                    return
            self._previouslySetValues[attr] = arg
            getattr(traci.vehicle, attr)(self.getName(), arg)

    # def createReservationRequest(self):
    #     rc = self.getRouteCells()
    #     ID = self.getName()
    #     for
