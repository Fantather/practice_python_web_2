"""
Замыкания
"""

#LEGB (BGEL)
"""
- built - in - доступны в любом файле и модуле (Что такое модули), это функции и переменные, которые используются Python и мы можем обращаться к ним в любом месте модуля
-- Global - видимость всех элементов в рамках одного модуля, в котором именно эти элементы были созданы, функции, переменные, речь о них
--- Enclosure - 
---- Local - это функции, всё что есть в теле функции считается локальным
"""

x = 10 # Global, всё что тут создаётся оказывается в Heap

def sample():
    #print(x) # Будет исключение, потому что переменная создаётся в этой функции, но ещё не определена
    x = 5
    print("Local x: ", x)

sample()
print("Global x: ", x) # Получили 10, потому что x внутри функции воспринимается как локальная переменная

def change_global():
    global x
    x = 20
    print("Change x value: ", x)

change_global()
print("Global x:", x)


print("-"*10, "Local variables", "-"*10)

def outer_func():
    x = 10
    print("Outer X:", x)

    def inner_func():
        nonlocal x  # Если указать тут global, то будет обращаться к глобальному x, а не к внешнему, что бы обратится к x во внешней функции есть nonlocal
        x = 20
        print("Inner X:", x)

    inner_func()
    print("Outer(again) X:", x)

outer_func()


print("-"*10, "Closure", "-"*10)
# Замыкание это?
# По простому, замыкание это функция, которая запоминает своё лексическое окружение
# На пример наш start, мы к нему обращаемся, и Python видит, что на переменную start всё ещё существует ссылка и сохраняет это значение в специальной области памяти для замыканий, вместо удаления
def outer(start:int = 10):
    def innner():
        nonlocal start
        start -= 1
        print(start)
    return innner


inner = outer()
inner()

# Можно создать полноценный Storage, не используя класс Storage, только функции
def make_storage():
    data = []

    push_data = lambda value: data.append(value)
    print_all_data = lambda: print(data)

    def remove_item(item):
        if item in data:
            data.remove(item)

    return push_data, print_all_data, remove_item

(push, show, delete) = make_storage()
push("Test")
show()
delete("Test")