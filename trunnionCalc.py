from math import pi

class TrunnionCalc:
    # calculates stresses in trunnion
    def __init__(self, pipeData, trunnionData, hotStress):
        self._pipeOutDia, self._pipeThk, self._pipeMillTol, self._corrAllow = pipeData
        self._trunnionOutDia, self._trunnionThk, self._trunnionMillTol = trunnionData[:3]
        self._trunnionHeight, self._repadThk, self._typeOfTrunnion = trunnionData[3:]
        self._hotStress = hotStress
        self._tc = self._get_minimum_pipe_thk("pipe")
        self._trunnionArea = self._get_trunnion_area()
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
        self._SlAndSaAndSlp = 0
        self._ScAndSaAndScp = 0
        self._allowableLocalStress = 0
        self._localStressUtilization = 0

        self._V = 0
        self._Mb = 0
        self._Z = 0
        self._Sb = 0
        self._Sn = 0
        self._Ts = 0
        self._Svm = 0
        self._bendingStressUtilization = 0

    # gets the crossection area of the trunnion
    def _get_trunnion_area(self):
        trunnionThickness = self._get_minimum_pipe_thk("trunnion")
        outerRadius = self._trunnionOutDia / 2
        innerRadius = outerRadius - trunnionThickness
        area = pi * (outerRadius**2 - innerRadius**2)

        return area

    # gets the minimum pipe thickness of either pipe or trunnion
    def _get_minimum_pipe_thk(self, keyWord):
        if keyWord == "pipe":
            millTol = self._pipeMillTol
            corrosionMargin = self._corrAllow
            thickness = self._pipeThk + self._repadThk
        elif keyWord == "trunnion":
            millTol = self._trunnionMillTol
            corrosionMargin = 0
            thickness = self._trunnionThk
        millMargin = thickness * 0.01 * millTol
        minPipeThk = thickness - millMargin - corrosionMargin

        return minPipeThk

    # check that trunnion is within allowable
    def check_trunnion(self, pressure, axialForce, circumForce, lineForce):
        self._Fa = axialForce
        self._Fc = circumForce
        self._Fl = lineForce
        self._pressure = pressure / 10 # bar to MPA
        self._calculate_line_loads()
        self._calculate_trunnion_stress()

    # calculates line loads for trunnion
    def _calculate_line_loads(self):
        height = self._trunnionHeight
        radius = self._trunnionOutDia / 2
        self._FFl = self._Fl * height / (pi * radius**2)
        self._FFc = self._Fc * height / (pi * radius**2)
        self._FFa = self._Fa / (2 * pi * radius)

    # sets the stress factor based on wether or not trunnion is on elbow
    def _get_allowable_stress_factor(self):
        if self._typeOfTrunnion == "elbow":
            return 1
        else:
            return 1.5

    # calculates local stresses on pipe
    def _calculate_local_stresses(self):
        pipeRadius = self._pipeOutDia / 2

        # get pressure stress
        self._slp = self._pressure * pipeRadius / (2 * self._tc)
        self._scp = self._pressure * pipeRadius / self._tc

        # get local stress
        fac = pipeRadius ** 0.5 / self._tc ** 1.5

        self._SL = 1.17 * self._FFl * fac
        self._SC = 2.34 * self._FFc * fac
        self._SA = 1.75 * self._FFa * fac

        self._SlAndSaAndSlp = self._SL + self._SA + self._slp
        self._ScAndSaAndScp = self._SC + self._SA + self._scp

        stressFactor = self._get_allowable_stress_factor()

        self._allowableLocalStress = stressFactor * self._hotStress

        self._localStressUtilization = max(self._SlAndSaAndSlp, self._ScAndSaAndScp) / self._allowableLocalStress

    # calculates bending stress in trunnion
    def _calculate_bending_stress(self):
        self._V = (self._Fl**2 + self._Fc**2)**0.5 # shear stress
        self._Mb = self._V * self._trunnionHeight # bending moment
        self._Z = self._get_section_modulus() # section modulus
        self._Sb = self._Mb / self._Z # bending stress
        self._Sn = self._Fa / self._trunnionArea # normal stress
        self._Ts = self._V / (0.5 * self._trunnionArea) # shear stress
        self._Svm = ((self._Sb + self._Sn)**2 + 3*self._Ts**2)**0.5
        self._allowableBendingStress = self._hotStress

        self._bendingStressUtilization = self._Svm / self._allowableBendingStress

    # calculates local and bending stress
    def _calculate_trunnion_stress(self):
        self._calculate_local_stresses()
        self._calculate_bending_stress()

    # get section modulus for trunnion
    def _get_section_modulus(self):
        D = self._trunnionOutDia
        trunnionThickness = self._get_minimum_pipe_thk("trunnion")
        d = D - 2 * trunnionThickness

        z = (pi/32) * (D**4 - d**4)/D

        return z

    @property
    def bendingStressUtilization(self):
        return self._bendingStressUtilization

    @property
    def allowableBendingStress(self):
        return self._allowableBendingStress

    @property
    def Svm(self):
        return self._Svm

    @property
    def Ts(self):
        return self._Ts

    @property
    def Sn(self):
        return self._Sn

    @property
    def Sb(self):
        return self._Sb

    @property
    def Mb(self):
        return self._Mb

    @property
    def SL(self):
        return self._SL

    @property
    def SC(self):
        return self._SC

    @property
    def SA(self):
        return self._SA

    @property
    def slp(self):
        return self._slp

    @property
    def scp(self):
        return self._scp

    @property
    def SlAndSaAndSlp(self):
        return self._SlAndSaAndSlp

    @property
    def ScAndSaAndScp(self):
        return self._ScAndSaAndScp

    @property
    def allowableLocalStress(self):
        return self._allowableLocalStress

    @property
    def localStressUtilization(self):
        return self._localStressUtilization

    @property
    def V(self):
        return self._V

    @property
    def Z(self):
        return self._Z





