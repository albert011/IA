import numpy as np
#Ejemplo de algoritmo genetico
class gen():
  def __init__(self, **configurable_data):
    self.number_variables = configurable_data.get('number_variables')
    self.number_population = configurable_data.get('number_population')
    self.number_generation = configurable_data.get('number_generation')
    self.number_selected = configurable_data.get('number_selected')
    self.variables = configurable_data.get('variable_names')
    self.mutation_rate = configurable_data.get('mutation_rate')
    self.seed = configurable_data.get('seed')
    self.verbose = configurable_data.get('verbose')

  def create_chromosome(self, seed=None):
    if(seed != None):
      np.random.seed(seed)
    chromosome = [np.random.randint(0,10) for i in range(self.number_variables)]
    #print(chromosome)
    return chromosome

  def create_population(self):
    population = []
    self.generation = 0
    if(self.seed != None):
      population = [self.create_chromosome(self.seed+i) for i in range(self.number_population)]
    else:
      population = [self.create_chromosome() for i in range(self.number_population)]
    #print(population)
    return population

  #Ejemplo de prueba, funcion de validacion
  def fitness(self, chromosome):
    counter = 0
    for i in chromosome:
      if i > 7:
        counter += 1
    return (counter, chromosome)

  def get_elitist_chromosomes(self, population):
    elitist_chromosomes = [self.fitness(i) for i in population]
    elitist_chromosomes = sorted(elitist_chromosomes, reverse=True)[:self.number_selected]
    #Devuelve un conjunto de seleccionados pensando unicamente bajo criterios de explotacion
    return elitist_chromosomes

  def cross_mutation(self, population, selected):
    new_population = []
    self.generation +=1
    if(self.seed != None):
      for i in range(len(population)):
        np.random.seed(self.seed+i)
        
        cross_point = np.random.randint(1,len(population[i]))
        chromosome_selected = selected[np.random.randint(0,len(selected))][1]
        #Crea nuevo cromosoma a partir de los valores previos
        new_chromosome = [*chromosome_selected[:cross_point],*population[i][cross_point:]]
        #Aplicar mutation rate a valor random
        new_chromosome = [i  if np.random.randint(1,100) < 100-self.mutation_rate*100 else np.random.randint(0,10) for i in new_chromosome]
        new_population.append(new_chromosome)
    else:
      #Mismo codigo solo que sin semilla
      for i in range(len(population)):
        cross_point = np.random.randint(1,len(population[i]))
        chromosome_selected = selected[np.random.randint(0,len(selected))][1]
        #Crea nuevo cromosoma a partir de los valores previos
        new_chromosome = [*chromosome_selected[:cross_point],*population[i][cross_point:]]
        #Aplicar mutation rate a valor random
        new_chromosome = [i  if np.random.randint(1,100) < 100-self.mutation_rate*100 else np.random.randint(0,10) for i in new_chromosome]
        new_population.append(new_chromosome)
    return new_population


  def get_solution(self):
    population = self.create_population()
    selected = self.get_elitist_chromosomes(population)
    if(self.verbose):
      print('Creando poblacion inicial\n'+
            '{p}\n'.format(p=population)+
            'Evaluando mejores cromosomas\n'+
           '{s}'.format(s=selected))
    while(self.generation<self.number_generation):
      population = self.cross_mutation(population, selected)
      selected = self.get_elitist_chromosomes(population)
      if(self.verbose):
        print('Nueva poblacion generada\n'+
            '{p}\n'.format(p=population)+
            'Evaluando mejores cromosomas\n'+
           '{s}'.format(s=selected))
    if(self.verbose):
      print('Mejor solucion encontrada: {s}'.format(s=selected[0][1]))
    return selected[0][1]
      
    
    

    

if __name__ == '__main__':
  gen_example = gen(number_variables=10, number_population=10,number_generation=5, number_selected=3,mutation_rate=0.02,seed=1,verbose=True)
  gen_example.get_solution()
