def call_limit(max_calls, prod=False):
    def decorator(func):
        count = 0
        def wrapper(value):
            nonlocal count
            if count >= max_calls:
                if prod:
                    print('Лимит превышен, но мы продолжаем')
                else:
                    print("Лимит превышен, остановка выполнения")
                    return None
            count += 1
            return func(value)
        return wrapper
    return decorator

def unique_closure(max_calls, prod):
    seen = set()
    add = []
    @call_limit(max_calls, prod)
    def add_unique(value):
        if value in seen:
            print(f"{value} уже добавлен, пропускаем")
        else:
            seen.add(value)
            add.append(value)
            print(f"{value} добавлен")
        return add
    return add_unique

def str_to_bool(s):
    return s.lower() in ('true')

max_calls = int(input("Максимальное число вызовов: "))
prod_input = input("Продолжить выполнение при превышении лимита? (True/False): ")
prod = str_to_bool(prod_input)

values_input = input("Введите значения через пробел: ")
test_values = [int(x) for x in values_input.split()]

unique_selector = unique_closure(max_calls, prod)
for val in test_values:
    result = unique_selector(val)
    print("Результат:", result)
