
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
                initialSolution = None

                print('\n\n-------------------')
                verbose = self.config.verbose
                self.config.verbose = False
                greedy = Solver_Greedy(self.config, instance)
                initialSolution = greedy.solve(solver='Greedy', localSearch=False)
                self.config.verbose = verbose

                best_config = {
                    "eliteProp": 0.2,
                    "mutantProp": 0.1,
                    "inheritanceProb": 0.7,
                    "IndividualsMultiplier": 1.,
                    "objective": 0.776,
                }
                print('Best config: ', best_config, 'target Simplex: 0.772')

                for eliteProp in [0.1, 0.3,  0.5]:
                    for mutantProp in [0.1,  0.3,  0.5]:
                        for inheritanceProb in [0.1,  0.3, 0.5,  0.7]:
                                IndividualsMultiplier = 1
                                print('\n\n-------------------')
                                print(f'BRKGA eliteProp: {eliteProp}, mutantProp: {mutantProp}, inheritanceProb: {inheritanceProb}, IndividualsMultiplier: {IndividualsMultiplier}')
                                self.config.solver = 'BRKGA'
                                self.config.eliteProp = eliteProp
                                self.config.mutantProp = mutantProp
                                self.config.inheritanceProb = inheritanceProb
                                self.config.IndividualsMultiplier = IndividualsMultiplier
                                decoder = Decoder(self.config, instance)
                                solver = Solver_BRKGA(decoder, instance)
                                solution = solver.solve(solution=initialSolution)
                                if solution.getFitness() < best_config["objective"]:
                                    best_config["eliteProp"] = eliteProp
                                    best_config["mutantProp"] = mutantProp
                                    best_config["inheritanceProb"] = inheritanceProb
                                    best_config["IndividualsMultiplier"] = IndividualsMultiplier
                                    best_config["objective"] = solution.getFitness()

                print('Best config: ', best_config)
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
