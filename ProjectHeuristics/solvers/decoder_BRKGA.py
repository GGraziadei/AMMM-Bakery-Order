'''
AMMM Lab Heuristics
Decoder for the task to CPU assignment problem v2.0
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from AMMMGlobals import AMMMException
from ProjectHeuristics.BRKGA_fwk.decoder import _Decoder

class Decoder(_Decoder):
    def __init__(self, config, instance):
        config.__dict__['numGenes'] = int(instance.getNumOrder())
        config.__dict__['numIndividuals'] = int(config.IndividualsMultiplier * config.numGenes)
        config.__dict__['numElite'] = int(config.eliteProp * config.numIndividuals)
        config.__dict__['numMutants'] = int(config.mutantProp * config.numIndividuals)
        config.__dict__['numCrossover'] = int(config.numIndividuals - config.numElite - config.numMutants)
        super().__init__(config, instance)

    def selectCandidate(self, candidateList):
        if not candidateList: return None

        # sort candidate assignments by highestLoad in ascending order
        sortedCandidateList = sorted(candidateList,
                                     key=lambda x: x.getDelta(),
                                     reverse=True)

        # choose assignment with minimum highest load
        return sortedCandidateList[0]

    def decodeIndividual(self, chromosome):

        if len(chromosome) != self.instance.getNumOrder():
            raise AMMMException("Error: the length of the chromosome does not fits the number of orders")

        # get an empty solution for the problem
        solution = self.instance.createSolution()

        orders = self.instance.getOrders()
        for order in orders:
            order.setGene(chromosome[order.getId()])

        sortedOrders = sorted(orders,
                              key=lambda o: o.getWeightedProfitability(),
                              reverse=True)

        for order in sortedOrders:
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

        return solution, solution.getProfit()