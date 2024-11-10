"""
 * Nombre: ga.py
 * Autores:
    - Fernanda Esquivel, 21542
    - Melissa Pérez, 21385
    - Sara Echeverría, 21371
    - Ricardo Méndez, 21289
    - Fabián Juárez, 21440
 * Descripción: Programa que implementa un algoritmo GA para optimizar rutas de entrega.
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: 
    - Creado el 07/11/2024
    - Modificado el 07/11/2024
"""

import numpy as np
import pandas as pd
import ast
from prettytable import PrettyTable
import time

# parámetros iniciales GA
population_size = 20        # Tamaño de la población
num_generations = 100       # Número de generaciones
mutation_rate = 0.1         # Tasa de mutación
cost_per_unit_demand = 0.5  # Costo por unidad de demanda

#Leer datos desde el archivo CSV
data = pd.read_csv("./data/routes.csv")

#función de aptitud que incluye distancia, combustible y demanda
def fitness(route, distances, fuel_costs, demands):
    # Costo total de distancia
    route_cost = sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1))
    # Costo total de combustible
    fuel_cost = sum(fuel_costs[route[i]] * demands[route[i]] for i in range(len(route)))
    # Costo total
    return route_cost + fuel_cost

# población con rutas aleatorias
def initialize_population(num_nodes):
    return [np.random.permutation(num_nodes) for _ in range(population_size)]

# crossover de un punto
def crossover(parent1, parent2):
    cross_point = np.random.randint(1, len(parent1) - 1)
    child1 = np.concatenate((parent1[:cross_point], [node for node in parent2 if node not in parent1[:cross_point]]))
    child2 = np.concatenate((parent2[:cross_point], [node for node in parent1 if node not in parent2[:cross_point]]))
    return child1, child2

# operador de mutación
def mutate(route):
    swap_idx = np.random.choice(len(route), size=2, replace=False)
    route[swap_idx[0]], route[swap_idx[1]] = route[swap_idx[1]], route[swap_idx[0]]
    return route

# tabla para mostrar resultados
table = PrettyTable()
table.field_names = ["route_id", "nodes", "mejor_ruta", "costo_minimo"]

# inicio de medición del tiempo
start_time = time.time()

# ejecución de GA para cada ruta en el archivo
for index, row in data.iterrows():
    route_id = row["route_id"]
    nodes = ast.literal_eval(row["nodes"])
    demands = np.array(ast.literal_eval(row["demands"]))
    fuel_costs = np.array(ast.literal_eval(row["fuel_costs"]))
    distances_raw = ast.literal_eval(row["distances"])

    # matriz de distancias simétrica para el GA (se llenan diagonales con 0)
    num_nodes = len(nodes)
    distances = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes - 1):
        distances[i, i + 1] = distances_raw[i]
        distances[i + 1, i] = distances_raw[i]  # distancia simétrica

    # inicializar población
    population = initialize_population(num_nodes)

    # Algoritmo Genético (GA)
    for generation in range(num_generations):
        # Evaluación de aptitud de la población
        fitness_scores = np.array([fitness(route, distances, fuel_costs, demands) for route in population])

        # selección por torneo
        selected_indices = np.random.choice(population_size, size=population_size, replace=True, 
                                            p=(1 / (fitness_scores + 1e-5)) / sum(1 / (fitness_scores + 1e-5)))
        selected_population = [population[i] for i in selected_indices]

        # cruce para generar nueva población
        new_population = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected_population[i], selected_population[(i + 1) % population_size]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])

        # mutación
        for i in range(population_size):
            if np.random.rand() < mutation_rate:
                new_population[i] = mutate(new_population[i])

        # actualizar población
        population = new_population

    # selección de la mejor solución final
    best_route = population[np.argmin([fitness(route, distances, fuel_costs, demands) for route in population])]
    best_route_cost = fitness(best_route, distances, fuel_costs, demands)

    table.add_row([route_id, nodes, [nodes[i] for i in best_route], round(best_route_cost, 2)])

# fin medición del tiempo
end_time = time.time()
execution_time = end_time - start_time

# impresión tabla de resultados y tiempo de ejecución
print(table)
print(f"Tiempo de ejecución total: {execution_time:.2f} segundos")
