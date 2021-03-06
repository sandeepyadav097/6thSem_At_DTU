import time
import random
import multiprocessing
import math
import matplotlib.pyplot as plt
import numpy as np

def merge(*args):
    left, right = args[0] if len(args) == 1 else args
    llft = len(left)
    lrgt = len(right)
    lin, rin = 0, 0

    merged = []

    while (lin < llft and rin < lrgt):
        if (left[lin] <= right[rin]):
            merged.append(left[lin])
            lin += 1
        else:
            merged.append(right[rin])
            rin += 1
    if lin == llft :
        merged.extend(right[rin:])
    else:
        merged.extend(left[lin:])
    return merged 
    
def merge_sort(arr):
    length = len(arr)
    if length <= 1 : return arr
    m = int(length//2)
    left = arr[0:m]
    right = arr[m:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

def paraller_merge_sort(arr):
    processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=processes)
    size = int(math.ceil(float(len(arr)) / processes))
    arr = [arr[i * size:(i + 1) * size] for i in range(processes)]
    arr = pool.map(merge_sort, arr)
    # Each partition is now sorted - we now just merge pairs of these
    # together using the worker pool, until the partitions are reduced
    # down to a single sorted result.
    while len(arr) > 1:
        # If the number of partitions remaining is odd, we pop off the
        # last one and append it back after one iteration of this loop,
        # since we're only interested in pairs of partitions to merge.
        extra = arr.pop() if len(arr) % 2 == 1 else None
        arr = [(arr[i], arr[i + 1]) for i in range(0, len(arr), 2)]
        arr = pool.map(merge, arr) + ([extra] if extra else [])
    return arr[0]

def main():
    # n = int(input("Enter the length of array to generate : "))
    # arr = random.sample(range(100000), n)
    # print ("generated array!")
    # for sort in merge_sort, paraller_merge_sort:
    #     start = time.time()
    #     arr_sorted = sort(arr)
    #     end = time.time() - start
    #     print (sort.__name__, end, sorted(arr) == arr_sorted)
    s_x = []
    s_y = []
    p_x = []
    p_y = []
    for i in range(10000,100000,5000):
        arr = random.sample(range(100000),i)
        start = time.time()
        arr_sorted = merge_sort(arr)
        end = time.time() - start
        s_x.append(i)
        s_y.append(end)

        start = time.time()
        arr_sorted = paraller_merge_sort(arr)
        end = time.time() - start
        p_x.append(i)
        p_y.append(end)
        print("Done itr : ",i)
    s_fit = np.polyfit(s_x, s_y,deg=2)
    s_p = np.poly1d(s_fit)
    p_fit = np.polyfit(p_x, p_y,deg=2)
    p_p = np.poly1d(p_fit)
    plt.plot(s_x,s_y, label="Serial Merge sort", color = 'red')
    plt.plot(s_x,s_p(s_x), linestyle="dotted", color = 'red')
    plt.plot(p_x,p_y, label="Parallel Merge sort")
    plt.plot(p_x,p_p(p_x), linestyle="dotted")
    plt.xlabel('Input size')
    plt.ylabel('Time')
    plt.title("Comparision on parallel and serial merge sort")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
