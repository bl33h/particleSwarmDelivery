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
    - Modificado el 11/11/2024
"""

import numpy as np
import pandas as pd
import ast

# Parámetros del PSO
num_particles = 30
num_iterations = 100
inertia_weight = 0.5
cognitive_weight = 1.5
social_weight = 1.5

# Inicializar las posiciones y velocidades
def initialize_particles(num_particles, num_nodes):
    positions = np.array([np.random.permutation(num_nodes) for _ in range(num_particles)])
    velocities = [np.zeros(num_nodes) for _ in range(num_particles)]  # Velocidades iniciales como swaps
    return positions, velocities

# Función objetivo: calcular el costo total de una ruta específica
def objective_function(route, distances, fuel_costs, demands):
    total_distance = sum(distances[route[i], route[i + 1]] for i in range(len(route) - 1))
    total_fuel_cost = sum(fuel_costs[route[i]] * demands[route[i]] for i in range(len(route)))
    return total_distance + total_fuel_cost

# Actualización de velocidades y posiciones
def update_velocity(velocity, position, best_local, best_global, inertia_weight, cognitive_weight, social_weight):
    r1, r2 = np.random.rand(), np.random.rand()
    cognitive_component = cognitive_weight * r1 * (best_local - position)
    social_component = social_weight * r2 * (best_global - position)
    new_velocity = inertia_weight * velocity + cognitive_component + social_component
    return new_velocity

# Función para mover las partículas y mantenerlas como permutaciones
def move_particles(positions, velocities, num_nodes):
    new_positions = []
    for position, velocity in zip(positions, velocities):
        # Permutar posiciones en base a la velocidad
        permuted_position = position.copy()
        for i in range(num_nodes):
            swap_index = int(abs(velocity[i]) % num_nodes)
            permuted_position[i], permuted_position[swap_index] = permuted_position[swap_index], permuted_position[i]
        new_positions.append(permuted_position)
    return np.array(new_positions)

# Ejecutar PSO para cada ruta en el archivo CSV
def run_pso(filename):
    # Leer datos desde el archivo CSV
    data = pd.read_csv(f"./data/{filename}.csv")
    
    mean_cost = 0
    std = 0

    results = []
    
    # Ejecutar PSO para cada ruta en el archivo CSV
    for index, row in data.iterrows():
        route_id = row["route_id"]
        nodes = ast.literal_eval(row["nodes"])
        demands = ast.literal_eval(row["demands"])
        fuel_costs = ast.literal_eval(row["fuel_costs"])
        distances_raw = ast.literal_eval(row["distances"])

        # Convertir la matriz de distancias de lista de listas a un array de numpy
        distances = np.array(distances_raw)

        # Inicializar partículas
        num_nodes = len(nodes)
        positions, velocities = initialize_particles(num_particles, num_nodes)
        best_local_positions = positions.copy()
        best_global_position = np.random.permutation(num_nodes)
        best_local_scores = np.full(num_particles, np.inf)
        best_global_score = np.inf

        # Algoritmo PSO para optimizar la ruta de entrega
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
                velocities[i] = update_velocity(
                    velocities[i], positions[i], best_local_positions[i], 
                    best_global_position, inertia_weight, cognitive_weight, social_weight)
            positions = move_particles(positions, velocities, num_nodes)

        result = [route_id, nodes, [nodes[i] for i in best_global_position], round(best_global_score, 2)]
        results.append(result)
        
        # Calcular el costo promedio y la desviación estándar de los costos mínimos
        mean_cost += best_global_score
        std += best_global_score ** 2
    
    mean_cost /= len(data)
    std = np.sqrt(std / len(data) - mean_cost ** 2)
    
    return results, mean_cost, std
