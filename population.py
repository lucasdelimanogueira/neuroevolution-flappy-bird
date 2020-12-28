from bird import Bird
import random

class Population:
    def __init__(self, n_individuals, mutation_rate):
        self.n_individuals = n_individuals
        self.mutation_rate = mutation_rate
        self.individuals = []  # population individuals
        self.generate()
        self.total_fitness = 0

    def generate(self): # generates population
        for id_individual in range(self.n_individuals):
            individual = Bird(115, 175) # generates and individual
            self.individuals.append(individual)

    def reproduct(self):
        self.calculate_total_fitness()

        childs = []

        for n in range(self.n_individuals):
            partner_a = self.select()  # samples an individual a with probability according to fitness
            partner_b = self.select()  # samples an individual b with probability according to fitness

            child = Bird.cross_over(partner_a, partner_b) # generates child through a-b crossover

            child.mutate(self.mutation_rate)  # mutates child according to mutation_rate probability
            childs.append(child)  # adds child in population

        self.individuals = childs.copy()  # updates population

    def select(self):
        """ Sampels an individual according to its fitness
        1- Generates a random value random_value
        2- Iterates over the individuals imagining a "fitness stack"
        3- Compares the random_value "height" with the stacked fitness values and return an individual in the same range
        ex: AAAAAAABBBBBBBCCCCC # stack
            VVVVV # random_value -> return A
            VVVVVVVVVVV -> return B
            VVVVVVVVVVVVVVVVV -> return C
        """
        rand_value = self.total_fitness * random.random()  # generates value v between 0 and fitness overall sum

        for individual in self.individuals:  # iterates over the individuals list
            rand_value = rand_value - individual.fitness  # subtracts from the random value the scores of the individual

            if rand_value <= 0:
                # when random_value becomes negative it means that the generated random_value was in the range of probabilities of the respective individual's fitness
 
                return individual




    ######## MISC #######

    def get_best_individual(self): # retorna o indivíduo com maior fitness
        best_individual = Bird()
        for individual in self.individuals:
            if individual.fitness > best_individual.fitness:
                best_individual = individual
        return best_individual

    def calculate_total_fitness(self): # calcula soma de fitness de toda população
        self.total_fitness = 0

        for individual in self.individuals:
            self.total_fitness += individual.fitness

    def is_all_dead(self):
        for individual in self.individuals:
            if individual.is_alive:
                return False

        return True
