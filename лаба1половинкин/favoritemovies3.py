#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов
def main():

    my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

    # Выведите на консоль с помощью индексации строки, последовательно:
    #   первый фильм
    #   последний
    #   второй
    #   второй с конца

    # Запятая не должна выводиться.  Переопределять my_favorite_movies нельзя
    # Использовать .split() или .find()или другие методы строки нельзя - пользуйтесь только срезами,
    # как указано в задании!

    # TODO здесь ваш код
    print (my_favorite_movies[:10] + "\n"  + my_favorite_movies[12:25] + "\n"  + my_favorite_movies[27:33] + "\n"  + my_favorite_movies[35:40] + "\n"  + my_favorite_movies[42:])
    return '=========================================================='
print(main())