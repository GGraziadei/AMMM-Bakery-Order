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
        endTime = kwargs.get('endTime', None)

        current_solution = initialSolution
        improved = True

        while improved and time.time() < endTime:
            improved = False
            best_neighbor = self.find_best_neighbor(current_solution)

            if best_neighbor is not None and best_neighbor.getProfit() > current_solution.getProfit():
                current_solution = best_neighbor
                improved = True

        return current_solution

    def optimize_space(self, solution):
        orders = solution.getSolutionOrders()
        # remove orders that are not assigned to a time slot
        orders = [order for order in orders if solution.getTimeSlotAssignedToOrder(order.getId()) is not None]

        # Sort orders based on their current time slots for a sequential approach
        orders.sort(key=lambda order_: solution.getTimeSlotAssignedToOrder(order_.getId()))

        for order in orders:
            current_slot = solution.getTimeSlotAssignedToOrder(order.getId())
            # Try moving the order to earlier time slots
            for new_slot in range(1, current_slot):
                if solution.can_add_order_to_timeslot(order.getId(), new_slot):
                    solution.move_order(order.getId(), new_slot)
                    break  # Break once the order is moved to avoid unnecessary checks

    def find_best_neighbor(self, current_solution):
        best_neighbor = None
        best_profit = current_solution.getProfit()
        # self.optimize_space(current_solution)
        sorted_orders = sorted(current_solution.getOrders(),
                               key=lambda order_: order_.getProfit() / (order_.getLength() * order_.getSurface()),
                               reverse=True)

        # now check all orders not in the current solution and try to add them or replace them if we get a better profit
        if 0:
            for order in sorted_orders:
                if order not in current_solution.getSolutionOrders():
                    # try to add the order to the solution
                    candidates = current_solution.timeslot_candidates(order)
                    candidates = sorted(candidates,
                                        key=lambda x: x.getDelta(),
                                        reverse=True)

                    if len(candidates) > 0:
                        best_candidate = candidates.pop(0)
                        # print("best candidate: " + str(best_candidate) + str(order))
                        new_solution = copy.deepcopy(current_solution)
                        new_solution.accept_order(order.getId(), best_candidate.getTimeSlot())
                        new_solution.updateTimeSlotCapacity(best_candidate.getTimeSlot(), order.getLength(),
                                                            order.getSurface())

                        if new_solution.getProfit() > best_profit:
                            best_neighbor = new_solution
                            best_profit = new_solution.getProfit()

        # now we try to see if we can use orders not in the solution to replace orders in the solution
        # to see if we can get a better profit by replacing an order with a better one
        if 1:
            for order1 in self.instance.getOrders():
                best_candidate = None
                best_profit_increase = 0

                if current_solution.getTimeSlotAssignedToOrder(order1.getId()) is None:
                    for order2 in current_solution.getSolutionOrders():
                        if order1 != order2:
                            # Check if the swap is feasible and profitable
                            if self.swap_is_feasible(order1, order2, current_solution):
                                potential_profit = order1.getProfit() - order2.getProfit()

                                # Only consider swaps that increase the profit
                                if potential_profit > 0:
                                    print("swap is feasible: " + str(order1) + " " + str(order2))
                                    new_solution = copy.deepcopy(current_solution)
                                    new_solution.replace_order(order1, order2)
                                    profit_increase = new_solution.getProfit() - current_solution.getProfit()

                                    # Check if this swap is better than the best one found so far
                                    if profit_increase > best_profit_increase:
                                        print("better solution found: " + str(new_solution.getProfit()))
                                        best_candidate = (order1, order2, new_solution)
                                        best_profit_increase = profit_increase

                # Apply the best swap found for this order
                if best_candidate:
                    order1, order2, best_solution = best_candidate
                    current_solution = best_solution
                    best_neighbor = best_solution
                    print("Applied swap: " + str(order1) + " with " + str(order2))

        return best_neighbor

    def swap_is_feasible(self, order1, order2, solution):
        slot = solution.getTimeSlotAssignedToOrder(order2.getId())
        if slot is None:
            return False

        if slot + order1.getLength() > solution.getNTimeslot():
            return False

        # check min and max delivery time
        if order1.getMinDeliver() < order2.getMinDeliver() or order1.getMaxDeliver() > order2.getMaxDeliver():
            return False

        for i in range(slot-1, slot + order1.getLength() - 1):
            if (solution.getTimeSlotCapacity()[i] + order2.getSurface()) - order1.getSurface() < 0:
                return False

        return True
