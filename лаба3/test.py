from lab3 import z1_1
from lab3 import z1_2
from lab3 import z2_1
from lab3 import z2_2
def test_z1_1():
    assert z1_1([1, [2, [3, [4, [5]]]]]) == '1 -> 2 -> 3 -> 4 -> 5 -> None'
def test_z1_2():
    assert z1_2([1, [2, [3, [4, [5]]]]]) == '1 -> 2 -> 3 -> 4 -> 5 -> None'
def test_z2_1():
    assert z2_1(9) == 'a9 = 1.51309497623879'
def test_z2_2():
    assert z2_2(9) == 'a9 = 1.51309497623879'


