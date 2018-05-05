import random
from copy import deepcopy
######### Todo #########
#   0. Running Simplified Class Scheduling - Done
#   1. Multiple classes
#   2. Class Size
#   3. Multiple days
#   4. Duration
#   5. Lab

cpg = ["000000", "010001", "100100", "111010"] # course, professor, student group pair
lts = ["00", "01"] # lecture theatres
slots = ["00", "01", "10", "11"] # time slots

########## Chromosome ##############
# <Course, Prof, Group, Slot, LT>  #
#  0-2   , 2-4 , 4-6  , 6-8 , 8-10 #
####################################

courses_bits  = 2
professors_bits = 2
groups_bits = 2
lts_bits = 2
slots_bits = 2

total_bits = courses_bits + professors_bits + groups_bits + lts_bits + slots_bits


# All these *_bits() function assume that the *_bits variables are correctly set
def course_bits(c):
    return c[0:courses_bits]

def professor_bits(c):
    return c[courses_bits: courses_bits + professors_bits]

def group_bits(c):
    return c[courses_bits + professors_bits:courses_bits + professors_bits + groups_bits]

def slot_bits(c):
    return c[total_bits - lts_bits - slots_bits: total_bits - lts_bits]

def lt_bits(c):
    return c[total_bits - lts_bits:total_bits]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b): return 1
    return 0


#checks that a faculty member teaches only one course at a time. 
def facultymemberOneClass(chromosome):
    clashes = []
    for i in range(len(chromosome) - 1): # select one cpg pair
        for j in range(i + 1, len(chromosome)): # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and professor_bits(chromosome[i]) == professor_bits(chromosome[j]):
                #print("These profs. have clash")
                #printChromosome(chromosome[i])
                #printChromosome(chromosome[j])
                #print()
                clashes.append([chromosome[i], chromosome[j]])
    return (len(chromosome) * 100 - len(clashes) * 100) / len(cpg)


# checks that a course is assigned to an available classroom. 
def useClassroomAvailableTime(chromosome):
    clashes = []
    for i in range(len(chromosome) - 1): # select one cpg pair
        for j in range(i + 1, len(chromosome)): # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                #print("These classes have slot/lts clash")
                #printChromosome(chromosome[i])
                #printChromosome(chromosome[j])
                clashes.append([chromosome[i], chromosome[j]])
    return (len(chromosome) * 100 - len(clashes) * 100)/ len(cpg)


def scores(c):
    score = 0
    score = score + useClassroomAvailableTime(c)
    score = score + facultymemberOneClass(c)
    return score


def init(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for c in cpg:
            chromosome.append(c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes

def mutate(c):
    old_c = c[:]
    #print("Before mutation: ", end="")
    #printChromosome(c)
    a = random.randint(0, len(c) - 1)
    b = random.randint(0, len(c) - 1)
    #print(c[a])
    temp = deepcopy(c[a])
    c[a] = course_bits(c[a]) + professor_bits(c[a]) + group_bits(c[a]) + slot_bits(c[b]) + lt_bits(c[b])
    c[b] = course_bits(c[b]) + professor_bits(c[b]) + group_bits(c[b]) + slot_bits(temp) + lt_bits(temp)

    #print("After mutation: ", end="")
    #printChromosome(c)

def crossover(c):
    a = random.randint(0, len(c) - 1)
    b = random.randint(0, len(c) - 1)
    pass

def printChromosome(c):
    print("Course:", course_bits(c),
          "Prof:", professor_bits(c),
          "Group:", group_bits(c),
          "Slot:", slot_bits(c),
          "LT:", lt_bits(c))

def main():
    random.seed()
    c = init(3)
    print("Chromosome", c)

    gen = 0
    oldscore = scores(max(c, key = scores))
    print("Best Original score:", oldscore)
    while (oldscore != 200):
        for _c in range(len(c)):
            mutate(c[_c])
            mutate(c[_c])
            gen = gen + 1
            if scores(c[_c]) > oldscore:
                oldscore = scores(c[_c])

            if gen == 1000:
                oldscore = 200
                break
    print()
    print("Generations:", gen)
    best_chromosome = max(c, key = scores)
    print("Best Chromosome:", best_chromosome, "Scores:", scores(best_chromosome))

    print("All Chromosomes:", c)
main()
