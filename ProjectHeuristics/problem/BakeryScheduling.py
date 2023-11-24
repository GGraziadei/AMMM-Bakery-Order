"""
AMMM Bakery order
Gianluca Graziadei
"""

from ProjectHeuristics.problem.Order import Order
from ProjectHeuristics.problem.BakerySchedulingSolution import BakerySchedulingSolution as Solution

class BakeryScheduling(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        nOrder = inputData.n

        self.nTimeSlot = inputData.t
        self.surface_capacity = inputData.surface_capacity

        self.orders = [None] * nOrder  # vector with orders
        for order_id in range(0, nOrder):
            self.orders[order_id] = Order(order_id=order_id,
                                            profit=inputData.profit[order_id],
                                            length=inputData.length[order_id],
                                            min_deliver=inputData.min_deliver[order_id],
                                            max_deliver=inputData.max_deliver[order_id],
                                            surface=inputData.surface[order_id])

    def getNumOrder(self):
        return len(self.orders)

    def getNumTimeSlot(self):
        return self.nTimeSlot

    def getSurfaceCapacity(self):
        return self.surface_capacity

    def getOrders(self):
        return self.orders

    def createSolution(self):
        solution = Solution(self.orders, self.nTimeSlot, self.surface_capacity)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        # preprocessing

        for order in self.orders:

            if order.getSurface() > self.surface_capacity:
                print("Warning: Order %d has a surface greater than the surface capacity" % order.getId())

            if order.getMinDeliver() > order.getMaxDeliver():
                print("Error: Order %d has a min_deliver greater than the max_deliver" % order.getId())
                return False

            if order.getLength() > self.nTimeSlot:
                print("Error: Order %d has a length greater than the number of time slots" % order.getId())
                return False

            if order.getMinDeliver() > self.nTimeSlot:
                print("Warning: Order %d has a min_deliver greater than the number of time slots" % order.getId())

            if order.getMaxDeliver() > self.nTimeSlot:
                print("Warning: Order %d has a max_deliver greater than the number of time slots" % order.getId())
                order.setMaxDeliver(self.nTimeSlot)

            if order.getMinDeliver() < order.getLength():
                print("Warning: Order %d has a min_deliver smaller than the length" % order.getId())
                #order.setMinDeliver(order.getLength())

        return True
