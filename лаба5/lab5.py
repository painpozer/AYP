from math import pi
def generator(n):
    digits = str(pi).replace('.', '')
    count = 0
    for d in digits:
        if d != '0':
            yield int(d)
            count += 1
            if count == n:
                break
def z(n):
    mapped_values = map(lambda x: x / (x ** 2), generator(n))
    result = sum(mapped_values)
    return f"Сумма значений: {result}"
#m = int(input())
#print(z(m))