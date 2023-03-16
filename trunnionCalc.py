from math import pi

class TrunnionCalc:
    def __init__(self, pipeData, trunnionData, materialData):
        self._pipeOutDia, self._pipeThk, self._pipeMillTol, self._corrAllow = pipeData
        self._trunnionOutDia, self._trunnionThk, self._trunnionMillTol = trunnionData[:3]
        self._trunnionHeight, self._repadThk, self._typeOfTrunnion = trunnionData[3:]
        self._yieldStrength, self._hotStress = materialData
        self._tc = self._getMinimumPipeThk("pipe")
        self._trunnionArea = self._getTrunnionArea()
        self._Fl = 0
        self._Fc = 0
        self._Fa = 0
        self._FFl = 0
        self._FFc = 0
        self._FFa = 0
        self._slp = 0
        self._scp = 0
        self._SL = 0
        self._SC = 0
        self._SA = 0
        self._localStressComb1 = 0
        self._localStressComb2 = 0
        self._allowableLocalStress = 0
        self._V = 0
        self._Mb = 0
        self._Z = 0
        self._Sb = 0
        self._Sn = 0
        self._Ts = 0
        self._Svm = 0

    def _getTrunnionArea(self):
        trunnionThickness = self._getMinimumPipeThk("trunnion")
        outerRadius = self._trunnionOutDia
        innerRadius = outerRadius - trunnionThickness
        area = pi * (outerRadius**2 - innerRadius**2)

        return area

    def _getMinimumPipeThk(self, type):
        if type == "pipe":
            millTol = self._pipeMillTol
            corrosionMargin = self._corrAllow
            thickness = self._pipeThk
        elif type == "trunnion":
            millTol = self._trunnionMillTol
            corrosionMargin = 0
            thickness = self._trunnionThk

        millMargin = thickness * 0.01 * millTol
        minPipeThk = thickness - millMargin - corrosionMargin

        return minPipeThk

    def checkTrunnion(self, pressure, axialForce, circumForce, lineForce):
        self._Fa = axialForce
        self._Fc = circumForce
        self._Fl = lineForce
        self._pressure = pressure
        self._calculateLineLoads()
        self._calculateTrunnionStress()

    def _calculateLineLoads(self):
        height = self._trunnionHeight
        radius = self._trunnionOutDia / 2
        self._FFl = self._Fl * height / (pi * radius**2)
        self._FFc = self._Fc * height / (pi * radius**2)
        self._FFa = self._Fa / (2 * pi * radius)

    def _getAllowableStressFactor(self):
        if self._typeOfTrunnion == "elbow":
            return 1
        else:
            return 1.5

    def _calculateLocalStresses(self):
        pipeRadius = self._pipeOutDia / 2

        # get pressure stress
        self._slp = self._pressure * pipeRadius / (2 * self._tc)
        self._scp = self._pressure * pipeRadius / self._tc

        # get local stress
        fac = pipeRadius ** 0.5 / self._tc ** 1.5

        self._SL = 1.17 * self._FFl * fac
        self._SC = 2.34 * self._FFc * fac
        self._SA = 1.75 * self._FFa * fac

        self._localStressComb1 = self._SL + self._SA + self._slp
        self._localStressComb2 = self._SC + self._SA + self._scp

        stressFactor = self._getAllowableStressFactor()
        self._allowableLocalStress = stressFactor * self._hotStress

    def _calculateBendingStress(self):
        self._V = (self._Fl**2 + self._Fc**2)**0.5 # shear stress
        self._Mb = self._V * self._trunnionHeight # bending moment
        self._Z = self._getSectionModulus() # section modulus
        self._Sb = self._Mb / self._Z # bending stress
        self._Sn = self._Fa / self._trunnionArea # normal stress
        self._Ts = self._V / (0.5 * self._trunnionArea) # shear stress
        self._Svm = ((self._Sb + self._Sn)**2 + 3*self._Ts**2)**0.5


    def _calculateTrunnionStress(self):
        self._calculateLocalStresses()
        self._calculateBendingStress()

    def _getSectionModulus(self):
        D = self._trunnionOutDia
        trunnionThickness = self._getMinimumPipeThk("trunnion")
        d = D - 2 * trunnionThickness

        z = (pi/32) * (D**4 - d**4)/D

        return z








