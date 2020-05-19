from bird import Bird
import random

class Population:
    def __init__(self, n_individuals, mutation_rate):
        self.n_individuals = n_individuals
        self.mutation_rate = mutation_rate
        self.individuals = []  # individuos da população
        self.generate()
        self.total_fitness = 0

    def generate(self): # gerar população
        for id_individual in range(self.n_individuals):
            individual = Bird(115, 175) # cria individuo e adiciona à população
            self.individuals.append(individual)

    def reproduct(self):
        self.calculate_total_fitness()

        childs = []

        for n in range(self.n_individuals):
            partner_a = self.select()  # seleciona um indivíduo a com probabilidade de acordo com fitness
            partner_b = self.select()  # seleciona um indivíduo b com probabilidade de acordo com fitness

            child = Bird.cross_over(partner_a, partner_b) # gera o child a partir do cross-over entre a e b

            child.mutate(self.mutation_rate)  # mutação do child a partir da probabilidade mutation_rate
            childs.append(child)  # adiciona o child na população

        self.individuals = childs.copy()  # atualiza população

    def select(self):
        """ Seleciona um individuo dentro da população com probabilidade de acordo com o fitness
        1- Gera um valor aleatório random_value
        2- Itera sobre os indivíduos imaginando os fitness em uma "pilha de fitness imaginária"
        3- Compara a altura do random_value com a altura da pilha e retorna o individuo na mesma faixa
        ex: AAAAAAABBBBBBBCCCCC # pilha
            VVVVV # random_value -> retorna A
            VVVVVVVVVVV -> retorna B
            VVVVVVVVVVVVVVVVV -> retorna C
        """
        rand_value = self.total_fitness * random.random()  # gera um valor v entre 0 e soma dos fitness

        for individual in self.individuals:  # itera sobre a lista de individuos
            rand_value = rand_value - individual.fitness  # subtrai do valor aleatório os scores de cada individuo

            if rand_value <= 0:
                # quando o random_value ficar negativo, significa que o rand_value gerado estava
                # na faixa de probabilidades do fitness do individuo
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
