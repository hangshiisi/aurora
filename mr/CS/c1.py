class Pet(object):

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def __str__(self):
        return "%s is a %s" % (self.name, self.species)



from pyspark.accumulators import AccumulatorParam
class VectorAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        return [0.0] * len(value)
    def addInPlace(self, val1, val2):
        for i in xrange(len(val1)):
             val1[i] += val2[i]
        return val1