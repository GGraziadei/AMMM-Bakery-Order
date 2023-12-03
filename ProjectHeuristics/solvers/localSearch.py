import copy
import time
from AMMMGlobals import AMMMException
from ProjectHeuristics.solver import _Solver


class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)

        current_solution = initialSolution

        policy = self.config.policy

        while time.time() < (self.startTime + self.config.maxExecTime):

            neighbor_solution = self.exchanging_two(current_solution, policy)

            if neighbor_solution.getProfit() > current_solution.getProfit():
                current_solution = neighbor_solution
            else : break #local best already found

            if policy == 'FirstImprovement':
                return current_solution

        return current_solution

    def exchanging_one(self, current_solution, policy='BestImprovement'):

        print("Exploring neighbor, starting with solution of profit: " + str(current_solution.getProfit()))

        sorted_orders = sorted(current_solution.getOrders(),
                               key=lambda order_: order_.getProfit() / (order_.getLength() * order_.getSurface()),
                               reverse=True)

        # now check all orders not in the current solution and try to add them or replace them if we get a better profit
        for order1 in sorted_orders:
            if current_solution.getTimeSlotAssignedToOrder(order1.getId()) is None:
                incumbent = copy.deepcopy(current_solution)
                for order2 in current_solution.getSolutionOrders():
                    if order1 != order2:
                        # Check if the swap is feasible and profitable
                        potential_profit = order1.getProfit() - order2.getProfit()
                        surface_improving = (order1.getSurface() * order1.getLength()) - (order2.getSurface() * order2.getLength())

                        if potential_profit > 0 or surface_improving < 0:
                            starting_timeslot = incumbent.getTimeSlotAssignedToOrder(order2.getId())

                            new_solution = copy.deepcopy(incumbent)
                            new_solution.remove_order(order2.getId())
                            new_solution.updateTimeSlotCapacity(starting_timeslot, order2.getLength(), -order2.getSurface())

                            afflicted_slot = range(starting_timeslot - order1.getLength() +1, starting_timeslot + order2.getLength())
                            candidates_slot = new_solution.timeslot_candidates(order1)

                            if not candidates_slot: continue

                            slot = candidates_slot.pop(0)

                            if slot.getTimeSlot() in afflicted_slot:
                                new_solution.accept_order(order1.getId(), slot.getTimeSlot())
                                new_solution.updateTimeSlotCapacity(slot.getTimeSlot(), order1.getLength(), order1.getSurface())

                                if current_solution.getProfit() < new_solution.getProfit():
                                    print("Neighbor found, profit: " + str(new_solution.getProfit()))

                                    if policy == 'FirstImprovement':
                                        print("First improvement found, profit: " + str(new_solution.getProfit()))
                                        return new_solution

                                    current_solution = new_solution



        return current_solution

    def adding_one(self, current_solution, policy='BestImprovement'):
        for order1 in current_solution.getOrders():
            if current_solution.getTimeSlotAssignedToOrder(order1.getId()) is None:
                candidates_slot = current_solution.timeslot_candidates(order1)

                for slot in candidates_slot:
                    new_solution = copy.deepcopy(current_solution)
                    new_solution.accept_order(order1.getId(), slot.getTimeSlot())
                    new_solution.updateTimeSlotCapacity(slot.getTimeSlot(), order1.getLength(), order1.getSurface())

                    if policy == 'FirstImprovement':
                        return new_solution

                    if new_solution.getProfit() > current_solution.getProfit():
                        current_solution = new_solution

        return current_solution

    def exchanging_two(self, current_solution, policy='BestImprovement'):
        neighbor_solution = self.exchanging_one(current_solution, policy)
        return self.adding_one(neighbor_solution, policy)



