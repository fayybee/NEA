class Wire:
    def __init__(self):
        self.__resistance = 0
        self.__voltage = 0
        self.__current = 0

    def updateVoltage(self, newVoltage):
        self.__voltage = newVoltage

    def updateCurrent(self, newCurrent):
        self.__current = newCurrent

    def updateResistance(self, newResistance):
        self.__resistance = newResistance

    def getVoltage(self):
        return self.__voltage

    def getCurrent(self):
        return self.__current

    def getResistance(self):
        return self.__resistance


class EMF:
    def __init__(self, startEMF):
        self.__EMF = startEMF
        self.__internalResistance = 0

    def setEMF(self, newEMF):
        self.__EMF = newEMF

    def getEMF(self):
        return self.__EMF

    def setInternalResistance(self, newResistance):
        self.__internalResistance = newResistance

    def getInternalResistance(self):
        return self.__internalResistance


class Ground:
    def __init__(self):
        self.__voltage = 0
