import sys
from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from ProjectGenerator.ValidateConfig import ValidateConfig
from ProjectGenerator.InstanceGenerator import InstanceGenerator

def run():
    try:
        configFile = "config\config.dat"
        print("Project Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        #print all the attributes
        print(config.__dict__)

        ValidateConfig.validate(config)
        print("Creating Instances...")
        instGen = InstanceGenerator(config)
        instGen.generate()
        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())
