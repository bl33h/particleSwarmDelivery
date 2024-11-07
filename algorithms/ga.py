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

# Parámetros iniciales
num_nodes = 10  # Número de ubicaciones
population_size = 20  # Tamaño de la población
num_generations = 100  # Número de generaciones
mutation_rate = 0.1  # Tasa de mutación

# Matriz de distancias
np.random.seed(42)  # Para reproducibilidad
distances = np.random.rand(num_nodes, num_nodes)
distances = (distances + distances.T) / 2  # Simétrica
np.fill_diagonal(distances, 0)  # La distancia de un nodo a sí mismo es 0

# Costos de combustible
fuel_costs = np.random.uniform(1, 5, num_nodes)  # Costos aleatorios entre 1 y 5

# Demanda variable en cada nodo (valores aleatorios entre 1 y 10)
demand = np.random.randint(1, 10, num_nodes)
cost_per_unit_demand = 0.5  # Costo por unidad de demanda

# Función de aptitud que incluye demanda y costos
def fitness(route):
    # Costos de distancia y combustible
    route_cost = sum(distances[route[i], route[i+1]] for i in range(len(route) - 1))
    fuel_cost = sum(fuel_costs[route])

    # Costo adicional por demanda
    demand_cost = sum(demand[route] * cost_per_unit_demand)

    # Costo total
    return route_cost + fuel_cost + demand_cost

# Generación inicial de población (rutas aleatorias)
population = [np.random.permutation(num_nodes) for _ in range(population_size)]

# Algoritmo Genético (GA)
for generation in range(num_generations):
    # Evaluación de aptitud de la población
    fitness_scores = np.array([fitness(route) for route in population])
    
    # Selección por torneo
    selected_indices = np.random.choice(population_size, size=population_size, replace=True, 
                                        p=(1 / (fitness_scores + 1e-5)) / sum(1 / (fitness_scores + 1e-5)))
    selected_population = [population[i] for i in selected_indices]

    # Cruce (cross-over) para generar nueva población
    new_population = []
    for i in range(0, population_size, 2):
        parent1, parent2 = selected_population[i], selected_population[(i + 1) % population_size]
        # Cruzamiento en un punto con filtro para mantener nodos únicos
        cross_point = np.random.randint(1, num_nodes - 1)
        child1 = np.concatenate((parent1[:cross_point], [node for node in parent2 if node not in parent1[:cross_point]]))
        child2 = np.concatenate((parent2[:cross_point], [node for node in parent1 if node not in parent2[:cross_point]]))
        new_population.extend([child1, child2])

    # Mutación
    for i in range(population_size):
        if np.random.rand() < mutation_rate:
            swap_idx = np.random.choice(num_nodes, size=2, replace=False)
            new_population[i][swap_idx[0]], new_population[i][swap_idx[1]] = new_population[i][swap_idx[1]], new_population[i][swap_idx[0]]
    
    # Actualizar población
    population = new_population

# Selección de la mejor solución final
best_route = population[np.argmin([fitness(route) for route in population])]
best_route_cost = fitness(best_route)

print("Mejor ruta encontrada:", best_route)
print("Costo total de la mejor ruta:", best_route_cost)
