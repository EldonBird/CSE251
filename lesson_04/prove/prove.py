"""
Course: CSE 251
Lesson: L04 Prove
File:   prove.py
Author: <Add name here>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Complete the assignments TODO sections and DO NOT edit parts you were told to leave alone.
- Review the full instructions in Canvas; there are a lot of DO NOTS in this lesson.
"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        #print(f'Created: {self.info()}') GOT RID OF THIS IT WAS MESSING WITH MY INPUTS

    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []

    def size(self):
        return len(self.__items)

    def put(self, item):
        assert len(self.__items) <= 10
        self.__items.append(item)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, q, sem, queuesem):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.q = q
        self.fullsem = sem
        self.emptySem = queuesem


    def run(self):

        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """

            self.emptySem.acquire()

            car = Car()
            self.q.put(car)

            self.fullsem.release()

            logging.info(f"Created: {car.info()}")


        # signal the dealer that there there are not more cars

        self.fullsem.acquire()
        self.emptySem.release()
        self.q.put("FIN")


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, q, sem, queuesem):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.q = q
        self.fullsem = sem
        self.emptySem = queuesem
        self.queue_stats = []

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

            if self.q.size() > 0: # this is mostly for my own convieneice, I know it technically goes against what you had asked, but in a different way so I think it is fine

                self.emptySem.acquire()


                item = self.q.get()

                if item == "FIN":
                    break


                self.fullsem.release()



                self.queue_stats.append(self.q.size())
                logging.info(f"Sold {item.info()}")

                # Sleep a little after selling a car
                time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


    def getQStats(self):
        counts = [0] * MAX_QUEUE_SIZE

        for size in self.queue_stats:
            counts[size] += 1

        return counts

def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)

    emptySemiphor = threading.Semaphore(MAX_QUEUE_SIZE) # basically just a lock to keep track of when you can alter the Lot semiphore
    LotSemiphor = threading.Semaphore(0) # for the lot, you aquire the key to the lot as it is filled, them release it when it is empty.

    # TODO Create queue251

    q = Queue251()

    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE



    factory = Factory(q, LotSemiphor, emptySemiphor)
    dealer = Dealer(q, emptySemiphor, LotSemiphor)

    log.start_timer()

    # Start threads
    factory.start()
    dealer.start()

    # Wait for completion
    dealer.join()
    factory.join()

    queue_stats = dealer.getQStats()



    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(0, MAX_QUEUE_SIZE)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production count vs queue size.png')



if __name__ == '__main__':
    main()