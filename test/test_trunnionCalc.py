from trunnionCalc import TrunnionCalc

# pipedata input
pipeOutDia = 273.05
pipeThk = 3.404
millTol = 12.5
corrAllow = 1
pipeData = [pipeOutDia, pipeThk, millTol, corrAllow]

# trunnion input
trunnionOutDia = 219.08
trunnionThk = 2.769
trunnionHeight = 100
repadThk = 3.404
typeOfTrunnion = "pipe"
trunnionData = [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion]

# material data
hotStress = 150

calc = TrunnionCalc(pipeData, trunnionData, hotStress)

def test_trunnionCalc_trunnion_area():
    pass