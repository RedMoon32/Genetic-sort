from random import uniform, randint, shuffle

#Hromosom
class Individual:
    def __init__(self,genome = []):
        #genom
        self.genome = genome
        self.score = 0

    #Score of this individual (number of unordered pairs in array )
    @property
    def fitness(self):
        score = 0
        for i in range(1,len(self.genome)):
            if self.genome[i]<self.genome[i-1]:
                score+=1
        self.score = score
        return score

    def __repr__(self):
        return str(self.genome)
    
    def __str__(self):
        return str(self.genome)

#Population
class Population:
    def __init__(self):
        self.individuals = []

    #New individum in population
    def add(self,individ):
        self.individuals.append(individ)

    #Individual with highest score 
    @property  
    def best_individual(self):
        best = None
        best_score = 9999
        for ind in self.individuals:
            f = ind.fitness
            if f < best_score:
                best = ind
                best_score = f
        return best

    #Cross(скрещиваем) two individuals
    @staticmethod
    def crossover(father:list, mother:list, start_index:int, end_index:int):
        sperm = father[start_index:end_index+1]
        fetus = [l for l in mother if l not in sperm]
        baby = fetus[:start_index] + sperm
        if len(baby)<len(father):
            baby += fetus[start_index:]
        return Individual(baby)

    #Mutate individual(randomly swap two elements of genom)
    @staticmethod
    def mutate(population, rate:float):
        for p in population.individuals:
            if uniform(0,1) < rate:
                first = randint(0,len(p.genome)-1)
                second = randint(0,len(p.genome)-1)
                if (first<second and p.genome[first]>p.genome[second]) \
                    or (first>second and p.genome[first]<p.genome[second]):
                    p.genome[first],p.genome[second] = p.genome[second],p.genome[first]    

        return population

#One evolution iteration
def evolve(population, mutation_rate):
    new_population = Population()
    #Best individ from the last population
    best = population.best_individual
    new_population.add(best)
    for i in range(len(population.individuals)-1):
        ind = population.individuals[i]
        start_at = randint(0, len(ind.genome) - 1)
        stop_at = randint(start_at, len(ind.genome) - 1)
        #Cross i'th individual with i+1 individual
        baby = Population.crossover(best.genome, population.individuals[i+1].genome,
                            start_at,stop_at)
        if baby is not None:
            new_population.add(baby)
            #Let some mutation
    return Population.mutate(new_population,mutation_rate)

def run(inp, population_size, mutation_rate):
    population = Population()
    for i in range(population_size):
        shuffle(inp)
        population.add(Individual(list(inp)))
    generation = 1
    #While we did not sort the array
    while population.best_individual.fitness>0:
        if generation % 5000 == 0:
            print('Generation #',generation)
            print('Score:',population.best_individual.score)
        population = evolve(population,mutation_rate)
        #print('Best fitness: ',population.best_individual.genome)
        generation += 1
    
    print('Solution found:',population.best_individual.genome)

if __name__ == "__main__":
    inp = [i for i in range(20,0,-1)]
    population_size = 10
    mutation_rate = 0.1
    run(inp,population_size,mutation_rate)
