"""
AMMM Bakery optimization
Gianluca Graziadei
"""

from ProjectHeuristics.solution import _Solution


class StartingSlot(object):

    def __init__(self, order_id, slot_id):
        self._order_id = order_id
        self._slot_id = slot_id

    def getOrderId(self):
        return self._order_id

    def getSlotId(self):
        return self._slot_id

    def __str__(self):
        return "order_id: %d, slot_id: %d" % (self._order_id, self._slot_id)


class Candidate(object):

    def __init__(self, timeSlot, delta):
        self._timeSlot = timeSlot
        self._delta = delta

    def getTimeSlot(self):
        return self._timeSlot

    def getDelta(self):
        return self._delta


class BakerySchedulingSolution(_Solution):

    def __init__(self, orders, nTimeSlot, surface_capacity):
        self._orders = orders
        self._nTimeSlot = nTimeSlot
        self._surface_capacity = surface_capacity
        self._timeSlotCapacity = [self._surface_capacity] * nTimeSlot
        self._ordersStartingSlot = [None] * len(self._orders)
        self._totalProfit = 0.0
        super().__init__()

    def getSolutionOrders(self):
        solutionOrders = []
        for order in self._orders:
            if self._ordersStartingSlot[order.getId()] is not None:
                solutionOrders.append(order)
        return solutionOrders

    def getNTimeslot(self):
        return self._nTimeSlot
    def getOrders(self):
        return self._orders

    def getAcceptedOrders(self):
        acceptedOrders = [False] * len(self._ordersStartingSlot)
        for order in self._ordersStartingSlot:
            if order is not None:
                acceptedOrders[order.getOrderId()] = True
        return acceptedOrders

    # override _Solution getFitness
    def getFitness(self):
        return self._totalProfit

    def getOrdersStartingSlot(self):
        return self._ordersStartingSlot

    def remainingSurface(self, timeSlot):
        timeSlotId = timeSlot - 1  # timeSlot starts from 1
        return self._timeSlotCapacity[timeSlotId]

    def accept_order(self, order_id, slot_id):
        profit = self._orders[order_id].getProfit()
        self._totalProfit += profit

        self._ordersStartingSlot[order_id] = StartingSlot(order_id, slot_id)

    def remove_order(self, order_id):
        profit = self._orders[order_id].getProfit()
        self._totalProfit -= profit

        self._ordersStartingSlot[order_id] = None

    def updateTimeSlotCapacity(self, timeSlot, length, surface):

        timeSlotId = timeSlot - 1  # timeSlot starts from 1
        endingSlot = timeSlotId + length - 1

        for i in range(timeSlotId, endingSlot + 1):
            self._timeSlotCapacity[i] -= surface

    def getProfit(self):
        return self._totalProfit

    def setOrders(self, orders):
        self._orders = orders

    def getTimeSlotAssignedToOrder(self, order_id):
        if self._ordersStartingSlot[order_id] is not None:
            return self._ordersStartingSlot[order_id].getSlotId()
        else:
            return None

    def getNTimeslot(self):
        return self._nTimeSlot



    def timeSlotCapacity(self, timeSlot):
        timeSlotId = timeSlot - 1
        return self._timeSlotCapacity[timeSlotId]

    def _checkSurface(self, start_id, end_id, s):
        for i in range(start_id, end_id + 1):
            if self._timeSlotCapacity[i] < s:
                return False
        return True

    def optimal_function(self, t, s, length) -> int:
        # -t is given by the idea to more priority to the first time slot available
        value = (self.timeSlotCapacity(t) -s -t )/ (self.timeSlotCapacity(t))

        return int(value * 1e4) #determinism in the solution

    def timeslot_candidates(self, order) -> list[Candidate]:
        candidates = []
        for t in range(1, self._nTimeSlot + 1):

            timeSlotId = t - 1
            hypoteticalEndingSlotId = timeSlotId + order.getLength() - 1

            # it this condition is true, then the order is not feasible, dont check it anymore
            if hypoteticalEndingSlotId + 1 > order.getMaxDeliver():
                continue

            if hypoteticalEndingSlotId + 1 < order.getMinDeliver():
                continue

            if self._checkSurface(timeSlotId, hypoteticalEndingSlotId, order.getSurface()):
                candidate = Candidate(t, self.optimal_function(t, order.getSurface(), order.getLength()))
                candidates.append(candidate)

        return candidates

    def getTimeSlotCapacity(self):
        return self._timeSlotCapacity

    def getSurfaceCapacity(self):
        return self._surface_capacity

    def __str__(self):

        strSolution = "Total Profit: %f\n" % self._totalProfit
        strSolution += "------------------\nAvailable Capacity:\n"
        for timeSlotId in range(0, self._nTimeSlot):
            strSolution += "Time Slot %d: %f\n" % (timeSlotId, self._timeSlotCapacity[timeSlotId])

        strSolution += "------------------\n"

        for order in self._orders:

            strSolution += "Order %d\t\t" % (order.getId())

            if self._ordersStartingSlot[order.getId()]:
                # order is accepted
                timeSlotStart = self._ordersStartingSlot[order.getId()].getSlotId()
                timeSlotEnd = timeSlotStart + order.getLength() - 1
                for timeSlotId in range(1, self._nTimeSlot + 1):
                    if timeSlotId >= timeSlotStart and timeSlotId <= timeSlotEnd:
                        strSolution += "x\t"
                    else:
                        strSolution += "-\t"

                strSolution += "\nTaken surface: %f, profit %f\n" % (order.getSurface(), order.getProfit())
            else:
                # order is not accepted
                for timeSlotId in range(1, self._nTimeSlot + 1):
                    strSolution += "-\t"

                strSolution += ("\nNot taken %s\n" %  order.__str__())

        return strSolution
