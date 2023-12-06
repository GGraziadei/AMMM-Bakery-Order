import random
import time
import copy
from ProjectHeuristics.solver import _Solver
from ProjectHeuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidates, alpha):

        candidates = sorted(candidates,
                            key=lambda x: x.getDelta(),
                            reverse=True)

        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        qmax = candidates[0].getDelta()
        qmin = candidates[-1].getDelta()

        bound = qmax - (qmax - qmin) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in candidates:
            if candidate.getDelta() >= bound:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = candidates[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        
        # sorting the order by descending order of profit/length
        orderList = copy.deepcopy(self.instance.getOrders())
        sortedOrder = sorted(orderList, key=lambda x: (x.getProfit() / (x.getLength() * x.getSurface())), reverse=True)


        # for each task taken in sorted order
        for order in sortedOrder:

            # get the list of time slot where the order can be assigned
            candidates = solution.timeslot_candidates(order)

            # no candidate assignments => the order could not be assigned
            if not candidates:
                continue
            
            # select an assignment - best_randomized_candidate
            best_candidate = self._selectCandidate(candidates, alpha)

            # accept candidate
            solution.accept_order(order.getId(), best_candidate.getTimeSlot())
            # update time slot capacity
            solution.updateTimeSlotCapacity(best_candidate.getTimeSlot(), order.getLength(), order.getSurface())
            
        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestProfit = incumbent.getProfit()
        self.writeLogLine(bestHighestProfit, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)

            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionHighestProfit = solution.getProfit()
                if solutionHighestProfit > bestHighestProfit :
                    incumbent = solution
                    bestHighestProfit = solutionHighestProfit
                    self.writeLogLine(bestHighestProfit, iteration)

        self.writeLogLine(bestHighestProfit, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

