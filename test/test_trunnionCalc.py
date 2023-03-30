from trunnionCalc import TrunnionCalc
import pytest

# pipedata default input
pipeOutDia = 273.05
pipeThk = 3.404
millTol = 12.5
corrAllow = 1
#pipeData = [pipeOutDia, pipeThk, millTol, corrAllow]

# trunnion default input
trunnionOutDia = 219.08
trunnionThk = 2.769
trunnionHeight = 100
repadThk = 3.404
typeOfTrunnion = "pipe"
#trunnionData = [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion]

# material default data
hotStress = 150

@pytest.mark.parametrize(
    "thickness, corrAllow, repad, type, output", [
        (pipeThk, 0, repadThk, "pipe", 5.957),
        (12.785, 1, 0, "pipe", 11.187),
    ]
)
def test_trunnionCalc_get_minimum_pipe_thk_for_pipe(thickness, corrAllow, repad, type, output):
    calc = TrunnionCalc([pipeOutDia, thickness, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repad, typeOfTrunnion], hotStress)
    assert calc._get_minimum_pipe_thk(type) - output < 0.001

@pytest.mark.parametrize(
    "thickness, type, output", [
        (trunnionThk, "trunnion", 2.429),
        (41.275, "trunnion", 36.116)
    ]
)
def test_trunnionCalc_get_minimum_pipe_thk_for_trunnion(thickness, type, output):
    calc = TrunnionCalc([pipeOutDia, thickness, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion], hotStress)
    assert calc._get_minimum_pipe_thk(type) - output < 0.001

@pytest.mark.parametrize(
    "trunnionOutDia, trunnionThk, output", [
        (trunnionOutDia, trunnionThk, 1649.126),
        (508.00, 5.537, 7658.339)
    ]
)
def test_trunnionCalc_get_trunnion_area(trunnionOutDia, trunnionThk, output):
    calc = TrunnionCalc([pipeOutDia, pipeThk, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion], hotStress)
    assert calc._get_trunnion_area() - output < 0.001

@pytest.mark.parametrize(
    "typeOfTrunnion, output", [
        (typeOfTrunnion, 1.5),
        ("elbow", 1)
    ]
)
def test_trunnionCalc_get_allowable_stress_factor(typeOfTrunnion, output):
    calc = TrunnionCalc([pipeOutDia, pipeThk, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion], hotStress)
    assert calc._get_allowable_stress_factor() == output

@pytest.mark.parametrize(
    "trunnionOutDia, trunnionThk, output", [
        (trunnionOutDia, trunnionThk, 110793.174),
        (406.40, 9.525, 1059868.667)
    ]
)
def test_trunnionCalc_get_section_modulus(trunnionOutDia, trunnionThk, output):
    calc = TrunnionCalc([pipeOutDia, pipeThk, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion], hotStress)
    assert calc._get_section_modulus() - output < 0.001

@pytest.mark.parametrize(
    "trunnionOutDia, height, pressure, fa, fc, fl, Ffa, Ffc, Ffl", [
        (trunnionOutDia, trunnionHeight, 10, 2000, 1500, 3000, 2.906),
        (406.40, 9.525, 1059868.667)
    ]
)
def test_calculate_line_loads(trunnionOutDia, height, pressure, fa, fc, fl, Ffa, Ffc, Ffl):
    calc = TrunnionCalc([pipeOutDia, pipeThk, millTol, corrAllow],
                        [trunnionOutDia, trunnionThk, millTol, trunnionHeight, repadThk, typeOfTrunnion], hotStress)
    calc.check_trunnion(pressure, fa, fc, fl) # check_trunnion() will call _calculate_line_loads()
    assert calc.Ffa - Ffa < 0.001
    assert calc.Ffc - Ffc < 0.001
    assert calc.Ffl - Ffl < 0.001

