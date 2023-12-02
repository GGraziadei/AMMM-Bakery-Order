"""
AMMM Bakery order
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
        self._solutionOrders = []
        self._nTimeSlot = nTimeSlot
        self._surface_capacity = surface_capacity
        self._timeSlotCapacity = [self._surface_capacity] * nTimeSlot
        self._ordersStartingSlot = [None] * len(self._orders)
        self._totalProfit = 0.0
        super().__init__()

    def setSolutionOrders(self, solutionOrders):
        self._solutionOrders = solutionOrders

    def getSolutionOrders(self):
        return self._solutionOrders

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

    def updateTimeSlotCapacity(self, timeSlot, length, surface):

        timeSlotId = timeSlot - 1  # timeSlot starts from 1
        endingSlot = timeSlotId + length - 1

        for i in range(timeSlotId, endingSlot + 1):
            self._timeSlotCapacity[i] -= surface

    def getProfit(self):
        return self._totalProfit

    def setOrders(self, orders):
        self._orders = orders

    def can_add_order(self, order_id):
        order = self._orders[order_id]
        candidates = self.timeslot_candidates(order)
        if len(candidates) > 0:
            return True
        else:
            return False

    def can_add_order_to_timeslot(self, order_id, timeSlot):
        order = self._orders[order_id]
        candidates = self.timeslot_candidates(order)
        for candidate in candidates:
            if candidate.getTimeSlot() == timeSlot:
                return True
        return False

    def move_order(self, order_id, timeSlot):
        order = self._orders[order_id]
        candidates = self.timeslot_candidates(order)
        self._ordersStartingSlot[order_id] = None
        self._totalProfit -= order.getProfit()
        for candidate in candidates:
            if candidate.getTimeSlot() == timeSlot:
                self.accept_order(order_id, timeSlot)
                self.updateTimeSlotCapacity(timeSlot, order.getLength(), order.getSurface())
        # remove order from previous time slot

        return False

    def getTimeSlotAssignedToOrder(self, order_id):
        if self._ordersStartingSlot[order_id] is not None:
            return self._ordersStartingSlot[order_id].getSlotId()
        else:
            return None

    def getNTimeslot(self):
        return self._nTimeSlot

    # replace order1(not in solution) with order2(in solution)
    def replace_order(self, order1, order2):
        # remove order2 from solution
        self._totalProfit -= order2.getProfit()
        # update time slot capacity
        for timeSlotId in range(self.getTimeSlotAssignedToOrder(order2.getId()),
                                self.getTimeSlotAssignedToOrder(order2.getId()) + order2.getLength()):
            self._timeSlotCapacity[timeSlotId - 1] -= order2.getSurface()
        # add order1 to solution
        self._totalProfit += order1.getProfit()
        self._ordersStartingSlot[order1.getId()] = StartingSlot(order1.getId(), self.getTimeSlotAssignedToOrder(
            order2.getId()))

        # update time slot capacity
        for timeSlotId in range(self.getTimeSlotAssignedToOrder(order1.getId()),
                                self.getTimeSlotAssignedToOrder(order1.getId()) + order1.getLength()):
            self._timeSlotCapacity[timeSlotId - 1] += order1.getSurface()
        self._solutionOrders.append(order1)
        self._ordersStartingSlot[order2.getId()] = None

    def timeSlotCapacity(self, timeSlot):
        timeSlotId = timeSlot - 1
        return self._timeSlotCapacity[timeSlotId]

    def _checkSurface(self, start_id, end_id, s):
        for i in range(start_id, end_id + 1):
            if self._timeSlotCapacity[i] < s:
                return False
        return True

    def optimal_function(self, t, s, length) -> float:
        return (self.timeSlotCapacity(t) - s) / self.timeSlotCapacity(t)

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
        strSolution += "------------------\n"
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
                timeSlotStart = -1
                timeSlotEnd = -1
                strSolution += ("\nNot taken %s\n" %  order.__str__())

        return strSolution
