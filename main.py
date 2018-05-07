import random
from Classes import *
from math import ceil, log2

Group.groups = [Group("a", 10), Group("b", 20), Group("c", 30), Group("d", 10), Group("e", 40)]

Professor.professors = [Professor("mutaqi"), Professor("khalid"), Professor("zafar"),
                        Professor("basit"), Professor("khalid_zaheer")]

Course.courses = [Course("hu100"), Course("mt111"), Course("hu160"),
                  Course("ch110"), Course("cs101"), Course("cs152")]

Room.rooms = [Room("lt1", 20), Room("lt2", 40)]

Slot.slots = [Slot("08:30", "10:00", "Mon"), Slot("10:15", "11:45", "Mon"),
              Slot("12:00", "13:30", "Mon")]



# TODO
# 0.  Running Simplified Class Scheduling - Done
# 0.5 Problem Instance to Binary String - Done
# 1.  Multiple days - Done
# 2.  Class Size - Done
# 2.5 One group can attend only one class at a time
# 3.  Multiple classes
# 4.  Duration
# 5.  Lab

# cpg = ["000000", "010001", "100100", "111010"] # course, professor, student group pair
# lts = ["00", "01"] # lecture theatres
# slots = ["00", "01"] # time slots


max_score = 300


# ######### Chromosome ##############
# <Course, Prof, Group, Slot, LT>   #
# ###################################

cpg = []
lts = []
slots = []

def bits_needed(x):
    return int(ceil(log2(len(x))))


def binary_converter(x):
    bit_repr = {}
    for i in range(len(x)):
        keys = list(x.keys())
        bit_repr[keys[i]] = (bin(i)[2:]).rjust(bits_needed(x), '0')
    return bit_repr


def join_cpg_pair(cpg):
    res = []
    for i in range(0, len(cpg), 3):
        res.append(cpg[i] + cpg[i + 1] + cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, lts, slots

    cpg = [Course.find("hu100"), Professor.find("mutaqi"), Group.find("a"),
           Course.find("mt111"), Professor.find("khalid"), Group.find("a"),
           Course.find("hu160"), Professor.find("mutaqi"), Group.find("b"),
           Course.find("ch110"), Professor.find("zafar"), Group.find("c"),
           Course.find("cs101"), Professor.find("basit"), Group.find("e"),
           Course.find("cs152"), Professor.find("basit"), Group.find("e")]

    for _c in range(len(cpg)):
        if _c % 3:  # Course
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Course.courses), '0')
        elif _c % 3 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
        else:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), '0'))

    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots), '0'))

    print(cpg)
    

def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(Course.courses)]


def professor_bits(chromosome):
    i = bits_needed(Course.courses)

    return chromosome[i: i + bits_needed(Professor.professors)]


def group_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors)

    return chromosome[i:i + bits_needed(Group.groups)]


def slot_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups)

    return chromosome[i:i + bits_needed(Slot.slots)]


def lt_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors) +\
        bits_needed(Group.groups) + bits_needed(Slot.slots)

    return chromosome[i: i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    clashes = []
    for i in range(len(chromosome) - 1):  # select one cpg pair
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and professor_bits(chromosome[i]) == professor_bits(chromosome[j]):
                # print("These profs. have clash")
                clashes.append([chromosome[i], chromosome[j]])
    return (len(chromosome) * 100 - len(clashes) * 100) / len(cpg)


# checks that a course is assigned to an available classroom. 
def use_classroom_available_time(chromosome):
    clashes = []
    for i in range(len(chromosome) - 1):  # select one cpg pair
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                # print("These classes have slot/lts clash")
                # printChromosome(chromosome[i])
                # printChromosome(chromosome[j])
                clashes.append([chromosome[i], chromosome[j]])
    return (len(chromosome) * 100 - len(clashes) * 100) / len(cpg)


# checks that the classroom capacity is large enough for the courses that
# are assigned to that classroom.
def classroom_size(chromosome):
    points = 0
    problems = 0
    if type(chromosome) == str:
        if Group.groups[int(group_bits(chromosome), 2)].size > Room.rooms[int(lt_bits(chromosome), 2)].size:
            problems = problems + 1
        else:
            points = points + 100
    else:
        for _c in chromosome:
            if Group.groups[int(group_bits(_c), 2)].size > Room.rooms[int(lt_bits(_c), 2)].size:
                problems = problems + 1
            else:
                points = points + 100
    return points / len(cpg)


def evaluate(chromosome):
    score = 0
    score = score + use_classroom_available_time(chromosome)
    score = score + faculty_member_one_class(chromosome)
    score = score + classroom_size(chromosome)
    return score


def init_population(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)

    a = random.randint(0, len(chromosome) - 1)
    
    chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) +\
        group_bits(chromosome[a]) + rand_slot + rand_lt

    # print("After mutation: ", end="")
    # printChromosome(chromosome)


def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    

def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()


def print_chromosome(chromosome):
    print(Course.courses[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Slot.slots[int(slot_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)])


def genetic_algorithm():
    generation = 0
    convert_input_to_bin()
    population = init_population(3)

    print("Original population:")
    print(population)
    
    while True:
        
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == max_score or generation == 200:
            print("Generations:", generation)
            print("Best Chromosome score", evaluate(max(population, key=evaluate)))
            print("Best Chromosome: ", max(population, key=evaluate))
            for lec in max(population, key=evaluate):
                print_chromosome(lec)
            break
        
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                
                selection(population[_c], len(cpg))
                mutate(population[_c])

        generation = generation + 1
        print("Gen:", generation)

    print("Population", population)


def main():
    random.seed()
    genetic_algorithm()


main()
