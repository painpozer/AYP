def benz(type):
    if type.lower() in 'бенз':
        return 1
    return 0

def diz(type):
    if type.lower() in 'диз':
        return 1
    return 0

def leg(type, d, v, np, bg):
    p = 61.5 * benz(type) + 70.5 * diz(type)
    base_rate = 8.2 * benz(type) + 7.6 * diz(type)
    load = np * 70 + bg
    extra_multiplier = 1 + 0.005 * (load / 100)
    q = round((base_rate / 100) * d * extra_multiplier * 1.01, 2)
    c = round(q * p, 2)
    t = round(d / v, 2)
    return q, c, t

# type = input('какой тип топлива?: бенз/диз ')
# d = int(input('какое расстояние поездки (в км)?: '))
# v = int(input('какая была скорость (в км/ч)?: '))
# np = int(input('сколько пассажиров (без водителя)?: '))
# bg = int(input('вес багажа (в кг)?: '))
