from functools import lru_cache
def z1_1(mylist):
    result = []
    def f(lst):
        if isinstance(lst,(int, str)):
            result.append(str(lst))
        elif isinstance(lst, list):
            for i in lst:
                f(i)

    f(mylist)
    result.append('None')
    return ' -> '.join(result)



def z1_2(mylist):
    result = []
    lst = [mylist]

    while lst:
        cur = lst.pop(0)

        if isinstance(cur, list):
            lst.extend(cur)
        else:
            result.append(str(cur))

    result.append('None')
    return ' -> '.join(result)






def z2_1(x):
    def a(i):
        if i == 0 or i == 1:
            return 1
        else:
            return a(i - 2) + (a(i - 1) / (2 ** (i - 1)))

    for n in range(x + 1):
        a(n)
    return f"a{x} = {a(x)}"


@lru_cache()
def z2_2(x):
    a = []
    a.append(1)
    a.append(1)
    for i in range(2, x + 1):
        nu = a[i - 2] + (a[i - 1] / (2 ** (i - 1)))
        a.append(nu)

    return f"a{x} = {a[x]}"
