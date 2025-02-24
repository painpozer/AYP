from itertools import product
print('---------------------------')

def z1 ():
    """
    >>> z1()
    6075
    """
    k=0
    for i in product('НАСТЯ', repeat=6):
        if i.count('А') <= 1 and i.count('Я') <= 1:
         k+=1
    return k
print(z1())

print('---------------------------')

def z2():
    """
    >>> z2()
    7
    """
    x = 16 ** 18 + 4 ** 10 - 46 - 16
    s = ''
    while x != 0:
        s += str(x % 4)
        x //= 4
    s = s[::-1]
    return (s.count("3"))
print(z2())

print('---------------------------')

def z3():
    """
    >>> z3()
    452025 150678
    452029 23810
    452034 226019
    452048 226026
    452062 226033
    ''
    """

    def m(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return i + n // i
        return 0
    k = 0
    for i in range(452021 + 1, 10000000000000):
        if m(i) % 7 == 3:
            print(i, m(i))
            k += 1
        if k == 5:
            break
    return ''
print(z3())

print('---------------------------')