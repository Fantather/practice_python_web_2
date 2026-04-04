l = [1,2,3,4,5]

for item in l:
    print(item)

set_iter = iter({1,2,3,4,5})
print(next(set_iter))


"""
Основные методы итератора
__next()__
__getitem()__
__iter()__
"""

print("GENERATOR")
def num_generator(seed:int=0, limit:int = 100):
    item = seed
    while item < limit:
        item += 1
        yield item * 2

g = num_generator(limit=5)
print(next(g))

try:
    for i in range(9):
        print(next(g))
except StopIteration: pass

"""
Каждый for под капотом останавливается исключением stop iteration, просто for его отлавливает
"""

print("File strings generator: ")
def file_generator(file_path:str):
    with open(file_path, 'r') as file:
        for line in file:
            yield line

fg = file_generator("file.txt")

try:
    while True:
        print(next(fg))
except StopIteration: pass

g = (x ** 2 for x in range(20) if x%2 == 0)
"""
Генераторное выражение
"""

for item in g:
    print(item)