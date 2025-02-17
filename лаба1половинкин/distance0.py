#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов
def main():
    sites = {
        'Moscow': (550, 370),
        'London': (510, 510),
        'Paris': (480, 480),
    }

    # Составим словарь словарей расстояний между ними
    # расстояние на координатной сетке - ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    distances = {}

    city = list(sites.keys())

    for i in range(len(city)):
        for j in range(i + 1, len(city)):
            x1 = sites[city[i]][0]
            y1 = sites[city[i]][1]
            x2 = sites[city[j]][0]
            y2 = sites[city[j]][1]
            distance = (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 0.5
            distances[str(city[i]) + '-' + str(city[j])] = distance


    print( distances)
    return '=========================================================='

# TODO здесь заполнение словаря
print(main())

