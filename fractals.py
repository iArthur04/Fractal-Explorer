import numpy as np

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return max_iter

def julia(z, c, max_iter):
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return max_iter

# Add a global Julia parameter
JULIA_C = complex(-0.7, 0.27015)

def set_julia_c(c):
    global JULIA_C
    JULIA_C = c

def julia(z, max_iter):
    global JULIA_C
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + JULIA_C
    return max_iter