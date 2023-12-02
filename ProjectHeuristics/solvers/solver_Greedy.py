import random, time
from ProjectHeuristics.solver import _Solver
from ProjectHeuristics.solvers.localSearch import LocalSearch

import copy


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        # sorting the order by descending order of profit/length
        orderList = copy.deepcopy(self.instance.getOrders())
        sortedOrder = sorted(orderList, key=lambda x: (x.getProfit() / (x.getLength() * x.getSurface())), reverse=True)

        for order in sortedOrder:
            # get the list of time slot where the order can be assigned
            candidates = solution.timeslot_candidates(order)

            # select best time slot - minimizing the delta 'load' of a starting time slot
            candidates = sorted(candidates,
                                key=lambda x: x.getDelta(),
                                reverse=True)
            if len(candidates) > 0:
                best_candidate = candidates.pop(0)

                # accept candidate
                solution.accept_order(order.getId(), best_candidate.getTimeSlot())
                # update time slot capacity
                solution.updateTimeSlotCapacity(best_candidate.getTimeSlot(), order.getLength(), order.getSurface())

        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()

        new_orders = []

        # remove orders that are not assigned to a time slot
        for order in solution.getOrders():
            if solution.getTimeSlotAssignedToOrder(order.getId()) is not None:
                new_orders.append(order)

        if self.config.localSearch:
            localSearch = LocalSearch(self.config, self.instance)
            endTime = self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution
