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

Updated by Gianluca Graziadei, Emmanuel Onyekachukwu Irabor

"""
import os
from argparse import ArgumentParser
from pathlib import Path

import sys

# input data parsing and validation
from ProjectHeuristics.datParser import DATParser
from ProjectHeuristics.ValidateInputData import ValidateInputData
from ProjectHeuristics.ValidateConfig import ValidateConfig

# problem model
from ProjectHeuristics.problem.BakeryScheduling import BakeryScheduling


from ProjectHeuristics.solvers.solver_Greedy import Solver_Greedy

from AMMMGlobals import AMMMException

#from ProjectHeuristics.BRKGA_fwk.solver_BRKGA import Solver_BRKGA
#from ProjectHeuristics.solvers.solver_GRASP import Solver_GRASP
#from ProjectHeuristics.solvers.decoder_BRKGA import Decoder



class Main:
    def __init__(self, config):
        self.config = config
        self.solution = None

    def runMultipleInstances(self, numInstances, instancesDirectory, fileNamePrefix, fileNameExtension):
        totalMetric = 0
        for i in range(numInstances):
            instanceFileName = f"{fileNamePrefix}_{i}.{fileNameExtension}"
            instancePath = os.path.join(instancesDirectory, instanceFileName)
            if not os.path.exists(instancePath):
                print(f"Instance file not found: {instancePath}")
                continue

            inputData = DATParser.parse(instancePath)
            ValidateInputData.validate(inputData)

            resultCode = self.run(inputData)
            if resultCode == 0:
                # Assuming the solution object has a method 'getTotalProfit' to get the desired metric
                totalMetric += self.solution.getProfit()
            else:
                print(f"Error occurred in processing instance: {instancePath}")

        averageMetric = totalMetric / numInstances
        print(f"Average Metric over {numInstances} instances: {averageMetric}")

        return averageMetric

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = BakeryScheduling(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    solver = Solver_Greedy(self.config, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                """
                elif self.config.solver == 'GRASP':
                    solver = Solver_GRASP(self.config, instance)
                elif self.config.solver == 'BRKGA':
                    verbose = self.config.verbose
                    self.config.verbose = False
                    greedy = Solver_Greedy(self.config, instance)
                    initialSolution = greedy.solve(solver='Greedy', localSearch=False)
                    self.config.verbose = verbose
                    decoder = Decoder(self.config, instance)
                    solver = Solver_BRKGA(decoder, instance)
                """

                self.solution = solver.solve(solution=initialSolution)
                print(self.solution.__str__())
                self.solution.saveToFile(self.config.solutionFile)
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
    parser = ArgumentParser(description='AMMM Bakery Order')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)

    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Bakery Order')
        print('Gianluca Graziadei, Emmanuel Onyekachukwu Irabor')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    averageMetric = main.runMultipleInstances(10, 'data', 'bakery_example', 'dat')
    sys.exit(0)
