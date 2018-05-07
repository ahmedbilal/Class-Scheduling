import random
from Data import *
from math import ceil, log2


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


g_bin = None
p_bin = None
c_bin = None
r_bin = None
t_bin = None


def bits_needed(x):
    return int(ceil(log2(len(x))))


def binary_converter(x):
    bit_repr = {}
    for i in range(len(x)):
        keys = list(x.keys())
        bit_repr[keys[i]] = (bin(i)[2:]).rjust(bits_needed(x), '0')
    return bit_repr


def join_elements(_list):
    for i in range(len(_list)):
        _list[i] = "".join(_list[i])


def convert_input_to_bin():
    global cpg, lts, slots
    global g_bin, p_bin, c_bin, r_bin, t_bin

    g_bin = binary_converter(sample_data.g)
    p_bin = binary_converter(sample_data.p)
    c_bin = binary_converter(sample_data.c)
    
    r_bin = binary_converter(sample_data.r)
    t_bin = binary_converter(sample_data.t)

    cpg = [
        [c_bin["hu100"], p_bin["mutaqi"], g_bin["a"]],
        [c_bin["mt111"], p_bin["khalid"], g_bin["a"]],
        [c_bin["hu160"], p_bin["mutaqi"], g_bin["b"]],
        [c_bin["ch110"], p_bin["zafar"],  g_bin["c"]],
        [c_bin["cs101"], p_bin["basit"], g_bin["e"]],
        [c_bin["cs152"], p_bin["basit"], g_bin["e"]],
    ]
    join_elements(cpg)

    lts = list(r_bin.values())
    slots = list(t_bin.values())

    print(cpg)
    

# All these *_bits() function assume that the *_bits variables are correctly set
def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(sample_data.c)]


def professor_bits(chromosome):
    i = bits_needed(sample_data.c)

    return chromosome[i: i + bits_needed(sample_data.p)]


def group_bits(chromosome):
    i = bits_needed(sample_data.c) + bits_needed(sample_data.p)

    return chromosome[i:i + bits_needed(sample_data.g)]


def slot_bits(chromosome):
    i = bits_needed(sample_data.c) + bits_needed(sample_data.p) + \
        bits_needed(sample_data.g)

    return chromosome[i:i + bits_needed(sample_data.t)]


def lt_bits(chromosome):
    i = bits_needed(sample_data.c) + bits_needed(sample_data.p) +\
        bits_needed(sample_data.g) + bits_needed(sample_data.t)

    return chromosome[i: i + bits_needed(sample_data.r)]


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
        _g_key = list(sample_data.g.keys())[int(group_bits(chromosome), 2)]
        _g_size = sample_data.g[_g_key].size

        _r_key = list(sample_data.r.keys())[int(lt_bits(chromosome), 2)]
        _r_size = sample_data.r[_r_key].size

        if _g_size > _r_size:
            problems = problems + 1
        else:
            points = points + 100
    else:
        for _c in chromosome:
            _g_key = list(sample_data.g.keys())[int(group_bits(_c), 2)]
            _g_size = sample_data.g[_g_key].size

            _r_key = list(sample_data.r.keys())[int(lt_bits(_c), 2)]
            _r_size = sample_data.r[_r_key].size

            if _g_size > _r_size:
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
    print("Course:", list(sample_data.c.keys())[list(c_bin.values()).index(course_bits(chromosome))],
          "Prof:", list(sample_data.p.keys())[list(p_bin.values()).index(professor_bits(chromosome))],
          "Group:", list(sample_data.g.keys())[list(g_bin.values()).index(group_bits(chromosome))],
          "Slot:", list(sample_data.t.keys())[list(t_bin.values()).index(slot_bits(chromosome))],
          "LT:", list(sample_data.r.keys())[list(r_bin.values()).index(lt_bits(chromosome))])


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
