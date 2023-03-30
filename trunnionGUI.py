from tkinter import Tk, Label, Entry, ttk, Frame, Variable, IntVar, \
    Button, StringVar, Checkbutton, messagebox
from trunnionCalc import TrunnionCalc
from scraper import Scraper

class trunnionGUI:
    # GUI for calculating trunnions attached to pipes
    def __init__(self, root):
        self._root = root
        self._root.title("Trunnion calc")
        self._root.geometry("500x800")

        url = "https://en.wikipedia.org/wiki/Nominal_Pipe_Size#:~:text=%22Nominal%22%20refers%20to%20pipe%20in,60.3%20mm)%20outside%20diameter)."
        self._scraper = Scraper(url)

        # trunnion calculator
        self._calc = None

        self._titleFont = ("Helvetica", 10, "bold")
        self._pady = 5

        self._pipeScheduleDict = self._set_pipe_schedule_dict()

        inputLabel = Label(self._root, text="Input", font=("Helvetica", 12, "bold"))
        inputLabel.grid(row=0, column=0)

        self._inputFrame = Frame(self._root)
        self._inputFrame.grid(row=1, column=0, sticky="n")

        geometryLabel = Label(self._inputFrame, text="Geometry", font=self._titleFont)
        geometryLabel.grid(row=0, column=0, columnspan=2)

        pipeLabel = Label(self._inputFrame, text="Pipe", font=("Helvetica", 8, "bold"))
        pipeLabel.grid(row=1, column=0, sticky="w")

        pipeOD = Label(self._inputFrame, text="Pipe Outer diameter")
        pipeOD.grid(row=2, column=0, sticky="w", pady=self._pady)

        self._pipeComboVar = Variable()
        self._pipeCombo = ttk.Combobox(self._inputFrame, state="readonly", textvariable=self._pipeComboVar ,width=10)
        self._pipeCombo.grid(row=2, column=1, sticky="w")
        self._set_pipe_sizes()

        scheduleLabel = Label(self._inputFrame, text="Schedule")
        scheduleLabel.grid(row=3, column=0, sticky="w", pady=self._pady)

        self._scheduleComboPipeVar = Variable()
        self._scheduleComboPipe = ttk.Combobox(self._inputFrame, state="readonly", textvariable=self._scheduleComboPipeVar, width=10)
        self._scheduleComboPipe.grid(row=3, column=1, sticky="w")
        self._set_schedule("pipe")

        pipeWallThicknessLabel = Label(self._inputFrame, text="Wall thickness")
        pipeWallThicknessLabel.grid(row=4, column=0, sticky="w", pady=self._pady)

        self._pipeWallThicknessValueLabel = Label(self._inputFrame, text="")
        self._pipeWallThicknessValueLabel.grid(row=4, column=1, sticky="w")

        self._set_wall_thickness("pipe")

        self._scheduleComboPipe.bind("<<ComboboxSelected>>",
                                     lambda event, arg="pipe": self._make_widget_change_after_schedule(event, arg))


        corrPipeLabel = Label(self._inputFrame, text="Corr. allowance (mm)")
        corrPipeLabel.grid(row=5, column=0, sticky="w", pady=self._pady)

        self._corrVar = StringVar()
        corrPipeEntry = Entry(self._inputFrame, textvariable=self._corrVar, width=5)
        corrPipeEntry.grid(row=5, column=1, sticky="w")
        self._corrVar.set("0")

        millTolLabel = Label(self._inputFrame, text="Mill. tolerance in %")
        millTolLabel.grid(row=6, column=0, sticky="w", pady=self._pady)

        self._millTolPipeVar = StringVar()
        millTolPipeEntry = Entry(self._inputFrame, textvariable=self._millTolPipeVar, width=5)
        millTolPipeEntry.grid(row=6, column=1, sticky="w")
        self._millTolPipeVar.set("12.5")

        trunnionLabel = Label(self._inputFrame, text="Trunnion", font=("Helvetica", 8, "bold"))
        trunnionLabel.grid(row=7, column=0, sticky="w")

        trunnionOD = Label(self._inputFrame, text="Trunnion outer diameter")
        trunnionOD.grid(row=8, column=0, sticky="w")

        self._trunnionComboVar = Variable()
        self._trunnionCombo = ttk.Combobox(self._inputFrame, state="readonly", textvariable=self._trunnionComboVar, width=10)
        self._trunnionCombo.grid(row=8, column=1, sticky="w")
        self._set_trunnion_sizes()

        self._pipeCombo.bind("<<ComboboxSelected>>", lambda event, arg="pipe": self._make_widget_changes_after_pipesize(event, arg))
        self._trunnionCombo.bind("<<ComboboxSelected>>", lambda event, arg="trunnion": self._make_widget_changes_after_pipesize(event, arg))

        scheduleLabelTrunn = Label(self._inputFrame, text="Schedule")
        scheduleLabelTrunn.grid(row=9, column=0, sticky="w", pady=self._pady)

        self._scheduleComboTrunnVar = Variable()
        self._scheduleComboTrunn = ttk.Combobox(self._inputFrame, state="readonly", textvariable=self._scheduleComboTrunnVar, width=10)
        self._scheduleComboTrunn.grid(row=9, column=1, sticky="w")
        self._set_schedule("trunnion")

        trunnionWallThicknessLabel = Label(self._inputFrame, text="Wall thickness")
        trunnionWallThicknessLabel.grid(row=10, column=0, sticky="w")

        self._trunnionWallThicknessValueLabel = Label(self._inputFrame, text="")
        self._trunnionWallThicknessValueLabel.grid(row=10, column=1, sticky="w")

        self._set_wall_thickness("trunnion")

        self._scheduleComboTrunn.bind("<<ComboboxSelected>>",
                                      lambda event, arg="trunnion": self._make_widget_change_after_schedule(event, arg))

        millTolLabelTrunn = Label(self._inputFrame, text="Mill. tolerance in %")
        millTolLabelTrunn.grid(row=11, column=0, sticky="w", pady=self._pady)

        self._millTolTrunnVar = StringVar()
        millTolTrunnEntry = Entry(self._inputFrame, textvariable=self._millTolTrunnVar, width=5)
        millTolTrunnEntry.grid(row=11, column=1, sticky="w")
        self._millTolTrunnVar.set("12.5")

        heightLabel = Label(self._inputFrame, text="Height (mm)")
        heightLabel.grid(row=12, column=0, sticky="w", pady=self._pady)

        self._heightVar = StringVar()
        heighEntry = Entry(self._inputFrame, textvariable=self._heightVar, width=5)
        heighEntry.grid(row=12, column=1, sticky="w")
        self._heightVar.set("100")

        repadLabel = Label(self._inputFrame, text="Repad thk. (mm)")
        repadLabel.grid(row=13, column=0, sticky="w", pady=self._pady)

        self._repadVar = Variable()
        repadEntry = Entry(self._inputFrame, textvariable=self._repadVar, width=5)
        repadEntry.grid(row=13, column=1, sticky="w")
        self._repadVar.set("0")

        self._elbowVar = StringVar()
        elbowCheck = Checkbutton(self._inputFrame, text="Elbow trunnion", variable=self._elbowVar,
                                 onvalue="elbow", offvalue="pipe")
        elbowCheck.grid(row=14, column=0, sticky="w", pady=self._pady)
        self._elbowVar.set("pipe")

        materialLabel = Label(self._inputFrame, text="Material properties", font=self._titleFont)
        materialLabel.grid(row=15, column=0, columnspan=2)

        hotStressLabel = Label(self._inputFrame, text="Hot stress (MPa)")
        hotStressLabel.grid(row=17, column=0, sticky="w", pady=self._pady)

        self._hotStressVar = StringVar()
        hotStressEntry = Entry(self._inputFrame, textvariable=self._hotStressVar, width=5)
        hotStressEntry.grid(row=17, column=1, sticky="w")
        self._hotStressVar.set("0")

        forcesLabel = Label(self._inputFrame, text="Forces and pressure", font=self._titleFont)
        forcesLabel.grid(row=18, column=0, columnspan=2)

        pressureLabel = Label(self._inputFrame, text="Design pressure (barg)")
        pressureLabel.grid(row=19, column=0, sticky="w", pady=self._pady)

        self._pressureVar = StringVar()
        pressureEntry = Entry(self._inputFrame, textvariable=self._pressureVar, width=5)
        pressureEntry.grid(row=19, column=1, sticky="w")
        self._pressureVar.set("0")

        axialForceLabel = Label(self._inputFrame, text="Axial load (N)")
        axialForceLabel.grid(row=20, column=0, sticky="w", pady=self._pady)

        self._axialForceVar = StringVar()
        axialForceEntry = Entry(self._inputFrame, textvariable=self._axialForceVar, width=5)
        axialForceEntry.grid(row=20, column=1, sticky="w")
        self._axialForceVar.set("0")

        circumForceLabel = Label(self._inputFrame, text="Circum. load (N)")
        circumForceLabel.grid(row=21, column=0, sticky="w", pady=self._pady)

        self._circumForceVar = StringVar()
        circumForceEntry = Entry(self._inputFrame, textvariable=self._circumForceVar, width=5)
        circumForceEntry.grid(row=21, column=1, sticky="w")
        self._circumForceVar.set("0")

        lineForceLabel = Label(self._inputFrame, text="Line load (N)")
        lineForceLabel.grid(row=22, column=0, sticky="w", pady=self._pady)

        self._lineForceVar = StringVar()
        lineForceEntry = Entry(self._inputFrame, textvariable=self._lineForceVar, width=5)
        lineForceEntry.grid(row=22, column=1, sticky="w")
        self._lineForceVar.set("0")

        calcButton = Button(self._inputFrame, text="Check", bg="springgreen", command=self._check_trunnion)
        calcButton.grid(row=23, column=1)

    # checks if input string can be converted to float
    def _is_float(self, string):
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False

    # gets the wall thickness for pipe or trunnion
    def _get_wall_thickness(self, keyWord):
        if keyWord == "pipe":
            pipeSchedule = self._scheduleComboPipeVar.get()
            pipeSize = self._pipeComboVar.get().split()[0]
            pipeWallThk = self._pipeScheduleDict[pipeSize][pipeSchedule]
        elif keyWord == "trunnion":
            pipeSchedule = self._scheduleComboTrunn.get()
            pipeSize = self._trunnionComboVar.get().split()[0]
            pipeWallThk = self._pipeScheduleDict[pipeSize][pipeSchedule]

        return pipeWallThk

    # sets the wall thickness visible in the GUI
    def _set_wall_thickness(self, keyWord):
        pipeWallThk = self._get_wall_thickness(keyWord)
        if keyWord == "pipe":
            self._pipeWallThicknessValueLabel.config(text=pipeWallThk + "mm ")
        elif keyWord == "trunnion":
            self._trunnionWallThicknessValueLabel.config(text=pipeWallThk + "mm ")

    # creates a dict with pipesize, OD, DN and wall thicknesses
    def _set_pipe_schedule_dict(self):
        sizes = [1.5, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
        sizes = [str(x) for x in sizes]
        sizeDict = {}
        for size in sizes:
            sizeDict[size] = {}

        scraper = Scraper("https://en.wikipedia.org/wiki/Nominal_Pipe_Size")
        soup = scraper.getSoup()
        tables = soup.find_all("table", class_="wikitable")
        for table in tables[:5]:
            secondTableForPipeSize = False
            trTags = table.find_all("tr")
            scheduleTags = trTags[1].find_all("th")
            tableSchedules = []
            for scheduleTag in scheduleTags:
                # recursive to avoid extracting reference notes
                tableSchedules.append(scheduleTag.find(text=True, recursive=False).strip())
            for trTag in trTags[2:]:
                thTags = trTag.find_all("th")
                pipeSize = thTags[0].text.strip()
                plusSplit = pipeSize.split("+")
                if len(plusSplit) > 1 or pipeSize.isdigit():
                    if len(plusSplit) > 1: # size with fraction
                        numerator = plusSplit[0]
                        denominator = plusSplit[1][-1]
                        if denominator == "4":
                            decimal = "25"
                        elif denominator == "2":
                            decimal = "5"
                        pipeSize = numerator + "." + decimal
                    if pipeSize not in sizes:
                        continue

                    tdTags = trTag.find_all("td")
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
                        if wallthicknessText == '—' or wallthicknessText == "?":
                            continue
                        # remove inch part and parenthesis
                        metric = wallthicknessText.split()[1][1:-1]
                        sizeDict[pipeSize][tableSchedules[index]] = metric

        return sizeDict

    # checks if the negative wall thickness is negative
    def _check_wall_thickness(self):
        pipeWallThk = float(self._get_wall_thickness("pipe"))
        corrosionAllowance = float(self._corrVar.get())
        millMargin = float(self._millTolPipeVar.get()) * 0.01 * pipeWallThk

        if pipeWallThk - corrosionAllowance - millMargin < 0:
            return False
        return True

    # makes a popup with inputmessage
    def _make_popup(self, message):
        messagebox.showinfo(message=message)

    # checks that all entries have valid input
    def _valid_input(self):
        # check that all inputs are numeric type
        inputWidgets = self._inputFrame.winfo_children()
        for index, child in enumerate(inputWidgets):
            if "entry" in child.winfo_name():
                inputNum = child.get()
                if not self._is_float(inputNum):
                    labelText = inputWidgets[index - 1].cget("text").split("(")[0]  # get label text excluding unit
                    self._make_popup(f"Non numeric entry for {labelText.lower()}")
                    return False

        # check that minimum wall thickness is not negative
        if not self._check_wall_thickness():
            self._make_popup("Calculated wall thickness is negative, check corrosion and mill. tolerance")
            return False

        # checks that we have input for allowable stresses
        if float(self._hotStressVar.get()) <= 0:
            self._make_popup("Hot stress must be greater than zero")
            return False

        return True

    # sends data to trunnion calc and shows output of check
    def _check_trunnion(self):
        if not self._valid_input():
            return

        pipeSchedule = self._scheduleComboPipeVar.get()
        pipeSize = self._pipeComboVar.get().split()[0]
        pipeOuterDiameter = float(self._pipeScheduleDict[pipeSize]["OD"])
        pipeWallThk = float(self._pipeScheduleDict[pipeSize][pipeSchedule])
        pipeMillTol = float(self._millTolPipeVar.get())
        corrAllow = float(self._corrVar.get())

        pipeData = [pipeOuterDiameter, pipeWallThk, pipeMillTol, corrAllow]

        trunnionSchedule = self._scheduleComboTrunnVar.get()
        trunnionSize = self._trunnionComboVar.get().split()[0]
        trunnionOuterDiameter = float(self._pipeScheduleDict[trunnionSize]["OD"])
        trunnionWallThk = float(self._pipeScheduleDict[trunnionSize][trunnionSchedule])
        trunnionMillTol = float(self._millTolTrunnVar.get())
        trunnionHeight = float(self._heightVar.get())
        repadThk = float(self._repadVar.get())
        typeOfTrunnion = self._elbowVar.get()

        trunnionData = [trunnionOuterDiameter, trunnionWallThk, trunnionMillTol,
                        trunnionHeight, repadThk, typeOfTrunnion]

        hotStress = float(self._hotStressVar.get())

        self._calc = TrunnionCalc(pipeData, trunnionData, hotStress)

        pressure = float(self._pressureVar.get())
        axialForce = float(self._axialForceVar.get())
        circumForce = float(self._circumForceVar.get())
        lineForce = float(self._lineForceVar.get())

        self._calc.check_trunnion(pressure, axialForce, circumForce, lineForce)
        self._make_output_frame()

    # creats the output frame
    def _make_output_frame(self):
        outputWidth = 16
        outputLabel = Label(self._root, text="Results", font=("Helvetica", 12, "bold"))
        outputLabel.grid(row=0, column=1, padx=20)

        outPutFrame = Frame(self._root)
        outPutFrame.grid(row=1, column=1, sticky="n", padx=20)


        localStressLabel = Label(outPutFrame, text="Local stress", font=self._titleFont)
        localStressLabel.grid(row=0, column=0, columnspan=2)

        lineLoadsLabel = Label(outPutFrame, text="Line Loads", font=("Helvetica", 8, "bold"))
        lineLoadsLabel.grid(row=1, column=0, sticky="w")

        SlLabel = Label(outPutFrame, text="SL")
        SlLabel.grid(row=2, column=0, sticky="w", pady=self._pady)

        SlVar = StringVar()
        SlEntry = Entry(outPutFrame, textvariable=SlVar, width=outputWidth)
        SlEntry.grid(row=2, column=1)
        SlVar.set(f"{self._calc.SL:.2f} MPa")

        ScLabel = Label(outPutFrame, text="SC")
        ScLabel.grid(row=3, column=0, sticky="w", pady=self._pady)

        ScVar = StringVar()
        ScEntry = Entry(outPutFrame, textvariable=ScVar, width=outputWidth)
        ScEntry.grid(row=3, column=1)
        ScVar.set(f"{self._calc.SC:.2f} MPa")

        SaLabel = Label(outPutFrame, text="SA")
        SaLabel.grid(row=4, column=0, sticky="w", pady=self._pady)

        SaVar = StringVar()
        SaEntry = Entry(outPutFrame, textvariable=SaVar, width=outputWidth)
        SaEntry.grid(row=4, column=1)
        SaVar.set(f"{self._calc.SA:.2f} MPa")

        pressureLoadsLabel = Label(outPutFrame, text="Pressure loads", font=("Helvetica", 8, "bold"))
        pressureLoadsLabel.grid(row=5, column=0, sticky="w")

        SlpLabel = Label(outPutFrame, text="SLP")
        SlpLabel.grid(row=6, column=0, sticky="w", pady=self._pady)

        SlpVar = StringVar()
        SlpEntry = Entry(outPutFrame, textvariable=SlpVar, width=outputWidth)
        SlpEntry.grid(row=6, column=1)
        SlpVar.set(f"{self._calc.slp:.2f} MPa")

        ScpLabel = Label(outPutFrame, text="SCP")
        ScpLabel.grid(row=7, column=0, sticky="w", pady=self._pady)

        ScpVar = StringVar()
        ScpEntry = Entry(outPutFrame, textvariable=ScpVar, width=outputWidth)
        ScpEntry.grid(row=7, column=1)
        ScpVar.set(f"{self._calc.scp:.2f} MPa")

        loadCombinationsLabel = Label(outPutFrame, text="Load combinations", font=("Helvetica", 8, "bold"))
        loadCombinationsLabel.grid(row=8, column=0, sticky="w")

        loadCombination1Label = Label(outPutFrame, text="SL+SA+SLP")
        loadCombination1Label.grid(row=9, column=0, sticky="w", pady=self._pady)

        loadCombination1Var = StringVar()
        loadCombination1Entry = Entry(outPutFrame, textvariable=loadCombination1Var, width=outputWidth)
        loadCombination1Entry.grid(row=9, column=1)
        loadCombination1Var.set(f"{self._calc.SlAndSaAndSlp:.2f} MPa")

        loadCombination2Label = Label(outPutFrame, text="SC+SA+SCP")
        loadCombination2Label.grid(row=10, column=0, sticky="w", pady=self._pady)

        loadCombination2Var = StringVar()
        loadCombination2Entry = Entry(outPutFrame, textvariable=loadCombination2Var, width=outputWidth)
        loadCombination2Entry.grid(row=10, column=1)
        loadCombination2Var.set(f"{self._calc.ScAndSaAndScp:.2f} MPa")

        localStressResultLabel = Label(outPutFrame, text="Local stress Result", font=("Helvetica", 8, "bold"))
        localStressResultLabel.grid(row=11, column=0, columnspan=2, sticky="w", pady=self._pady)

        allowableLocalStressLabel = Label(outPutFrame, text="Allowable local stress")
        allowableLocalStressLabel.grid(row=12, column=0, sticky="w", pady=self._pady)

        allowableLocalStressVar = StringVar()
        allowableLocalStressEntry = Entry(outPutFrame, textvariable=allowableLocalStressVar, width=outputWidth)
        allowableLocalStressEntry.grid(row=12, column=1)
        allowableLocalStressVar.set(f"{self._calc.allowableLocalStress:.2f} MPa")

        localStressUtilizationLabel = Label(outPutFrame, text="Local stress utilization")
        localStressUtilizationLabel.grid(row=13, column=0, sticky="w", pady=self._pady)

        self._localStressUtilizationVar = StringVar()
        self._localStressUtilizationEntry = Entry(outPutFrame, textvariable=self._localStressUtilizationVar, width=outputWidth)
        self._localStressUtilizationEntry.grid(row=13, column=1)
        self._localStressUtilizationVar.set(f"{self._calc.localStressUtilization:.2f}")
        self._color_widget("local")

        bendingStressLabel = Label(outPutFrame, text="Bending stress", font=self._titleFont)
        bendingStressLabel.grid(row=14, column=0, columnspan=2)

        shearForceLabel = Label(outPutFrame, text="Shear force")
        shearForceLabel.grid(row=15, column=0, sticky="w", pady=self._pady)

        shearForceVar = StringVar()
        shearForceEntry = Entry(outPutFrame, textvariable=shearForceVar, width=outputWidth)
        shearForceEntry.grid(row=15, column=1)
        shearForceVar.set(f"{self._calc.V:.2f} N")

        sectionModulusLabel = Label(outPutFrame, text="Trunnion section modulus")
        sectionModulusLabel.grid(row=16, column=0, sticky="w", pady=self._pady)

        sectionModulusVar = StringVar()
        sectionModulusEntry = Entry(outPutFrame, textvariable=sectionModulusVar, width=outputWidth)
        sectionModulusEntry.grid(row=16, column=1)
        sectionModulusVar.set(f"{self._calc.Z:.2f} mm^3")

        bendingMomentLabel = Label(outPutFrame, text="Bending moment")
        bendingMomentLabel.grid(row=17, column=0, sticky="w", pady=self._pady)

        bendingMomentVar = StringVar()
        bendingMomentEntry = Entry(outPutFrame, textvariable=bendingMomentVar, width=outputWidth)
        bendingMomentEntry.grid(row=17, column=1)
        bendingMomentVar.set(f"{self._calc.Mb:.2f} Nmm")

        bendingStressLabel = Label(outPutFrame, text="Bending stress")
        bendingStressLabel.grid(row=18, column=0, sticky="w", pady=self._pady)

        bendingStressVar = StringVar()
        bendingStressEntry = Entry(outPutFrame, textvariable=bendingStressVar, width=outputWidth)
        bendingStressEntry.grid(row=18, column=1)
        bendingStressVar.set(f"{self._calc.Sb:.2f} MPa")

        normalStressLabel = Label(outPutFrame, text="Normal stress")
        normalStressLabel.grid(row=19, column=0, sticky="w", pady=self._pady)

        normalStressVar = StringVar()
        normalStressEntry = Entry(outPutFrame, textvariable=normalStressVar, width=outputWidth)
        normalStressEntry.grid(row=19, column=1)
        normalStressVar.set(f"{self._calc.Sn:.2f} MPa")

        shearStressLabel = Label(outPutFrame, text="Shear stress")
        shearStressLabel.grid(row=20, column=0, sticky="w", pady=self._pady)

        shearStressVar = StringVar()
        shearStressEntry = Entry(outPutFrame, textvariable=shearStressVar, width=outputWidth)
        shearStressEntry.grid(row=20, column=1)
        shearStressVar.set(f"{self._calc.Ts:.2f} MPa")

        vonMisesStressLabel = Label(outPutFrame, text="Von Mises stress")
        vonMisesStressLabel.grid(row=21, column=0, sticky="w", pady=self._pady)

        vonMisesStressVar = StringVar()
        vonMisesStressEntry = Entry(outPutFrame, textvariable=vonMisesStressVar, width=outputWidth)
        vonMisesStressEntry.grid(row=21, column=1)
        vonMisesStressVar.set(f"{self._calc.Svm:.2f} MPa")

        allowableBendingStressLabel = Label(outPutFrame, text="Allowable bending stress")
        allowableBendingStressLabel.grid(row=22, column=0, sticky="w", pady=self._pady)

        allowableBendingStressVar = StringVar()
        allowableBendingStressEntry = Entry(outPutFrame, textvariable=allowableBendingStressVar, width=outputWidth)
        allowableBendingStressEntry.grid(row=22, column=1)
        allowableBendingStressVar.set(f"{self._calc.allowableBendingStress:.2f} MPa")

        bendingStressUtilizationLabel = Label(outPutFrame, text="Bending stress utilization")
        bendingStressUtilizationLabel.grid(row=23, column=0, sticky="w", pady=self._pady)

        self._bendingStressUtilizationVar = StringVar()
        self._bendingStressUtilizationEntry = Entry(outPutFrame, textvariable=self._bendingStressUtilizationVar, width=outputWidth)
        self._bendingStressUtilizationEntry.grid(row=23, column=1)
        self._bendingStressUtilizationVar.set(f"{self._calc.bendingStressUtilization:.2f}")

        self._color_widget("bending")

        summaryLabel = Label(outPutFrame, text="Summary", font=self._titleFont)
        summaryLabel.grid(row=24, column=0, columnspan=2)

        localSummary = Label(outPutFrame, text="Local stress check")
        localSummary.grid(row=25, column=0, sticky="w", pady=self._pady)

        self._localSummaryResult = Label(outPutFrame)
        self._localSummaryResult.grid(row=25, column=1)

        self._set_pass_or_fail("local")

        globalSummary = Label(outPutFrame, text="Global stress check")
        globalSummary.grid(row=26, column=0, sticky="w", pady=self._pady)

        self._globalSummaryResult = Label(outPutFrame)
        self._globalSummaryResult.grid(row=26, column=1)

        self._set_pass_or_fail("global")

    # sets "Pass" or "Fail" dependent on the utilization ratios
    def _set_pass_or_fail(self, keyWord):
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

    # colors widget with color dependent on if stresses are acceptable or not
    def _color_widget(self, keyWord):
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

    # sets the trunnion sizes
    def _set_trunnion_sizes(self):
        pipeIndex = self._pipeCombo.current()
        if pipeIndex == 0:
            # if pipe size is the smallest available, trunnion will only have that option for size
            pipeSizes = [self._pipeComboVar.get()]
            trunnionIndex = 0
        else:
            # set options for trunnions to be all sizes smaller than pipe size
            pipeSizes = [(x + " (" + (self._pipeScheduleDict[x]["DN"]) + ")") for x in list(self._pipeScheduleDict.keys())[:pipeIndex]]
            trunnionIndex = pipeIndex - 1 # set default trunnion size to be one size smaller than pipe
        self._trunnionCombo["values"] = pipeSizes
        self._trunnionCombo.current(trunnionIndex)

    # sets all wall thicknesses, schedules and trunnion sizes after pipe size is changed
    def _make_widget_changes_after_pipesize(self, event, keyWord):
        if keyWord == "pipe":
            self._set_trunnion_sizes()
            self._set_schedule(keyWord)
            self._set_wall_thickness(keyWord)
        self._set_schedule("trunnion")
        self._set_wall_thickness("trunnion")

    # sets the wall thickness for selected schedule
    def _make_widget_change_after_schedule(self, event, keyWord):
        self._set_wall_thickness(keyWord)

    # sets the pipe sizes to choose from
    def _set_pipe_sizes(self):
        pipeSizes = [(x + " (" + (self._pipeScheduleDict[x]["DN"]) + ")") for x in self._pipeScheduleDict.keys()]
        self._pipeCombo["values"] = pipeSizes
        self._pipeCombo.current(4)

    # sets schedules for pipe or trunnion size
    def _set_schedule(self, type):
        if type == "pipe":
            pipeWidget = self._pipeCombo
            scheduleWidget = self._scheduleComboPipe
        elif type == "trunnion":
            pipeWidget = self._trunnionCombo
            scheduleWidget = self._scheduleComboTrunn

        index = pipeWidget.current()
        pipeSize = list(self._pipeScheduleDict.keys())[index]
        schedules = list(self._pipeScheduleDict[pipeSize].keys())[2:] # schedules start from index 2
        scheduleWidget["values"] = schedules
        scheduleWidget.current(0) # default selection for schedule will be the lowest available

root = Tk()
myGUI = trunnionGUI(root)
root.mainloop()
