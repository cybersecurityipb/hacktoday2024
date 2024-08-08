#!/usr/bin/env python3

input = input()

if input.count('n') > 1 or input.count('o') > 1 or '__' in input or any([c for c in input if c in __import__('string').whitespace]) or not all(c in __import__('string').printable for c in input):
    print('no')
    exit()

print = print
eval = eval

__builtins__.__dict__.clear()
print(eval(input, {'__builtins__': {}}, {'__builtins__': {}}))

