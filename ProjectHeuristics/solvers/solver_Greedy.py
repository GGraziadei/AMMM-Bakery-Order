
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
        # sortedOrder = sorted(orderList, key=lambda x: (x.getProfit() / x.getLength()), reverse=True)
        # sortedOrder = sorted(orderList, key=lambda x: (x.getProfit() / x.getSurface()), reverse=True)

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

    """
    Note: the following version is better iff there is an other constraint:
        - use the minimum number of time slot
        
    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        # sorting the order by descending order of profit/length
        orderList = copy.deepcopy(self.instance.getOrders())
        sortedOrder = sorted(orderList, key=lambda x: (x.getProfit() / (x.getLength() * x.getSurface())), reverse=True)
        # initialize the time slot
        t = 1

        while t <= self.instance.getNumTimeSlot() and len(sortedOrder) > 0:
            # compute candidate list for the given solution and time slot
            (candidateList, prunedOrderList) = solution.candidates(sortedOrder, t)

            if len(prunedOrderList) > 0:
                sortedOrder = list(filter(lambda x: x.getId() not in prunedOrderList, sortedOrder))

            if len(candidateList) > 0:
                # select best candidate
                best_candidate = candidateList.pop(0)
                # accept candidate
                solution.accept_order(best_candidate.getId(), t)
                # update time slot capacity
                solution.updateTimeSlotCapacity(t, best_candidate.getLength(), best_candidate.getSurface())
                # remove order from the sorted order list
                # from filter to list
                sortedOrder = list(filter(lambda x: x.getId() != best_candidate.getId(), sortedOrder))

            else:
                t = max(t + 1, solution.getNextSlot(t))

        return solution
    
    """

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

        """
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)
        """

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution
