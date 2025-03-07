"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: <Add your name here>

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 2

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function

def read_data_txt(filename, q):

    with open(filename, 'r') as f:
        for line in f:

            gohere = int(line)

            q.put(gohere)

    for i in range(PRIME_PROCESS_COUNT):
        q.put("FIN")




# TODO create prime_process function

def prime_process(q, output):
    while True:
        input = q.get()
        print(input)

        if input == "FIN":
            return

        if is_prime(input):
            output.append(input)
            print(f"FOUND ___: {input} :___")



def create_data_txt(filename):
    # only create if it doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    # Create the data file for this demo if it does not already exist.
    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures

    q = mp.Queue()

    output = mp.Manager().list()

    # TODO create reading thread

    readingthread = threading.Thread(target=read_data_txt, args=(filename, q))

    # TODO create prime processes

    threads = []

    for i in range(PRIME_PROCESS_COUNT):
        primethread = threading.Thread(target=prime_process, args=(q, output))
        threads.append(primethread)


    # TODO Start them all

    readingthread.start()

    for t in threads:
        t.start()

    # TODO wait for them to complete

    readingthread.join()

    for t in threads:
        t.join()

    primes = output

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
