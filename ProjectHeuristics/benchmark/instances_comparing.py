from argparse import ArgumentParser
from pathlib import Path

import sys

from ProjectHeuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from ProjectHeuristics.BRKGA_fwk.solver_BRKGA import Solver_BRKGA
from ProjectHeuristics.ValidateInputData import ValidateInputData
from ProjectHeuristics.ValidateConfig import ValidateConfig
from ProjectHeuristics.solvers.solver_Greedy import Solver_Greedy
from ProjectHeuristics.solvers.solver_GRASP import Solver_GRASP
from ProjectHeuristics.solvers.decoder_BRKGA import Decoder
from ProjectHeuristics.problem.BakeryScheduling import BakeryScheduling as Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                file_name = f'solutions/lab5_instances/{self.config.instanceNum}.sol'
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
                print('Greedy LS : firstImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : BestImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
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
                print('GRASP alpha=0.1 LS : firstImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : BestImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)


                print('\n\n-------------------')
                print('BRKGA - best configuration')
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
                        default=Path(__file__).parent.parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)

    for i in range(5):
        file_name = '../data/lab5_instances/lab5_comparing__'+str(i)+'.dat'
        config.inputDataFile = file_name
        config.instanceNum = i
        inputData = DATParser.parse(config.inputDataFile)
        ValidateInputData.validate(inputData)
        main = Main(config)
        main.run(inputData)
