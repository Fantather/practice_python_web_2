# Декораторы
"""
Это функция обёртка, которая возвращает какой-либо функционал, другую функцию
"""
def sample(*args, **kwargs):
    print(type(args))
    print(type(kwargs)) # key-word arguments

    if len(args) > 0:
        print("args: ", args)
    print()

    if len(kwargs) > 0:
        print("kwargs: ", kwargs)
    print()

sample(1,2,3,4, *(5,6,7,8), *(), name="user", surname='Due', d={"key1":"value1"}, **{"key2":"value2"}, **{})

def decorator(func):
    # *args **kwargs дают возможность декорировать любую функцию с любыми параметрами или без них 
    def wrapper(*args, **kwargs):
        print("-"*20)
        func(*args, **kwargs)
        print("-"*20)
    return wrapper

# Использование декоратора
# create function
greeting = lambda: print("Hello")

# decorate function
greeting = decorator(greeting)
greeting()

print('\n')

# create function
greet_user = lambda username: print(f"Hello, {username}")
greet_user("William")

greet_user = decorator(greet_user)
greet_user("Will") # Выдаст исключение, потому что метод декоратора не принимает параметры, он и не должен

# Декораторы должны быть максимально униварсальными, он должен быть таким, что бы быть использованным для любой существующей функции

# В пайтоне есть такие конструкции как *args и **kwargs, это два вида аргументов, котоыре мы можем передать в функцию, позиционные и именованные
# args это tuple, kwargs это dict, они работают как заглушки, даже когда мы ничего не передаём, функция успешно вызывается



# автоматическое декорирование функции
print("-"*10, "Автоматическое декорирование функций", "-"*10)

@decorator # Python автоматически декорирует функцию ниже
def sample_text():
    print("Hello")

sample_text()

@decorator
def user_text(text:str):
    print(text)

user_text("text")



# decorator with parameters
from functools import wraps
print("-"*10, "Decorator with params", "-"*10)

def decorator_param(symbol:str = '-'):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(symbol*10)
            r = func(*args, **kwargs)
            print(symbol*10)
            return r
        # wrapper.__name__ = func.__name__
        # wrapper.__doc__ = func.__doc__
        return wrapper
    return decor

def s(param:str = ""):
    """
    This a test function for decorator.
    
    Args:
        param(str): test parameter(optional)
    """
    print("Test,", param)

s = decorator_param("$")(s)
print(s.__name__)
help(s)

@decorator_param("^")
def a():
    print("a function")

a()
print(a.__name__)

@decorator_param()
def b(): return 12

print(b())