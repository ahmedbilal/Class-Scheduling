import random, copy
from Classes import *
from math import ceil, log2

Group.groups = [Group("a", 10), Group("b", 20), Group("c", 30), Group("d", 10), Group("e", 40)]

Professor.professors = [Professor("mutaqi"), Professor("khalid"), Professor("zafar"),
                        Professor("basit"), Professor("khalid_zaheer")]

CourseClass.classes = [CourseClass("hu100a"), CourseClass("hu100b"), CourseClass("mt111"),
                       CourseClass("hu160"), CourseClass("cs101 lab", is_lab=True),
                       CourseClass("ch110"), CourseClass("cs101"), CourseClass("cs152")]

Room.rooms = [Room("lt1", 20), Room("lt2", 40), Room("lt3", 60), Room("lab", 100, is_lab=True)]

Slot.slots = [Slot("08:30", "10:00", "Mon"), Slot("10:15", "11:45", "Mon"),
              Slot("12:00", "13:30", "Mon"), Slot("08:30", "10:00", "Tue"), Slot("08:30", "11:30", "Mon", True)]

# TODO
# 0.  Running Simplified Class Scheduling - Done
# 0.5 Problem Instance to Binary String - Done
# 1.  Multiple days - Done
# 2.  Class Size - Done
# 2.25 Check Selection Function - Done
# 2.5 One group can attend only one class at a time - Done
# 3.  Multiple classes - Done
# 4.  Lab - Done

# Below chromosome parts are just to teach basic

# cpg = ["000000", "010001", "100100", "111010"] # course, professor, student group pair
# lts = ["00", "01"] # lecture theatres
# slots = ["00", "01"] # time slots

# ######### Chromosome ##############
# <CourseClass, Prof, Group, Slot, LT>   #
# ###################################


max_score = None

cpg = []
lts = []
slots = []
bits_needed_backup_store = {}  # to improve performance


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, lts, slots, max_score

    cpg = [CourseClass.find("hu100a"), Professor.find("mutaqi"), Group.find("a"),
           CourseClass.find("hu100b"), Professor.find("mutaqi"), Group.find("a"),
           CourseClass.find("mt111"), Professor.find("khalid"), Group.find("a"),
           CourseClass.find("cs152"), Professor.find("basit"), Group.find("a"),
           CourseClass.find("hu160"), Professor.find("mutaqi"), Group.find("b"),
           CourseClass.find("ch110"), Professor.find("zafar"), Group.find("e"),
           CourseClass.find("cs101"), Professor.find("basit"), Group.find("e"),
           CourseClass.find("cs101 lab"), Professor.find("basit"), Group.find("e")
           ]

    for _c in range(len(cpg)):
        if _c % 3:  # CourseClass
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')
        elif _c % 3 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
        else:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), '0'))

    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots), '0'))

    # print(cpg)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(CourseClass.classes)]


def professor_bits(chromosome):
    i = bits_needed(CourseClass.classes)

    return chromosome[i: i + bits_needed(Professor.professors)]


def group_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors)

    return chromosome[i:i + bits_needed(Group.groups)]


def slot_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups)

    return chromosome[i:i + bits_needed(Slot.slots)]


def lt_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups) + bits_needed(Slot.slots)

    return chromosome[i: i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and professor_bits(chromosome[i]) == professor_bits(chromosome[j]):
                clash = True
                # print("These prof. have clashes")
                # print_chromosome(chromosome[i])
                # print_chromosome(chromosome[j])
        if not clash:
            scores = scores + 1
    return scores


# check that a group member takes only one class at a time.
def group_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and\
                    group_bits(chromosomes[i]) == group_bits(chromosomes[j]):
                # print("These classes have slot/lts clash")
                # print_chromosome(chromosomes[i])
                # print_chromosome(chromosomes[j])
                # print("____________")
                clash = True
                break
        if not clash:
            # print("These classes have no slot/lts clash")
            # print_chromosome(chromosomes[i])
            # print_chromosome(chromosomes[j])
            # print("____________")
            scores = scores + 1
    return scores


# checks that a course is assigned to an available classroom. 
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                # print("These classes have slot/lts clash")
                # printChromosome(chromosome[i])
                # printChromosome(chromosome[j])
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# checks that the classroom capacity is large enough for the classes that
# are assigned to that classroom.
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Group.groups[int(group_bits(_c), 2)].size <= Room.rooms[int(lt_bits(_c), 2)].size:
            scores = scores + 1
    return scores


# check that room is appropriate for particular class/lab
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c), 2)].is_lab == Room.rooms[int(lt_bits(_c), 2)].is_lab:
            scores = scores + 1
    return scores


# check that lab is allocated appropriate time slot
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c), 2)].is_lab == Slot.slots[int(slot_bits(_c), 2)].is_lab_slot:
            scores = scores + 1
    return scores


def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + group_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    return score / max_score

def cost(solution):
    # solution would be an array inside an array
    # it is because we use it as it is in genetic algorithms
    # too. Because, GA require multiple solutions i.e population
    # to work.
    return 1 / float(evaluate(solution))

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
    print(CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Slot.slots[int(slot_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)])

# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab
def ssn(solution):
    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)
    
    a = random.randint(0, len(solution) - 1)
    
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + rand_slot + lt_bits(solution[a])
    return [new_solution]

# Swapping Neighborhoods
# It randomy selects two classes and swap their time slots
def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + slot_bits(solution[b]) + lt_bits(solution[a])

    new_solution[b] = course_bits(solution[b]) + professor_bits(solution[b]) +\
        group_bits(solution[b]) + temp + lt_bits(solution[b])
    # print("Diff", solution)
    # print("Meiw", new_solution)
    return [new_solution]

    
def simulated_annealing():
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])
    # print("Cost of original random solution: ", old_cost)
    # print("Original population:")
    # print(population)

    for __n in range(500):
        new_solution = swn(population[0])
        new_cost = cost(new_solution[0])
        if (new_cost < old_cost):
            population = new_solution

        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        if (new_cost < old_cost):
            population = new_solution

    # print(population)
    # print("Cost of altered solution: ", cost(population[0]))
    print("\n------------- Simulated Annealing --------------\n")
    for lec in population[0]:
        print_chromosome(lec)
    print("Score: ", evaluate(population[0]))

def genetic_algorithm():
    generation = 0
    convert_input_to_bin()
    population = init_population(3)

    # print("Original population:")
    # print(population)
    print("\n------------- Genetic Algorithm --------------\n")
    while True:
        
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            print("Generations:", generation)
            print("Best Chromosome fitness value", evaluate(max(population, key=evaluate)))
            print("Best Chromosome: ", max(population, key=evaluate))
            for lec in max(population, key=evaluate):
                print_chromosome(lec)
            break
        
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                
                # selection(population[_c], len(cpg))
                mutate(population[_c])

        generation = generation + 1
        # print("Gen: ", generation)

    # print("Population", len(population))


def main():
    random.seed()
    genetic_algorithm()
    simulated_annealing()

main()
