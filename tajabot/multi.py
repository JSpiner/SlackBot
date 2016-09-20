from multiprocessing import Pool
import time

def f(x):
    print(x)
    return x*x

pool = Pool(processes=8)

pool.map(f, range(0,100))
