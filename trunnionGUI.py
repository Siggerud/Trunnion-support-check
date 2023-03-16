from tkinter import Tk, Label, Entry, ttk, Frame, Variable, IntVar, \
    Button, StringVar, Checkbutton
from trunnionCalc import TrunnionCalc
from scraper import Scraper

class trunnionGUI:
    def __init__(self, root):
        self._root = root
        self._root.title("Trunnion calc")
        self._root.geometry("400x650")

        url = "https://en.wikipedia.org/wiki/Nominal_Pipe_Size#:~:text=%22Nominal%22%20refers%20to%20pipe%20in,60.3%20mm)%20outside%20diameter)."
        self._scraper = Scraper(url)

        self._pipeSizeTargetTag = ""
        self._scheduleIndex = None

        #TODO: get DN mm into combobox
        # make elbow option

        titleFont = ("Helvetica", 10, "bold")
        pady=5

        self._pipeSizes = {1.5: [40, 48.26], 2: [50, 60.33], 3: [80, 88.9],
                           4: [100, 114.3], 5: [125, 141.3], 6: [150, 168.28],
                           8: [200, 219.08], 10: [250, 273.05], 12: [300, 323.85],
                           14: [350, 355.6], 16: [400, 406.4], 18: [450, 457.2],
                           20: [500, 508], 22: [550, 558.8], 24: [600, 609.6]}

        inputFrame = Frame(self._root, relief="raised", borderwidth=2)
        inputFrame.grid(row=0, column=0, sticky="n")

        geometryLabel = Label(inputFrame, text="Geometry", font=titleFont)
        geometryLabel.grid(row=0, column=0)

        pipeLabel = Label(inputFrame, text="Pipe", font=("Helvetica", 8, "bold"))
        pipeLabel.grid(row=1, column=0, sticky="w")

        pipeOD = Label(inputFrame, text="Pipe Outer diameter")
        pipeOD.grid(row=2, column=0, sticky="w", pady=pady)

        self._pipeComboVar = Variable()
        self._pipeCombo = ttk.Combobox(inputFrame, textvariable=self._pipeComboVar ,width=5)
        self._pipeCombo.grid(row=2, column=1, sticky="w")
        self._setPipeSizes()

        scheduleLabel = Label(inputFrame, text="Schedule")
        scheduleLabel.grid(row=3, column=0, sticky="w", pady=pady)

        self._scheduleComboPipeVar = Variable()
        self._scheduleComboPipe = ttk.Combobox(inputFrame, textvariable=self._scheduleComboPipeVar, width=5)
        self._scheduleComboPipe.grid(row=3, column=1, sticky="w")
        self._setSchedule(self._scheduleComboPipe)

        corrPipeLabel = Label(inputFrame, text="Corr. allowance (mm)")
        corrPipeLabel.grid(row=4, column=0, sticky="w", pady=pady)

        self._corrVar = StringVar()
        corrPipeEntry = Entry(inputFrame, textvariable=self._corrVar, width=5)
        corrPipeEntry.grid(row=4, column=1, sticky="w")

        millTolLabel = Label(inputFrame, text="Mill. tolerance in %")
        millTolLabel.grid(row=5, column=0, sticky="w", pady=pady)

        self._millTolPipeVar = StringVar()
        millTolPipeEntry = Entry(inputFrame, textvariable=self._millTolPipeVar, width=5)
        millTolPipeEntry.grid(row=5, column=1, sticky="w")

        trunnionLabel = Label(inputFrame, text="Trunnion", font=("Helvetica", 8, "bold"))
        trunnionLabel.grid(row=6, column=0, sticky="w")

        trunnionOD = Label(inputFrame, text="Trunnion outer diameter")
        trunnionOD.grid(row=7, column=0, sticky="w")

        self._trunnionComboVar = Variable()
        self._trunnionCombo = ttk.Combobox(inputFrame, textvariable=self._trunnionComboVar, width=5)
        self._trunnionCombo.grid(row=7, column=1, sticky="w")
        self._setTrunnionSizesAtStart()

        self._pipeCombo.bind("<<ComboboxSelected>>", self._setTrunnionSizes)

        scheduleLabelTrunn = Label(inputFrame, text="Schedule")
        scheduleLabelTrunn.grid(row=8, column=0, sticky="w", pady=pady)

        self._scheduleComboTrunnVar = Variable()
        self._scheduleComboTrunn = ttk.Combobox(inputFrame, textvariable=self._scheduleComboTrunnVar, width=5)
        self._scheduleComboTrunn.grid(row=8, column=1, sticky="w")
        self._setSchedule(self._scheduleComboTrunn)

        millTolLabelTrunn = Label(inputFrame, text="Mill. tolerance in %")
        millTolLabelTrunn.grid(row=9, column=0, sticky="w", pady=pady)

        self._millTolTrunnVar = StringVar()
        millTolTrunnEntry = Entry(inputFrame, textvariable=self._millTolTrunnVar, width=5)
        millTolTrunnEntry.grid(row=9, column=1, sticky="w")

        heightLabel = Label(inputFrame, text="Height (mm)")
        heightLabel.grid(row=10, column=0, sticky="w", pady=pady)

        self._heightVar = IntVar()
        heighEntry = Entry(inputFrame, textvariable=self._heightVar, width=5)
        heighEntry.grid(row=10, column=1, sticky="w")

        repadLabel = Label(inputFrame, text="Repad thk. (mm)")
        repadLabel.grid(row=11, column=0, sticky="w", pady=pady)

        self._repadVar = Variable()
        repadEntry = Entry(inputFrame, textvariable=self._repadVar, width=5)
        repadEntry.grid(row=11, column=1, sticky="w")

        self._elbowVar = StringVar()
        elbowCheck = Checkbutton(inputFrame, text="Elbow trunnion", variable=self._elbowVar,
                                 onvalue="elbow", offvalue="pipe")
        elbowCheck.grid(row=12, column=0, sticky="w", pady=pady)

        materialLabel = Label(inputFrame, text="Material properties", font=titleFont)
        materialLabel.grid(row=13, column=0)

        yieldLabel = Label(inputFrame, text="Yield strength")
        yieldLabel.grid(row=14, column=0, sticky="w", pady=pady)

        self._yieldVar = IntVar()
        yieldEntry = Entry(inputFrame, textvariable=self._yieldVar, width=5)
        yieldEntry.grid(row=14, column=1, sticky="w")

        hotStressLabel = Label(inputFrame, text="Hot stress")
        hotStressLabel.grid(row=15, column=0, sticky="w", pady=pady)

        self._hotStressVar = IntVar()
        hotStressEntry = Entry(inputFrame, textvariable=self._hotStressVar, width=5)
        hotStressEntry.grid(row=15, column=1, sticky="w")

        forcesLabel = Label(inputFrame, text="Forces and pressure", font=titleFont)
        forcesLabel.grid(row=16, column=0)

        pressureLabel = Label(inputFrame, text="Design pressure")
        pressureLabel.grid(row=17, column=0, sticky="w", pady=pady)

        self._pressureVar = IntVar()
        pressureEntry = Entry(inputFrame, textvariable=self._pressureVar, width=5)
        pressureEntry.grid(row=17, column=1, sticky="w")

        axialForceLabel = Label(inputFrame, text="Axial load (N)")
        axialForceLabel.grid(row=18, column=0, sticky="w", pady=pady)

        self._axialForceVar = IntVar()
        axialForceEntry = Entry(inputFrame, textvariable=self._axialForceVar, width=5)
        axialForceEntry.grid(row=18, column=1, sticky="w")

        circumForceLabel = Label(inputFrame, text="Axial load (N)")
        circumForceLabel.grid(row=19, column=0, sticky="w", pady=pady)

        self._circumForceVar = IntVar()
        circumForceEntry = Entry(inputFrame, textvariable=self._circumForceVar, width=5)
        circumForceEntry.grid(row=19, column=1, sticky="w")

        lineForceLabel = Label(inputFrame, text="Line load (N)")
        lineForceLabel.grid(row=20, column=0, sticky="w", pady=pady)

        self._lineForceVar = IntVar()
        lineForceEntry = Entry(inputFrame, textvariable=self._lineForceVar, width=5)
        lineForceEntry.grid(row=20, column=1, sticky="w")

        calcButton = Button(inputFrame, text="Check", bg="springgreen", command=self._checkTrunnion)
        calcButton.grid(row=21, column=1)

    def _checkIfPipeSizeExists(self, tags, ourSize):
        for tag in tags:
            sizeRaw = self._scraper.findAll(tag, "th")[0].text.strip()
            if not sizeRaw[0].isdigit():
                continue
            if len(sizeRaw.split("+")) > 1:
                if sizeRaw.split("+")[1].strip()[-1] == "2":
                    size = sizeRaw.split("+")[0] + ".5"
            else:
                size = sizeRaw
            if size == ourSize:
                self._pipeSizeTargetTag = tag
                return True
        return False

    def _checkIfScheduleExists(self, tags, schedule):
        self._scheduleIndex = 1
        for tag in tags:
            if tag == "":
                continue
            splitBySpace = tag.split()
            if splitBySpace[0] == "Sch." or splitBySpace[0] == "XXS":
                if splitBySpace[0] == "XXS":
                    if schedule == "XXS":
                        return True
                else:
                    scheduleTag = splitBySpace[1]
                    splitBySlash = scheduleTag.split("/")
                    if len(splitBySlash) > 1:
                        splitBySlash = [x.lower() for x in splitBySlash]
                        if schedule in splitBySlash:
                            return True
                    else:
                        if scheduleTag == schedule:
                            return True
                self._scheduleIndex += 1
        return False

    def _getWallThk(self, pipeSchedule, pipeSize):
        wikitables = self._scraper.findAll(self._scraper.getSoup(), "table", ("class", "wikitable"))

        for table in wikitables:
            scheduleFound = False
            pipeSizeFound = False

            trTags = self._scraper.findAll(table, "tr")
            scheduleTags = trTags[1]

            scheduleFound = self._checkIfScheduleExists(scheduleTags.text.split("\n"), pipeSchedule)
            if not scheduleFound:
                continue

            pipeTag = trTags[2:]
            pipeFound = self._checkIfPipeSizeExists(pipeTag, pipeSize)
            if pipeFound:
                break

        index = self._scheduleIndex
        thicknessesForPipe = self._scraper.findAll(self._pipeSizeTargetTag, "td")
        pipeThickness = float(thicknessesForPipe[index].text.split()[1][1:-1])

        return pipeThickness


    def _checkTrunnion(self):
        pipeSchedule = self._scheduleComboPipeVar.get()
        pipeSize = self._pipeComboVar.get()
        pipeOuterDiameter = self._pipeSizes[int(pipeSize)][1]
        pipeWallThk = self._getWallThk(pipeSchedule, pipeSize)
        pipeMillTol = float(self._millTolPipeVar.get())
        corrAllow = float(self._corrVar.get())

        pipeData = [pipeOuterDiameter, pipeWallThk, pipeMillTol, corrAllow]

        trunnionSchedule = self._scheduleComboTrunnVar.get()
        trunnionSize = self._trunnionComboVar.get()
        trunnionOuterDiameter = self._pipeSizes[int(trunnionSize)][1]
        trunnionWallThk = self._getWallThk(trunnionSchedule, trunnionSize)
        trunnionMillTol = float(self._millTolTrunnVar.get())
        trunnionHeight = self._heightVar.get()
        repadThk = float(self._repadVar.get())
        typeOfTrunnion = self._elbowVar.get()

        trunnionData = [trunnionOuterDiameter, trunnionWallThk, trunnionMillTol,
                        trunnionHeight, repadThk, typeOfTrunnion]

        yieldStrength = self._yieldVar.get()
        hotStress = self._hotStressVar.get()

        materialData = [yieldStrength, hotStress]

        calc = TrunnionCalc(pipeData, trunnionData, materialData)

        pressure = self._pressureVar.get()
        axialForce = self._axialForceVar.get()
        circumForce = self._circumForceVar.get()
        lineForce = self._lineForceVar.get()

        calc.checkTrunnion(pressure, axialForce, circumForce, lineForce)
        self._makeOutputFrame()

    def _makeOutputFrame(self):


    def _setTrunnionSizesAtStart(self):
        pipeIndex = self._pipeCombo.current()
        pipeSizes = list(self._pipeSizes.keys())[:pipeIndex]
        self._trunnionCombo["values"] = pipeSizes
        self._trunnionCombo.current(pipeIndex - 1)

    def _setTrunnionSizes(self, event):
        pipeIndex = self._pipeCombo.current()
        pipeSizes = list(self._pipeSizes.keys())[:pipeIndex]
        self._trunnionCombo["values"] = pipeSizes
        self._trunnionCombo.current(pipeIndex - 1)

    def _setPipeSizes(self):
        pipeSizes = list(self._pipeSizes.keys())
        self._pipeCombo["values"] = pipeSizes
        self._pipeCombo.current(4)

    def _setSchedule(self, widget):
        schedules = ["5s", "10", "10s", "20", "30", "40", "40s", "STD", "80", "80s", "100", "120",
                     "140", "160", "XXS"]
        widget["values"] = schedules
        widget.current(0)







root = Tk()
myGUI = trunnionGUI(root)
root.mainloop()
