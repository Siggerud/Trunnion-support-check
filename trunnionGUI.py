from tkinter import Tk, Label, Entry, ttk, Frame, Variable, IntVar, \
    Button, StringVar, Checkbutton
from trunnionCalc import TrunnionCalc
from scraper import Scraper

class trunnionGUI:
    def __init__(self, root):
        self._root = root
        self._root.title("Trunnion calc")
        self._root.geometry("500x780")

        url = "https://en.wikipedia.org/wiki/Nominal_Pipe_Size#:~:text=%22Nominal%22%20refers%20to%20pipe%20in,60.3%20mm)%20outside%20diameter)."
        self._scraper = Scraper(url)

        self._calc = None

        self._pipeSizeTargetTag = ""
        self._scheduleIndex = None

        #TODO: get DN mm into combobox

        self._titleFont = ("Helvetica", 10, "bold")
        self._pady = 5

        self._pipeScheduleDict = self._setPipeScheduleDict()

        inputLabel = Label(self._root, text="Input", font=("Helvetica", 12, "bold"))
        inputLabel.grid(row=0, column=0)

        inputFrame = Frame(self._root, borderwidth=2)
        inputFrame.grid(row=1, column=0, sticky="n")

        geometryLabel = Label(inputFrame, text="Geometry", font=self._titleFont)
        geometryLabel.grid(row=0, column=0)

        pipeLabel = Label(inputFrame, text="Pipe", font=("Helvetica", 8, "bold"))
        pipeLabel.grid(row=1, column=0, sticky="w")

        pipeOD = Label(inputFrame, text="Pipe Outer diameter")
        pipeOD.grid(row=2, column=0, sticky="w", pady=self._pady)

        self._pipeComboVar = Variable()
        self._pipeCombo = ttk.Combobox(inputFrame, textvariable=self._pipeComboVar ,width=10)
        self._pipeCombo.grid(row=2, column=1, sticky="w")
        self._setPipeSizes()

        scheduleLabel = Label(inputFrame, text="Schedule")
        scheduleLabel.grid(row=3, column=0, sticky="w", pady=self._pady)

        self._scheduleComboPipeVar = Variable()
        self._scheduleComboPipe = ttk.Combobox(inputFrame, textvariable=self._scheduleComboPipeVar, width=10)
        self._scheduleComboPipe.grid(row=3, column=1, sticky="w")
        self._setSchedule("pipe")

        pipeWallThicknessLabel = Label(inputFrame, text="Wall thickness")
        pipeWallThicknessLabel.grid(row=4, column=0, sticky="w", pady=self._pady)

        self._pipeWallThicknessValueLabel = Label(inputFrame, text="")
        self._pipeWallThicknessValueLabel.grid(row=4, column=1, sticky="w")

        self._setWallThickness("pipe")

        self._scheduleComboPipe.bind("<<ComboboxSelected>>",
                                     lambda event, arg="pipe": self._makeWidgetChangeAfterSchedule(event, arg))


        corrPipeLabel = Label(inputFrame, text="Corr. allowance (mm)")
        corrPipeLabel.grid(row=5, column=0, sticky="w", pady=self._pady)

        self._corrVar = StringVar()
        corrPipeEntry = Entry(inputFrame, textvariable=self._corrVar, width=5)
        corrPipeEntry.grid(row=5, column=1, sticky="w")
        self._corrVar.set("0")

        millTolLabel = Label(inputFrame, text="Mill. tolerance in %")
        millTolLabel.grid(row=6, column=0, sticky="w", pady=self._pady)

        self._millTolPipeVar = StringVar()
        millTolPipeEntry = Entry(inputFrame, textvariable=self._millTolPipeVar, width=5)
        millTolPipeEntry.grid(row=6, column=1, sticky="w")
        self._millTolPipeVar.set("12.5")

        trunnionLabel = Label(inputFrame, text="Trunnion", font=("Helvetica", 8, "bold"))
        trunnionLabel.grid(row=7, column=0, sticky="w")

        trunnionOD = Label(inputFrame, text="Trunnion outer diameter")
        trunnionOD.grid(row=8, column=0, sticky="w")

        self._trunnionComboVar = Variable()
        self._trunnionCombo = ttk.Combobox(inputFrame, textvariable=self._trunnionComboVar, width=10)
        self._trunnionCombo.grid(row=8, column=1, sticky="w")
        self._setTrunnionSizes()

        self._pipeCombo.bind("<<ComboboxSelected>>", lambda event, arg="pipe": self._makeWidgetChangesAfterPipesize(event, arg))
        self._trunnionCombo.bind("<<ComboboxSelected>>", lambda event, arg="trunnion": self._makeWidgetChangesAfterPipesize(event, arg))

        scheduleLabelTrunn = Label(inputFrame, text="Schedule")
        scheduleLabelTrunn.grid(row=9, column=0, sticky="w", pady=self._pady)

        self._scheduleComboTrunnVar = Variable()
        self._scheduleComboTrunn = ttk.Combobox(inputFrame, textvariable=self._scheduleComboTrunnVar, width=10)
        self._scheduleComboTrunn.grid(row=9, column=1, sticky="w")
        self._setSchedule("trunnion")

        trunnionWallThicknessLabel = Label(inputFrame, text="Wall thickness")
        trunnionWallThicknessLabel.grid(row=10, column=0, sticky="w")

        self._trunnionWallThicknessValueLabel = Label(inputFrame, text="")
        self._trunnionWallThicknessValueLabel.grid(row=10, column=1, sticky="w")

        self._setWallThickness("trunnion")

        self._scheduleComboTrunn.bind("<<ComboboxSelected>>",
                                     lambda event, arg="trunnion": self._makeWidgetChangeAfterSchedule(event, arg))

        millTolLabelTrunn = Label(inputFrame, text="Mill. tolerance in %")
        millTolLabelTrunn.grid(row=11, column=0, sticky="w", pady=self._pady)

        self._millTolTrunnVar = StringVar()
        millTolTrunnEntry = Entry(inputFrame, textvariable=self._millTolTrunnVar, width=5)
        millTolTrunnEntry.grid(row=11, column=1, sticky="w")
        self._millTolTrunnVar.set("12.5")

        heightLabel = Label(inputFrame, text="Height (mm)")
        heightLabel.grid(row=12, column=0, sticky="w", pady=self._pady)

        self._heightVar = IntVar()
        heighEntry = Entry(inputFrame, textvariable=self._heightVar, width=5)
        heighEntry.grid(row=12, column=1, sticky="w")
        self._heightVar.set(100)

        repadLabel = Label(inputFrame, text="Repad thk. (mm)")
        repadLabel.grid(row=13, column=0, sticky="w", pady=self._pady)

        self._repadVar = Variable()
        repadEntry = Entry(inputFrame, textvariable=self._repadVar, width=5)
        repadEntry.grid(row=13, column=1, sticky="w")
        self._repadVar.set("0")

        self._elbowVar = StringVar()
        elbowCheck = Checkbutton(inputFrame, text="Elbow trunnion", variable=self._elbowVar,
                                 onvalue="elbow", offvalue="pipe")
        elbowCheck.grid(row=14, column=0, sticky="w", pady=self._pady)

        materialLabel = Label(inputFrame, text="Material properties", font=self._titleFont)
        materialLabel.grid(row=15, column=0)

        yieldLabel = Label(inputFrame, text="Yield strength (MPa)")
        yieldLabel.grid(row=16, column=0, sticky="w", pady=self._pady)

        self._yieldVar = IntVar()
        yieldEntry = Entry(inputFrame, textvariable=self._yieldVar, width=5)
        yieldEntry.grid(row=16, column=1, sticky="w")

        hotStressLabel = Label(inputFrame, text="Hot stress (MPa)")
        hotStressLabel.grid(row=17, column=0, sticky="w", pady=self._pady)

        self._hotStressVar = IntVar()
        hotStressEntry = Entry(inputFrame, textvariable=self._hotStressVar, width=5)
        hotStressEntry.grid(row=17, column=1, sticky="w")

        forcesLabel = Label(inputFrame, text="Forces and pressure", font=self._titleFont)
        forcesLabel.grid(row=18, column=0)

        pressureLabel = Label(inputFrame, text="Design pressure (barg)")
        pressureLabel.grid(row=19, column=0, sticky="w", pady=self._pady)

        self._pressureVar = IntVar()
        pressureEntry = Entry(inputFrame, textvariable=self._pressureVar, width=5)
        pressureEntry.grid(row=19, column=1, sticky="w")

        axialForceLabel = Label(inputFrame, text="Axial load (N)")
        axialForceLabel.grid(row=20, column=0, sticky="w", pady=self._pady)

        self._axialForceVar = IntVar()
        axialForceEntry = Entry(inputFrame, textvariable=self._axialForceVar, width=5)
        axialForceEntry.grid(row=20, column=1, sticky="w")

        circumForceLabel = Label(inputFrame, text="Circum. load (N)")
        circumForceLabel.grid(row=21, column=0, sticky="w", pady=self._pady)

        self._circumForceVar = IntVar()
        circumForceEntry = Entry(inputFrame, textvariable=self._circumForceVar, width=5)
        circumForceEntry.grid(row=21, column=1, sticky="w")

        lineForceLabel = Label(inputFrame, text="Line load (N)")
        lineForceLabel.grid(row=22, column=0, sticky="w", pady=self._pady)

        self._lineForceVar = IntVar()
        lineForceEntry = Entry(inputFrame, textvariable=self._lineForceVar, width=5)
        lineForceEntry.grid(row=22, column=1, sticky="w")

        calcButton = Button(inputFrame, text="Check", bg="springgreen", command=self._checkTrunnion)
        calcButton.grid(row=23, column=1)

    def _makeWidgetChangeAfterSchedule(self, event, keyWord):
        self._setWallThickness(keyWord)

    def _setWallThickness(self, keyWord):
        if keyWord == "pipe":
            pipeSchedule = self._scheduleComboPipeVar.get()
            pipeSize = self._pipeComboVar.get()
            pipeWallThk = self._pipeScheduleDict[pipeSize][pipeSchedule]
            self._pipeWallThicknessValueLabel.config(text=pipeWallThk + "mm ")
        elif keyWord == "trunnion":
            pipeSchedule = self._scheduleComboTrunn.get()
            pipeSize = self._trunnionComboVar.get()
            pipeWallThk = self._pipeScheduleDict[pipeSize][pipeSchedule]
            self._trunnionWallThicknessValueLabel.config(text=pipeWallThk + "mm ")


    def _setPipeScheduleDict(self):
        sizes = [1.5, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
        sizes = [str(x) for x in sizes]
        sizeDict = {}
        for size in sizes:
            sizeDict[size] = {}

        scraper = Scraper("https://en.wikipedia.org/wiki/Nominal_Pipe_Size")
        soup = scraper.getSoup()
        tables = scraper.findAll(soup, "table", ("class", "wikitable"))
        for table in tables[:5]:
            secondTableForPipeSize = False
            trTags = scraper.findAll(table, "tr")
            scheduleTags = scraper.findAll(trTags[1], "th")
            tableSchedules = []
            for scheduleTag in scheduleTags:
                tableSchedules.append(scheduleTag.text.strip())
            for trTag in trTags[2:]:
                thTags = scraper.findAll(trTag, "th")
                pipeSize = thTags[0].text.strip()
                plusSplit = pipeSize.split("+")
                if len(plusSplit) > 1 or pipeSize.isdigit():
                    if len(plusSplit) > 1:
                        numerator = plusSplit[0]
                        denominator = plusSplit[1][-1]
                        if denominator == "4":
                            decimal = "25"
                        elif denominator == "2":
                            decimal = "5"
                        pipeSize = numerator + "." + decimal
                    if pipeSize not in sizes:
                        continue

                    tdTags = scraper.findAll(trTag, "td")
                    if not "DN" in sizeDict[pipeSize] and not "OD" in sizeDict[pipeSize]:
                        pipeSizeInMm = thTags[1].text.strip()
                        sizeDict[pipeSize]["DN"] = pipeSizeInMm

                        # remove inch part and paranthesis
                        outerDiameter = tdTags[0].text.strip().split()[1][1:-1]
                        sizeDict[pipeSize]["OD"] = outerDiameter

                    else:
                        secondTableForPipeSize = True

                    if secondTableForPipeSize:
                        wallThicknessTags = tdTags
                    else:
                        wallThicknessTags = tdTags[1:]

                    for index, wallThicknessTag in enumerate(wallThicknessTags):
                        wallthicknessText = wallThicknessTag.text.strip()
                        if wallthicknessText == '—':
                            continue
                        # remove inch part and paranthesis
                        metric = wallthicknessText.split()[1][1:-1]
                        sizeDict[pipeSize][tableSchedules[index]] = metric

        return sizeDict

    def _checkTrunnion(self):
        pipeSchedule = self._scheduleComboPipeVar.get()
        pipeSize = self._pipeComboVar.get()
        pipeOuterDiameter = float(self._pipeScheduleDict[pipeSize]["OD"])
        pipeWallThk = float(self._pipeScheduleDict[pipeSize][pipeSchedule])
        pipeMillTol = float(self._millTolPipeVar.get())
        corrAllow = float(self._corrVar.get())

        pipeData = [pipeOuterDiameter, pipeWallThk, pipeMillTol, corrAllow]

        trunnionSchedule = self._scheduleComboTrunnVar.get()
        trunnionSize = self._trunnionComboVar.get()
        trunnionOuterDiameter = float(self._pipeScheduleDict[trunnionSize]["OD"])
        trunnionWallThk = float(self._pipeScheduleDict[trunnionSize][trunnionSchedule])
        trunnionMillTol = float(self._millTolTrunnVar.get())
        trunnionHeight = self._heightVar.get()
        repadThk = float(self._repadVar.get())
        typeOfTrunnion = self._elbowVar.get()

        trunnionData = [trunnionOuterDiameter, trunnionWallThk, trunnionMillTol,
                        trunnionHeight, repadThk, typeOfTrunnion]

        yieldStrength = self._yieldVar.get()
        hotStress = self._hotStressVar.get()

        materialData = [yieldStrength, hotStress]

        self._calc = TrunnionCalc(pipeData, trunnionData, materialData)

        pressure = self._pressureVar.get()
        axialForce = self._axialForceVar.get()
        circumForce = self._circumForceVar.get()
        lineForce = self._lineForceVar.get()

        self._calc.checkTrunnion(pressure, axialForce, circumForce, lineForce)
        self._make_output_frame()

    # TODO: set entries to not editable
    def _make_output_frame(self):
        outputLabel = Label(self._root, text="Results", font=("Helvetica", 12, "bold"))
        outputLabel.grid(row=0, column=1, padx=20)

        outPutFrame = Frame(self._root)
        outPutFrame.grid(row=1, column=1, sticky="n", padx=20)


        localStressLabel = Label(outPutFrame, text="Local stress", font=self._titleFont)
        localStressLabel.grid(row=0, column=0)

        lineLoadsLabel = Label(outPutFrame, text="Line Loads", font=("Helvetica", 8, "bold"))
        lineLoadsLabel.grid(row=1, column=0, sticky="w")

        SlLabel = Label(outPutFrame, text="SL")
        SlLabel.grid(row=2, column=0, sticky="w", pady=self._pady)

        SlVar = StringVar()
        SlEntry = Entry(outPutFrame, textvariable=SlVar, width=10)
        SlEntry.grid(row=2, column=1)
        SlVar.set(f"{self._calc.SL:.2f} MPa")

        ScLabel = Label(outPutFrame, text="SC")
        ScLabel.grid(row=3, column=0, sticky="w", pady=self._pady)

        ScVar = StringVar()
        ScEntry = Entry(outPutFrame, textvariable=ScVar, width=10)
        ScEntry.grid(row=3, column=1)
        ScVar.set(f"{self._calc.SC:.2f} MPa")

        SaLabel = Label(outPutFrame, text="SA")
        SaLabel.grid(row=4, column=0, sticky="w", pady=self._pady)

        SaVar = StringVar()
        SaEntry = Entry(outPutFrame, textvariable=SaVar, width=10)
        SaEntry.grid(row=4, column=1)
        SaVar.set(f"{self._calc.SA:.2f} MPa")

        pressureLoadsLabel = Label(outPutFrame, text="Pressure loads", font=("Helvetica", 8, "bold"))
        pressureLoadsLabel.grid(row=5, column=0, sticky="w")

        SlpLabel = Label(outPutFrame, text="SLP")
        SlpLabel.grid(row=6, column=0, sticky="w", pady=self._pady)

        SlpVar = StringVar()
        SlpEntry = Entry(outPutFrame, textvariable=SlpVar, width=10)
        SlpEntry.grid(row=6, column=1)
        SlpVar.set(f"{self._calc.slp:.2f} MPa")

        ScpLabel = Label(outPutFrame, text="SCP")
        ScpLabel.grid(row=7, column=0, sticky="w", pady=self._pady)

        ScpVar = StringVar()
        ScpEntry = Entry(outPutFrame, textvariable=ScpVar, width=10)
        ScpEntry.grid(row=7, column=1)
        ScpVar.set(f"{self._calc.scp:.2f} MPa")

        loadCombinationsLabel = Label(outPutFrame, text="Load combinations", font=("Helvetica", 8, "bold"))
        loadCombinationsLabel.grid(row=8, column=0, sticky="w")

        loadCombination1Label = Label(outPutFrame, text="SL+SA+SLP")
        loadCombination1Label.grid(row=9, column=0, sticky="w", pady=self._pady)

        loadCombination1Var = StringVar()
        loadCombination1Entry = Entry(outPutFrame, textvariable=loadCombination1Var, width=10)
        loadCombination1Entry.grid(row=9, column=1)
        loadCombination1Var.set(f"{self._calc.SlAndSaAndSlp:.2f} MPa")

        loadCombination2Label = Label(outPutFrame, text="SC+SA+SCP")
        loadCombination2Label.grid(row=10, column=0, sticky="w", pady=self._pady)

        loadCombination2Var = StringVar()
        loadCombination2Entry = Entry(outPutFrame, textvariable=loadCombination2Var, width=10)
        loadCombination2Entry.grid(row=10, column=1)
        loadCombination2Var.set(f"{self._calc.ScAndSaAndScp:.2f} MPa")

        localStressResultLabel = Label(outPutFrame, text="Local stress Result", font=("Helvetica", 8, "bold"))
        localStressResultLabel.grid(row=11, column=0, columnspan=2, sticky="w", pady=self._pady)

        allowableLocalStressLabel = Label(outPutFrame, text="Allowable local stress")
        allowableLocalStressLabel.grid(row=12, column=0, sticky="w", pady=self._pady)

        allowableLocalStressVar = StringVar()
        allowableLocalStressEntry = Entry(outPutFrame, textvariable=allowableLocalStressVar, width=10)
        allowableLocalStressEntry.grid(row=12, column=1)
        allowableLocalStressVar.set(f"{self._calc.allowableLocalStress:.2f} MPa")

        localStressUtilizationLabel = Label(outPutFrame, text="Local stress utilization")
        localStressUtilizationLabel.grid(row=13, column=0, sticky="w", pady=self._pady)

        self._localStressUtilizationVar = StringVar()
        self._localStressUtilizationEntry = Entry(outPutFrame, textvariable=self._localStressUtilizationVar, width=10)
        self._localStressUtilizationEntry.grid(row=13, column=1)
        self._localStressUtilizationVar.set(f"{self._calc.localStressUtilization:.2f}")
        self._colorWidget("local")

        bendingStressLabel = Label(outPutFrame, text="Bending stress", font=self._titleFont)
        bendingStressLabel.grid(row=14, column=0, columnspan=2)

        shearForceLabel = Label(outPutFrame, text="Shear force")
        shearForceLabel.grid(row=15, column=0, sticky="w", pady=self._pady)

        shearForceVar = StringVar()
        shearForceEntry = Entry(outPutFrame, textvariable=shearForceVar, width=10)
        shearForceEntry.grid(row=15, column=1)
        shearForceVar.set(f"{self._calc.V:.2f} N")

        sectionModulusLabel = Label(outPutFrame, text="Trunnion section modulus")
        sectionModulusLabel.grid(row=16, column=0, sticky="w", pady=self._pady)

        sectionModulusVar = StringVar()
        sectionModulusEntry = Entry(outPutFrame, textvariable=sectionModulusVar, width=10)
        sectionModulusEntry.grid(row=16, column=1)
        sectionModulusVar.set(f"{self._calc.Z:.2f} mm^3")

        bendingMomentLabel = Label(outPutFrame, text="Bending moment")
        bendingMomentLabel.grid(row=17, column=0, sticky="w", pady=self._pady)

        bendingMomentVar = StringVar()
        bendingMomentEntry = Entry(outPutFrame, textvariable=bendingMomentVar, width=10)
        bendingMomentEntry.grid(row=17, column=1)
        bendingMomentVar.set(f"{self._calc.Mb:.2f} Nmm")

        bendingStressLabel = Label(outPutFrame, text="Bending stress")
        bendingStressLabel.grid(row=18, column=0, sticky="w", pady=self._pady)

        bendingStressVar = StringVar()
        bendingStressEntry = Entry(outPutFrame, textvariable=bendingStressVar, width=10)
        bendingStressEntry.grid(row=18, column=1)
        bendingStressVar.set(f"{self._calc.Sb:.2f} MPa")

        normalStressLabel = Label(outPutFrame, text="Normal stress")
        normalStressLabel.grid(row=19, column=0, sticky="w", pady=self._pady)

        normalStressVar = StringVar()
        normalStressEntry = Entry(outPutFrame, textvariable=normalStressVar, width=10)
        normalStressEntry.grid(row=19, column=1)
        normalStressVar.set(f"{self._calc.Sn:.2f} MPa")

        shearStressLabel = Label(outPutFrame, text="Shear stress")
        shearStressLabel.grid(row=20, column=0, sticky="w", pady=self._pady)

        shearStressVar = StringVar()
        shearStressEntry = Entry(outPutFrame, textvariable=shearStressVar, width=10)
        shearStressEntry.grid(row=20, column=1)
        shearStressVar.set(f"{self._calc.Ts:.2f} MPa")

        vonMisesStressLabel = Label(outPutFrame, text="Von Mises stress")
        vonMisesStressLabel.grid(row=21, column=0, sticky="w", pady=self._pady)

        vonMisesStressVar = StringVar()
        vonMisesStressEntry = Entry(outPutFrame, textvariable=vonMisesStressVar, width=10)
        vonMisesStressEntry.grid(row=21, column=1)
        vonMisesStressVar.set(f"{self._calc.Svm:.2f} MPa")

        allowableBendingStressLabel = Label(outPutFrame, text="Allowable bending stress")
        allowableBendingStressLabel.grid(row=22, column=0, sticky="w", pady=self._pady)

        allowableBendingStressVar = StringVar()
        allowableBendingStressEntry = Entry(outPutFrame, textvariable=allowableBendingStressVar, width=10)
        allowableBendingStressEntry.grid(row=22, column=1)
        allowableBendingStressVar.set(f"{self._calc.allowableBendingStress:.2f} MPa")

        bendingStressUtilizationLabel = Label(outPutFrame, text="Bending stress utilization")
        bendingStressUtilizationLabel.grid(row=23, column=0, sticky="w", pady=self._pady)

        self._bendingStressUtilizationVar = StringVar()
        self._bendingStressUtilizationEntry = Entry(outPutFrame, textvariable=self._bendingStressUtilizationVar, width=10)
        self._bendingStressUtilizationEntry.grid(row=23, column=1)
        self._bendingStressUtilizationVar.set(f"{self._calc.bendingStressUtilization:.2f}")

        self._colorWidget("bending")

        summaryLabel = Label(outPutFrame, text="Summary", font=self._titleFont)
        summaryLabel.grid(row=24, column=0)

        localSummary = Label(outPutFrame, text="Local stress check")
        localSummary.grid(row=25, column=0, sticky="w", pady=self._pady)

        self._localSummaryResult = Label(outPutFrame)
        self._localSummaryResult.grid(row=25, column=1)

        self._setPassOrFail("local")

        globalSummary = Label(outPutFrame, text="Global stress check")
        globalSummary.grid(row=26, column=0, sticky="w", pady=self._pady)

        self._globalSummaryResult = Label(outPutFrame)
        self._globalSummaryResult.grid(row=26, column=1)

        self._setPassOrFail("global")

    def _setPassOrFail(self, keyWord):
        if keyWord == "local":
            if float(self._localStressUtilizationVar.get()) > 1:
                self._localSummaryResult.config(text="FAIL")
            else:
                self._localSummaryResult.config(text="PASS")
        elif keyWord == "global":
            if float(self._bendingStressUtilizationVar.get()) > 1:
                self._globalSummaryResult.config(text="FAIL")
            else:
                self._globalSummaryResult.config(text="PASS")


    def _colorWidget(self, keyWord):
        if keyWord == "local":
            if float(self._localStressUtilizationVar.get()) > 1:
                self._localStressUtilizationEntry.config(bg="red")
            else:
                self._localStressUtilizationEntry.config(bg="green")
        elif keyWord == "bending":
            if float(self._bendingStressUtilizationVar.get()) > 1:
                self._bendingStressUtilizationEntry.config(bg="red")
            else:
                self._bendingStressUtilizationEntry.config(bg="green")


    def _setTrunnionSizes(self):
        pipeIndex = self._pipeCombo.current()
        if pipeIndex == 0:
            pipeSizes = list(self._pipeScheduleDict.keys())[0]
            trunnionIndex = 0
        else:
            pipeSizes = list(self._pipeScheduleDict.keys())[:pipeIndex]
            trunnionIndex = pipeIndex - 1
        self._trunnionCombo["values"] = pipeSizes
        self._trunnionCombo.current(trunnionIndex)

    def _makeWidgetChangesAfterPipesize(self, event, type):
        if type == "pipe":
            self._setTrunnionSizes()
        self._setSchedule(type)

    def _setPipeSizes(self):
        pipeSizes = list(self._pipeScheduleDict.keys())
        self._pipeCombo["values"] = pipeSizes
        self._pipeCombo.current(4)

    def _setSchedule(self, type):
        if type == "pipe":
            pipeWidget = self._pipeCombo
            scheduleWidget = self._scheduleComboPipe
        elif type == "trunnion":
            pipeWidget = self._trunnionCombo
            scheduleWidget = self._scheduleComboTrunn

        index = pipeWidget.current()
        pipeSize = list(self._pipeScheduleDict.keys())[index]
        schedules = list(self._pipeScheduleDict[pipeSize].keys())[2:]
        scheduleWidget["values"] = schedules
        scheduleWidget.current(0)










root = Tk()
myGUI = trunnionGUI(root)
root.mainloop()
