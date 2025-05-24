'''
    This file contains the class definition for the StrawHat class.
'''
# chances of error: 
# 
# comp3 me



from crewmate import Crewmate
from heap import Heap
from treasure import Treasure
from custom import *
def comp3(t1, t2):
        if t1.arrival_time + t1.size > t2.arrival_time + t2.size:
            return False
        elif t1.arrival_time + t1.size < t2.arrival_time + t2.size:
            return True
        else:
            if t1.id < t2.id:
                return True

class StrawHatTreasury:
    def __init__(self, m):
        self.crewmates = CrewmateHeap()
        self.treasures = []
        self.current_time = 0

        for _ in range(m):
            crewmate = Crewmate()
            self.crewmates.insert(crewmate)

    def add_treasure(self, treasure):
        least_loaded_crewmate = self.crewmates.extract_min()
        treasure.set_original_time()  # Set the original size when adding the treasure
        least_loaded_crewmate.treasures.append(treasure)
        least_loaded_crewmate.load = treasure.size + max(least_loaded_crewmate.load, treasure.arrival_time)
        self.crewmates.insert(least_loaded_crewmate)
        self.treasures.append(treasure)

    def get_completion_time(self):
        self.final_list = []
        for crewmate in self.crewmates:
            treasures_list = crewmate.treasures

            imp_list = Heap(comp3)
            t1 = 0
            t2 = 0
            for treasure in treasures_list:
                t2 = treasure.arrival_time
                while t2 - t1 > 0:
                    if imp_list.is_empty():
                        t1 = t2
                        imp_list.insert(treasure)
                        break
                    temp_tres = imp_list.extract()
                    if t2 - t1 < temp_tres.size:
                        temp_tres.size -= t2 - t1
                        t1 = t2
                        imp_list.insert(temp_tres)
                        imp_list.insert(treasure)
                        break
                    if t2 - t1 >= temp_tres.size:
                        t1 += temp_tres.size
                        temp_tres.size = 0
                        temp_tres.completion_time = t1
                        temp_tres.reset_size()  # Reset the size before appending
                        self.final_list.append(temp_tres)

            while not imp_list.is_empty():
                temp = imp_list.extract()
                t2 += temp.size
                temp.completion_time = t2
                temp.reset_size()  # Reset the size before appending
                self.final_list.append(temp)

        return sorted(self.final_list, key=lambda t: t.id)