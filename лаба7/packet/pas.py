def benz(type):
    if type.lower() in 'бенз':
        return 1
    return 0

def diz(type):
    if type.lower() in 'диз':
        return 1
    return 0

def pas(type, np, bg, d, v):
    p = 61.5 * benz(type) + 70.5 * diz(type)
    base_rate = 22 * benz(type) + 25 * diz(type)
    extra_rate = 0.01 * (np * 70 + bg) / 100
    total_rate = base_rate + extra_rate
    q = round((d / 100) * total_rate, 2)
    c = round(q * p, 2)
    t = round(d / v, 2)
    return q, c, t

# type = input('какой тип топлива?: бенз/диз ')
# np = int(input('сколько пассажиров?: '))
# bg = int(input('какой вес багажа (кг)?: '))
# d = int(input('какое расстояние (км)?: '))
# v = int(input('какая была скорость (км/ч)?: '))
