"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(sem, q):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue

        input = q.get()

        if input == NO_MORE_VALUES:
            break

        else:
            response = requests.get(input)

            if(response.status_code == requests.codes.ok):
                print(response.json())



        # TODO process the value retrieved from the queue


        # TODO make Internet call to get characters name and log it



        pass



def file_reader(sem, q): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    with open("urls.txt") as file:
        for line in file:
            q.put(line)

    #log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"

    for i in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)




def main():
    """ Main function """


    log = Log(show_terminal=True)

    # TODO create queue

    q = queue.Queue()

    # TODO create semaphore (if needed)

    sem = threading.Semaphore(RETRIEVE_THREADS)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    getter = threading.Thread(target=file_reader, args=(sem, q))


    threads = [threading.Thread(target=retrieve_thread, args=(sem, q)) for _ in range(RETRIEVE_THREADS)]


    getter.start()
    getter.join()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    log.start_timer()


    # TODO Wait for them to finish - The order doesn't matter

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()



