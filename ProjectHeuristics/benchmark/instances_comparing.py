import sys
from argparse import ArgumentParser
from pathlib import Path

from AMMMGlobals import AMMMException
from ProjectHeuristics.ValidateInputData import ValidateInputData
from ProjectHeuristics.datParser import DATParser
from ProjectHeuristics.problem.BakeryScheduling import BakeryScheduling as Instance
from ProjectHeuristics.solvers.solver_GRASP import Solver_GRASP
from ProjectHeuristics.solvers.solver_Greedy import Solver_Greedy


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data, i):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                print('Instance is feasible.')
                file_name = f'solutions/{self.config.instanceNum}.sol'
                log_file = open(file_name, 'w')

                sys.stdout = log_file
                initialSolution = None

                print('\n\n-------------------')
                print('Greedy ')
                self.config.solver = 'Greedy'
                self.config.localSearch = False
                self.config.solutionFile = f'solutions/Greedy_{self.config.instanceNum}.sol'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : firstImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.solutionFile = f'solutions/Greedy_LS_first_{self.config.instanceNum}.sol'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('Greedy LS : BestImprovement')
                self.config.solver = 'Greedy'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.solutionFile = f'solutions/Greedy_LS_best_{self.config.instanceNum}.sol'
                solver = Solver_Greedy(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                # GRASP
                print('\n\n-------------------')
                print('GRASP alpha=0.1 ')
                self.config.solver = 'GRASP'
                self.config.localSearch = False
                self.config.alpha = 0.3
                self.config.solutionFile = f'solutions/GRASP_01_{self.config.instanceNum}.sol'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : firstImprovement')
                self.config.solver = 'GRASP'
                self.config.localSearch = True
                self.config.policy = 'FirstImprovement'
                self.config.alpha = 0.3
                self.config.solutionFile = f'solutions/GRASP_01_LS_first_{self.config.instanceNum}.sol'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('GRASP alpha=0.1 LS : BestImprovement')
                self.config.solver = 'GRASP'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.alpha = 0.3
                self.config.solutionFile = f'solutions/GRASP_01_LS_best_{self.config.instanceNum}.sol'
                solver = Solver_GRASP(self.config, instance)
                solution = solver.solve(solution=initialSolution)

                print('\n\n-------------------')
                print('BRKGA')
                self.config.solver = 'BRKGA'
                self.config.localSearch = True
                self.config.policy = 'BestImprovement'
                self.config.alpha = 0.3
                self.config.solutionFile = f'solutions/BRKGA{self.config.instanceNum}.sol'
                solver = Solver_GRASP(self.config, instance)
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
    print(config.maxExecTime)
    #ValidateConfig.validate(config)

    for i in range(5):
        file_name = 'data/alpha_brute_force/data_'+str(i+1)+'.dat'
        config.inputDataFile = file_name
        config.instanceNum = i
        inputData = DATParser.parse(config.inputDataFile)
        ValidateInputData.validate(inputData)
        main = Main(config)
        main.run(inputData, i)
