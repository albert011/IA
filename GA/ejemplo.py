from sklearn.tree import DecisionTreeClassifier
from genetic_selection import GeneticSelectionCV as gscv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data(path):
  data = pd.read_csv(path)
  return data
  
def select_attributes(data, model):
  #Seleccionar atributo de clasificación, dado los datos de entrada que se encuentra en la ultima columna de nuestros datos\n",
  target = data.columns[-1]
  x = data.drop([target], axis=1)
  y = data[target].astype(float)
  solver = gscv(model, scoring='accuracy', n_jobs=-1)
  solver.fit(x, y)
  return x.columns[solver.support_]
  
cancer = load_data('conjuntos_de_datos/BreastCancerDataset.csv')
model = DecisionTreeClassifier()
cancer_attributes = select_attributes(cancer, model)
print(cancer_attributes)