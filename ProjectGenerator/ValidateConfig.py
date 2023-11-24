from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file for the bakery problem.

    @staticmethod
    def validate(data):
        # Validate mandatory input parameters for the bakery problem
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                     'numOrders', 'timeSlots', 'surfaceCapacity',
                     'minProfit', 'maxProfit', 'minLength', 'maxLength',
                     'minSurface', 'maxSurface', 'minDeliver', 'maxDeliver']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0:
            raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0:
            raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0:
            raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        # Validating new bakery problem parameters
        ValidateConfig._validatePositiveInteger(data.numOrders, 'numOrders')
        ValidateConfig._validatePositiveInteger(data.timeSlots, 'timeSlots')
        ValidateConfig._validatePositiveInteger(data.surfaceCapacity, 'surfaceCapacity')

        ValidateConfig._validateMinMax(data.minProfit, data.maxProfit, 'Profit')
        ValidateConfig._validateMinMax(data.minLength, data.maxLength, 'Length')
        ValidateConfig._validateMinMax(data.minSurface, data.maxSurface, 'Surface')
        ValidateConfig._validateMinMax(data.minDeliver, data.maxDeliver, 'Deliver', upperBound=data.timeSlots)

    @staticmethod
    def _validatePositiveInteger(value, name):
        if not isinstance(value, int) or (value <= 0):
            raise AMMMException('%s(%s) has to be a positive integer value.' % (name, str(value)))

    @staticmethod
    def _validateMinMax(minValue, maxValue, name, upperBound=None):
        if not isinstance(minValue, (int, float)) or not isinstance(maxValue, (int, float)):
            raise AMMMException('%s values must be numeric.' % name)
        if minValue > maxValue:
            raise AMMMException(
                'min%s(%s) must be less than or equal to max%s(%s).' % (name, str(minValue), name, str(maxValue)))
        if upperBound is not None and maxValue > upperBound:
            raise AMMMException('max%s(%s) cannot exceed %s.' % (name, str(maxValue), str(upperBound)))
