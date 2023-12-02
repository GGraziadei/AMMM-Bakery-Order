"""
AMMM Lab Heuristics
Main function
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

updated Gianluca Graziadei
"""

from argparse import ArgumentParser
from pathlib import Path

import sys

from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from Heuristics.BRKGA_fwk.solver_BRKGA import Solver_BRKGA
from Heuristics.validateInputDataP2 import ValidateInputData
from Heuristics.ValidateConfig import ValidateConfig
from Heuristics.solvers.solver_Greedy import Solver_Greedy
from Heuristics.solvers.solver_GRASP import Solver_GRASP
from Heuristics.solvers.decoder_BRKGA import Decoder
from Heuristics.problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                file_name = f'solutions/lab5_instances_results/{self.config.instanceNum}.sol'
                log_file = open(file_name, 'w')

                sys.stdout = log_file
                initialSolution = None

                print('\n\n-------------------')
                print('Greedy ')
                self.config.solver = 'Greedy'
                self.config.localSearch = False
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : firstImprovement, taskExchange')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.neighborhoodStrategy = 'TaskExchange'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : BestImprovement, taskExchange')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.neighborhoodStrategy = 'TaskExchange'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : firstImprovement, Reassignment')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.neighborhoodStrategy = 'Reassignment'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : BestImprovement, Reassignment')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.neighborhoodStrategy = 'Reassignment'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                # GRASP
                print('\n\n-------------------')
                print('GRASP alpha=0.1 ')
                self.config.solver = 'GRASP'
                self.config.localSearch = False
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : firstImprovement, taskExchange')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.neighborhoodStrategy = 'TaskExchange'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : BestImprovement, taskExchange')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.neighborhoodStrategy = 'TaskExchange'
                ssolver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : firstImprovement, Reassignment')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.neighborhoodStrategy = 'Reassignment'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : BestImprovement, Reassignment')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.neighborhoodStrategy = 'Reassignment'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('BRKGA - est configuration')
                self.config.solver = 'GRASP'
                self.config.maxExecTime = 60 * 10
                decoder = Decoder(self.config, instance)
                solver = Solver_BRKGA(decoder, instance)
                solution = solver.solve(solution=initialSolution)

            else:
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)


    for i in range(5):
        file_name = 'data/lab5_instances_results/lab5_comparing__'+str(i)+'.dat'
        config.inputDataFile = file_name
        config.instanceNum = i
        inputData = DATParser.parse(config.inputDataFile)
        ValidateInputData.validate(inputData)
        main = Main(config)
        main.run(inputData)
