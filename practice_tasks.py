"""1. Декоратор для перевірки аргументів функції: Створіть декоратор, який перевіряє типи аргументів функції. Якщо тип аргументу не відповідає очікуваному, викидається виключення.

2. Декоратор для кешування результатів: Напишіть декоратор, який буде кешувати результати функції. Якщо функція викликається з однаковими аргументами, результат має повертатися з кешу, а не обчислюватися повторно.

3. Декоратор для контролю доступу (логін): Напишіть декоратор, який перевіряє, чи авторизований користувач. Якщо ні — викидає виключення. Як аргумент функція буде приймати інформацію про користувача.

4. Декоратор для повторного виконання функції при виключенні: Створіть декоратор, який повторює виконання функції у разі виникнення виключення. Кількість спроб і інтервал між ними мають передаватися як параметри декоратора.

5. Генератор чисел Фібоначчі: Напишіть генератор, який буде повертати числа Фібоначчі. Генератор має безкінечно генерувати числа Фібоначчі, поки його не зупинять.

6. Генератор чисел, що діляться на 3 або 5: Напишіть генератор, який буде генерувати числа, що діляться на 3 або 5, починаючи з 1 і до заданої межі.

7. Напишіть генератор, який обчислює послідовність факторіалів для чисел від 1 до нескінченності.

8. Напишіть генератор, який повертає лише кожен n-й елемент із заданого списку.

9. Напишіть замикання, яке дозволяє викликати передану функцію не більше n разів. Після перевищення ліміту має повертатися помилка або повідомлення.

10. Створіть замикання, яке приймає список чисел і повертає функцію, що перевіряє, чи належить число цьому списку.

11. Напишіть замикання, яке приймає шаблон рядка і повертає функцію, яка форматує рядок за цим шаблоном.

12. Створіть замикання, яке приймає число і повертає різницю між цим числом і попереднім викликом функції.

13. Напишіть замикання, яке рахує, скільки разів функція була викликана з кожним унікальним аргументом."""


#1
from collections.abc import Iterator
from functools import wraps
import inspect
from typing import Any, Callable

def validate_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        # Сначала привязываем аргументы
        bound = sig.bind(*args, **kwargs)
        
        # Заполняем значения по умолчанию
        bound.apply_defaults()

        # Получаем словарь со значениями и ключами
        args_dict = bound.arguments

        # Получаем названия переменных и ожидаемые типы
        annotations = func.__annotations__

        for name, expected_type in annotations.items():
            if name == "return":
                continue

            if not isinstance(args_dict[name], expected_type):
                 raise TypeError(f"В метод {func.__name__} передан аргумент {name} с не верным типом")
        
        result = func(*args, **kwargs)
        if "return" in annotations:
            if not isinstance(result, annotations["return"]):
                raise TypeError(f"Метод {func.__name__} не возвращает указанный тип данных")
        
        return result
    
    return wrapper

@validate_types
def test_func(arg:str):
    print("Arg: ", arg)

# test_func(1)

#2
def cached(func):
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = (args, tuple(sorted(kwargs.items())))
        if cache_key in cache:
            return cache[cache_key]
        
        result = func(*args, **kwargs)
        cache[cache_key] =  result
        return result

    return wrapper


#3
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        if not bound.arguments["user"]["is_authenticated"]:
            raise PermissionError("Пользователь не вошёл в систему")
        
        return func(*args, **kwargs)
    
    return wrapper


user_logged = {"username": "alice", "is_authenticated": True}
user_guest = {"username": "guest", "is_authenticated": False}

@require_auth
def delete_post(user):
    print(f"Пост успешно удален пользователем {user['username']}")

# пользователь
delete_post(user_logged)

# гость
try:
    delete_post(user_guest)
except PermissionError as e:
    print(f"Ошибка поймана: {e}")

import time

# 4
def retry(tries:int, delay:int):
    def repeat(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(tries):
                    try:
                        return func(*args, **kwargs)
                
                    except Exception as e: 
                        if attempt == tries - 1:
                            raise e
                        
                        print(f"Ошибка: {e}. Попытка {attempt + 1} из {tries}. Ждем {delay} сек...")
                        time.sleep(delay)
            return wrapper
    return repeat

attempts_made = [0]   
@retry(3, 1)
def connect_to_server():
    attempts_made[0] += 1
    def wrapper():
        if attempts_made[0] < 3:
                print("Попытка подключения к серверу...")
                raise ConnectionError("Сервер не отвечает")
        
        print("Соединение успешно установлено")
        
    wrapper()

connect_to_server()

#5 Потом подумал что сюда могут передать и не 2 числа фибоначчи и всё поломается, но забил
def fibonacci_generator(num1:int = 0, num2:int = 1) -> Iterator[int]:
    while True:
        yield num1
        num1, num2 = num2, num1 + num2

fibonacci_gen = fibonacci_generator()
        
for i in range(10):
    print(f"Fibonacci num: {next(fibonacci_gen)}")


#6
def multiples_of_3_or_5(limit:int):
    num = 1
    while num < limit + 1:
        if num % 3 == 0 or num % 5 == 0:
            yield num
        num += 1

multiple_gen = multiples_of_3_or_5(50)
for num in multiple_gen:
    print(f"Multiple num: {num}")

#7
def factorial_generator() -> Iterator[int]:
    factorial = 1
    current_num = 1
    while True:
        yield factorial
        current_num += 1
        factorial = factorial * current_num

fact_gen = factorial_generator()
for _ in range(5):
  print(f"Factorial num: {next(fact_gen)}")

#8
def seek_element_generator(items:list, step:int) -> Iterator[Any]:
    for i in range(0, len(items), step):
        yield items[i]

#9
def limit_calls(func:Callable[..., Any], limit:int) -> Callable[..., Any]:
    counter = [0]
    def wrapper(*args, **kwargs):
        if counter[0] < limit:
            counter[0] += 1
            return func(*args, **kwargs)

        print("limited_greeting: Количество вызовов исчерпано")
    return wrapper

limited_greeting = limit_calls(lambda: print("HELLO"), 2)
limited_greeting()
limited_greeting()
limited_greeting()

#10
def make_membership_checker(items:list[int]) -> Callable[[int], bool]:
    def wrapper(number:int) -> bool:
        return number in items
    return wrapper

is_in_list = make_membership_checker([1, 2, 3, 5, 8])
print(is_in_list(3))  # True
print(is_in_list(4))  # False

#11
def make_formatter(template: str) -> Callable[..., str]:
    def formatter(*args:Any, **kwargs:Any) -> str:
        return template.format(*args, **kwargs)
    
    return formatter

greet = make_formatter("Привет, {}! Тебе присуждается {} лет строгого режима")
print(greet("Алексей", 25))

#12
def difference_calculator(initial_number:int) -> Callable[[int], int]:
    last_number = [initial_number]

    def calculate(new_number:int = 0):
        result = last_number[0] - new_number
        last_number[0] = new_number
        return result

    return calculate


diff = difference_calculator(10)
print("difference_calculator:", diff(15))
print("difference_calculator:", diff(12))
print("difference_calculator:", diff(20))

#13
def calculate_unique_number(func: Callable) -> Callable:
    registry = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        arg_key = (args, tuple(sorted(kwargs.items())))
        registry[arg_key] = registry.get(arg_key, 0) + 1

        result = func(*args, **kwargs)
        print(f"Аргументы {arg_key} были вызваны {registry[arg_key]} раз")
        return result
    
    return wrapper

@calculate_unique_number
def multiply(a, b):
  return a * b

multiply(2, 3)
multiply(5, 5)
multiply(2, 3)