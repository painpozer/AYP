#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров
def main():
    goods = {
        'Лампа': '12345',
        'Стол': '23456',
        'Диван': '34567',
        'Стул': '45678',
    }

    # Есть словарь списков количества товаров на складе.

    store = {
        '12345': [
            {'quantity': 27, 'price': 42},
        ],
        '23456': [
            {'quantity': 22, 'price': 510},
            {'quantity': 32, 'price': 520},
        ],
        '34567': [
            {'quantity': 2, 'price': 1200},
            {'quantity': 1, 'price': 1150},
        ],
        '45678': [
            {'quantity': 50, 'price': 100},
            {'quantity': 12, 'price': 95},
            {'quantity': 43, 'price': 97},
        ],
    }

    # Рассчитать на какую сумму лежит каждого товара на складе
    # например для ламп

    lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
    # или проще (/сложнее ?)
    lamp_code = goods['Лампа']
    lamps_item = store[lamp_code][0]
    lamps_quantity = lamps_item['quantity']
    lamps_price = lamps_item['price']
    lamps_cost = lamps_quantity * lamps_price
    print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')



    # Вывести стоимость каждого вида товара на складе:
    # один раз распечать сколько всего столов и их общая стоимость,
    # один раз распечать сколько всего стульев и их общая стоимость,
    #   и т.д. на складе
    # Формат строки <товар> - <кол-во> шт, стоимость <общая стоимость> руб

    # WARNING для знающих циклы: БЕЗ циклов. Да, с переменными; да, неэффективно; да, копипаста.
    # Это задание на ручное вычисление - что бы потом понять как работают циклы и насколько с ними проще жить.

    # TODO здесь ваш код
    table_code = goods['Стол']
    table_item1 = store[table_code][0]
    table_quantity1 = table_item1['quantity']
    table_price1 = table_item1['price']
    table_cost1 = table_quantity1 * table_price1

    table_item2 = store[table_code][1]
    table_quantity2 = table_item2['quantity']
    table_price2 = table_item2['price']
    table_cost2 = table_quantity2 * table_price2

    table_quantity = table_quantity1 + table_quantity2
    table_cost = table_cost1 + table_cost2
    print('Стол -', table_quantity, 'шт, стоимость', table_cost, 'руб')

    arm_code = goods['Диван']
    arm_item1 = store[arm_code][0]
    arm_quantity1 = arm_item1['quantity']
    arm_price1 = arm_item1['price']
    arm_cost1 = arm_quantity1 * arm_price1

    arm_item2 = store[arm_code][1]
    arm_quantity2 = arm_item2['quantity']
    arm_price2 = arm_item2['price']
    arm_cost2 = arm_quantity2 * arm_price2

    arm_quantity = arm_quantity1 + arm_quantity2
    arm_cost = arm_cost1 + arm_cost2
    print('Диван -', arm_quantity, 'шт, стоимость', arm_cost, 'руб')

    chair_code = goods['Стул']
    chair_item1 = store[chair_code][0]
    chair_quantity1 = chair_item1['quantity']
    chair_price1 = chair_item1['price']
    chair_cost1 = chair_quantity1 * chair_price1

    chair_item2 = store[chair_code][1]
    chair_quantity2 = chair_item2['quantity']
    chair_price2 = chair_item2['price']
    chair_cost2 = chair_quantity2 * chair_price2

    chair_item3 = store[chair_code][2]
    chair_quantity3 = chair_item3['quantity']
    chair_price3 = chair_item3['price']
    chair_cost3 = chair_quantity3 * chair_price3

    chair_quantity = chair_quantity1 + chair_quantity2 + chair_quantity3
    chair_cost = chair_cost1 + chair_cost2 + chair_cost3
    print('Диван -', chair_quantity, 'шт, стоимость', chair_cost, 'руб')
    return '=========================================================='
print(main())