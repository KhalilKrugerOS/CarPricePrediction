# list comprehension
numbers = [ 2 ** i for i in range(100) if i % 2 == 0 and i % 5 == 0 ]
words = ["khalil", "ahmed", "aziz", "saif"]
new_words = [ "ahla bik! " + word.upper() for word in words ]
print(numbers)
print(new_words)
 

 # map function 

def format(name):
    return f"this is your name : {name}"

print(list(map(format, words)))

# enumerate

for index, name in enumerate(words):
    print(f"{index} : {name}")

# lambda

prod = lambda x, y=5 : x*y
even = lambda x : x % 2 == 0
print(list(filter(prod, numbers)))

# any, all functions
    # any -> true if 1 is truthy
    # all -> true if all are truthy

print(all(numbers))

print(all([even(num) for num in numbers ])) # not all are even

print(list(reversed(numbers)))

# docstrings

def neuralNetwork(f_function, inputs: list[int], neurons: list[any]) -> int :
    '''
    this function imitates one layer of CNN

    :param f_function: non linear function to compute
    :param inputs: number of input signals
    :return: return the sum of the first layer
    '''
    res = [[ f_function(input) for input in inputs] for neuron in neurons ]
    return res

print(neuralNetwork(lambda x: x*2, numbers, [5, 4, 3]))

# zip funtion

age = [ 19, 20, 21, 22]

for i in range(len(age)):
    print(f"{words[i]} has the age {age[i]}")

for name, age in zip(words, age):
    print(f"{name} has the age {age}")

sales = [ 40, 50, 42, 80 ,110]
costs = [ 50 ,40 ,70, 22, 36 ]

flousy = [ sale - cost  for sale, cost in zip(sales, costs)]
print(flousy)

values = [("khalil", 100),("saif", 1000),("aziz", 480)]

names, marbouh = zip(*values)

print(names, marbouh)