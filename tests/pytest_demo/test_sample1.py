import pyDef_samp1 as pDef

# content of test_sample.py
def test_addone():
    assert pDef.addone(5) == 6

def test_addition():
    assert pDef.add(2, 3) == 5
    assert pDef.add(-1, 1) == 0
    assert pDef.add(0, 0) == 0
    assert pDef.add(0, 99.9) == 99.9

def test_subtraction():
    assert pDef.subtract(5, 2) == 3
    assert pDef.subtract(10, 5) == 5
    assert pDef.subtract(0, 0) == 0


from pyCla_samp1 import Calculator

def test_calculator_addition():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0