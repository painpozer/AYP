def benz(type):
    if type.lower() in 'бенз':
        return 1
    return 0

def diz(type):
    if type.lower() in 'диз':
        return 1
    return 0

def gruz(type, gpr, ggr, d, v):
    p = 61.5 * benz(type) + 70.5 * diz(type)
    base_rate = 35 * benz(type) + 30 * diz(type)
    extra_rate = 0.01 * (gpr + ggr) / 100
    total_rate = base_rate + extra_rate
    q = round((d / 100) * total_rate, 2)
    c = round(q * p, 2)
    t = round(d / v, 2)
    return q, c, t

# type = input('какой тип топлива?: бенз/диз ')
# gpr = int(input('какая масса прицепа (кг)?: '))
# ggr = int(input('какая масса груза (кг)?: '))
# d = int(input('какое расстояние (км)?: '))
# v = int(input('какая была скорость (км/ч)?: '))
