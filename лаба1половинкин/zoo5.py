#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# есть список животных в зоопарке
def main():
        
    zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]

    # посадите медведя (bear) между львом и кенгуру
    #  и выведите список на консоль
    # TODO здесь ваш код
    zoo.insert(1,'bear')
    print(zoo)
    # добавьте птиц из списка birds в последние клетки зоопарка
    birds = ['rooster', 'ostrich', 'lark', ]
    #  и выведите список на консоль
    # TODO здесь ваш код
    zoo.extend(birds)
    print(zoo)
    # уберите слона
    #  и выведите список на консоль
    # TODO здесь ваш код
    zoo.remove('rooster')
    print(zoo)
    # выведите на консоль в какой клетке сидит лев (lion) и жаворонок (lark).
    # Номера при выводе должны быть понятны простому человеку, не программисту.
    # TODO здесь ваш код
    print(zoo.index('lion') + 1,',',zoo.index('lark') + 1)
    return '=========================================================='
print(main())