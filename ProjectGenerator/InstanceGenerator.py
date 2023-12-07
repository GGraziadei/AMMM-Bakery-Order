import os, random
from AMMMGlobals import AMMMException

class InstanceGenerator(object):
    # Generate instances for the bakery problem.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        numOrders = self.config.numOrders
        timeSlots = self.config.timeSlots
        surfaceCapacity = self.config.surfaceCapacity

        minProfit = self.config.minProfit
        maxProfit = self.config.maxProfit

        minLength = self.config.minLength
        maxLength = self.config.maxLength

        minSurface = self.config.minSurface
        maxSurface = self.config.maxSurface

        minDeliver = self.config.minDeliver
        maxDeliver = self.config.maxDeliver

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            with open(instancePath, 'w') as fInstance:
                # Generate random values for each order attribute
                profits = [random.randint(minProfit, maxProfit) for _ in range(numOrders)]
                lengths = [random.randint(minLength, maxLength) for _ in range(numOrders)]
                surfaces = [random.randint(minSurface, maxSurface) for _ in range(numOrders)]

                minDelivers = [1] * numOrders
                maxDelivers = [1] * numOrders
                for i in range(numOrders):
                    l = lengths[i]
                    m = random.randint(l, max(l, minDeliver))
                    M = random.randint(m, max(m, maxDeliver))
                    maxDelivers[i] = M
                    minDelivers[i] = m

                #size = 3 ∗ n2 ∗ t + n ∗ t2
                instance_size = 3 * (numOrders**2) * timeSlots + numOrders * (timeSlots**2)

                # Write the generated values to the instance file
                fInstance.write(f'/*instance size {instance_size}*/ \n')
                fInstance.write(f'n={numOrders};\n')
                fInstance.write(f't={timeSlots};\n')
                fInstance.write(f'profit=[{" ".join(map(str, profits))}];\n')
                fInstance.write(f'length=[{" ".join(map(str, lengths))}];\n')
                fInstance.write(f'min_deliver=[{" ".join(map(str, minDelivers))}];\n')
                fInstance.write(f'max_deliver=[{" ".join(map(str, maxDelivers))}];\n')
                fInstance.write(f'surface=[{" ".join(map(str, surfaces))}];\n')
                fInstance.write(f'surface_capacity={surfaceCapacity};\n')

        # Additional instance-specific details can be added as required
