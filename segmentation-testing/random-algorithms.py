#!/usr/bin/env python3

def fibonnaci(n):
    a, b = 0, 1
    while(a < n):
        print(a, end=' ')
        a, b = b, a+b
    print()

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

fibonnaci(100)
print(factorial(6))