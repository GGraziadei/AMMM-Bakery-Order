from argparse import ArgumentParser
from pathlib import Path
import numpy as np
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
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    print('Greedy solver')
                    solver = Solver_Greedy(self.config, instance)
                elif self.config.solver == 'GRASP':
                    print('GRASP solver')
                    f = open(self.config.solutionFile, 'a')
                    for  alpha in np.arange(0,1,0.1):
                        self.config.alpha = alpha
                        fitness = 0.
                        for i in range(3):
                            print(f'ALPHA {alpha} execution {i}')
                            solver = Solver_GRASP(self.config, instance)
                            solution = solver.solve(solution=initialSolution)
                            # print('Solution Orders: %s' % str(solution.getOrders()))
                            writeStr = f'ALPHA {alpha} execution {i} fitness: {solution.getFitness()}\n\n'
                            f.write(writeStr)
                            fitness += solution.getFitness()
                        fitness /= 3
                        writeStr = f'\t\tALPHA {alpha}  avg_fitness: {fitness}\n\n'
                        f.write(writeStr)
                    f.close()
                elif self.config.solver == 'BRKGA':
                    verbose = self.config.verbose
                    self.config.verbose = False
                    greedy = Solver_Greedy(self.config, instance)
                    initialSolution = greedy.solve(solver='Greedy', localSearch=False)
                    self.config.verbose = verbose
                    decoder = Decoder(self.config, instance)
                    solver = Solver_BRKGA(decoder, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))

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
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Lab Heuristics')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))
