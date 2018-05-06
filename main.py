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
slots = ["00", "01"] # time slots


max_score = 200

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
def course_bits(chromosome):
    return chromosome[0:courses_bits]

def professor_bits(chromosome):
    return chromosome[courses_bits: courses_bits + professors_bits]

def group_bits(chromosome):
    return chromosome[courses_bits + professors_bits:courses_bits + professors_bits + groups_bits]

def slot_bits(chromosome):
    return chromosome[total_bits - lts_bits - slots_bits: total_bits - lts_bits]

def lt_bits(chromosome):
    return chromosome[total_bits - lts_bits:total_bits]


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


def init_population(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for c in cpg:
            chromosome.append(c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes

# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    old_chromosome = chromosome[:]
    #print("Before mutation: ", end="")
    #printChromosome(chromosome)

    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)

    a = random.randint(0, len(chromosome) - 1)
    
    chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) + group_bits(chromosome[a]) + rand_slot + rand_lt

    #print("After mutation: ", end="")
    #printChromosome(chromosome)

def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0])) # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    

def selection(population, n):
    population.sort(key = scores, reverse=True)
    while len(population) > n:
        population.pop()

def printChromosome(chromosome):
    print("Course:", course_bits(chromosome),
          "Prof:", professor_bits(chromosome),
          "Group:", group_bits(chromosome),
          "Slot:", slot_bits(chromosome),
          "LT:", lt_bits(chromosome))

def genetic_algorithm():
    generation = 0
    population = init_population(3)

    print("Original population:")
    print(population)
    
    while True:
        
        # if termination criteria are satisfied, stop.
        if scores(max(population, key = scores)) == max_score or generation == 200:
            print("Generations:", generation)
            print("Best Chromosome score", scores(max(population, key = scores)))
            print()
            for lec in max(population, key = scores):
                printChromosome(lec)
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
