"""
 * Nombre: pso.py
 * Autores:
    - Fernanda Esquivel, 21542
    - Melissa Pérez, 21385
    - Sara Echeverría, 21371
    - Ricardo Méndez, 21289
    - Fabián Juárez, 21440
 * Descripción: Programa que implementa un algoritmo PSO para optimizar rutas de entrega.
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: 
    - Creado el 22/10/2024
    - Modificado el 22/10/2024
"""

import numpy as np

#Número de nodos (ubicaciones de entrega)
num_nodes = 10  #Comencemos con algo sencillito (10 ubicaciones de entrega)

#Matriz de distancias entre nodos
#Generamos una matriz simétrica aleatoria para representar las distancias entre ubicaciones
np.random.seed(42)  #Para reproducibilidad
distances = np.random.rand(num_nodes, num_nodes)
distances = (distances + distances.T) / 2  #Hacerla simétrica
np.fill_diagonal(distances, 0)  #La distancia de un nodo a sí mismo es 0

#Costos de combustible asociados a cada nodo
fuel_costs = np.random.uniform(1, 5, num_nodes)  #Genera costos aleatorios entre 1 y 5

#Demanda en cada nodo, modelada como una variable aleatoria
def simulate_demand(num_nodes):
    #Probemos con una distribución normal (media=10, desviación estándar=5)
    return np.random.normal(loc=10, scale=5, size=num_nodes)

demands = simulate_demand(num_nodes)

#Parámetros del PSO
num_particles = 30
num_iterations = 100
inertia_weight = 0.5
cognitive_weight = 1.5
social_weight = 1.5

#Inicializar las posiciones y velocidades
def initialize_particles(num_particles, num_nodes):
    positions = np.array([np.random.permutation(num_nodes) for _ in range(num_particles)])
    velocities = np.random.rand(num_particles, num_nodes)  # Velocidades iniciales aleatorias
    return positions, velocities

#Función objetivo: calcular el costo total de una ruta
def objective_function(route, distances, fuel_costs, demands):
    total_distance = np.sum([distances[route[i], route[i + 1]] for i in range(len(route) - 1)])
    total_fuel_cost = np.sum([fuel_costs[route[i]] * demands[i] for i in range(len(route))])
    return total_distance + total_fuel_cost

#Actualización de velocidades y posiciones
def update_velocity(velocity, position, best_local, best_global, inertia_weight, cognitive_weight, social_weight):
    r1, r2 = np.random.rand(), np.random.rand()
    cognitive_component = cognitive_weight * r1 * (best_local - position)
    social_component = social_weight * r2 * (best_global - position)
    new_velocity = inertia_weight * velocity + cognitive_component + social_component
    return new_velocity

#Función para mover las partículas
def move_particles(positions, velocities):
    new_positions = positions + velocities
    # Asegurarse de que las posiciones sean válidas (en este caso, mantendremos posiciones como permutaciones)
    new_positions = np.clip(new_positions, 0, len(positions) - 1)
    return new_positions

#Inicializar partículas
positions, velocities = initialize_particles(num_particles, num_nodes)
best_local_positions = positions.copy()
best_global_position = np.random.permutation(num_nodes)
best_local_scores = np.full(num_particles, np.inf)
best_global_score = np.inf

#Algoritmo PSO
for iteration in range(num_iterations):
    for i in range(num_particles):
        score = objective_function(positions[i], distances, fuel_costs, demands)
        if score < best_local_scores[i]:
            best_local_scores[i] = score
            best_local_positions[i] = positions[i].copy()
        if score < best_global_score:
            best_global_score = score
            best_global_position = positions[i].copy()

    for i in range(num_particles):
        velocities[i] = update_velocity(velocities[i], positions[i], best_local_positions[i], best_global_position, inertia_weight, cognitive_weight, social_weight)
        positions[i] = move_particles(positions[i], velocities[i])

#(La mejor solución es la que tiene el menor costo global)
print("Mejor ruta encontrada: ", best_global_position)
print("Costo asociado: ", best_global_score)