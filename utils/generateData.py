"""
 * Nombre: generateData.py
 * Autores:
    - Fernanda Esquivel, 21542
    - Melissa Pérez, 21385
    - Sara Echeverría, 21371
    - Ricardo Méndez, 21289
    - Fabián Juárez, 21440
 * Descripción: Programa que genera data aleatoria de rutas de entrega con múltiples nodos y la guarda en un archivo CSV.
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: 
    - Creado el 09/11/2024
    - Modificado el 09/11/2024
"""

import numpy as np
import pandas as pd
import string

# Semilla para reproducibilidad
np.random.seed(42)

def generate_data(num_lines=10, min_nodes=3, max_nodes=20):
    data = {
        "route_id": [],
        "nodes": [],
        "demands": [],
        "fuel_costs": [],
        "distances": []
    }

    for i in range(num_lines):
        # Generar una cantidad aleatoria de nodos entre min_nodes y max_nodes
        num_nodes = np.random.randint(min_nodes, max_nodes + 1)

        # Generar nombres de nodos usando letras
        nodes = list(string.ascii_uppercase[:num_nodes])
        
        # Generar demandas para cada nodo en la ruta
        demands = [max(0, np.random.normal(10, 3)) for _ in range(num_nodes)]
        
        # Generar costos de combustible para cada nodo en la ruta
        fuel_costs = [round(np.random.uniform(1, 5), 2) for _ in range(num_nodes)]
        
        # Generar una matriz de distancias simétrica entre todos los pares de nodos
        distances = np.random.uniform(5, 100, size=(num_nodes, num_nodes))
        distances = (distances + distances.T) / 2  # Hacer la matriz simétrica
        np.fill_diagonal(distances, 0)  # La distancia de un nodo a sí mismo es 0
        distances_list = distances.tolist()  # Convertir a lista de listas para guardar en CSV
        
        # Guardar en el diccionario
        data["route_id"].append(i + 1)
        data["nodes"].append(nodes)
        data["demands"].append(demands)
        data["fuel_costs"].append(fuel_costs)
        data["distances"].append(distances_list)

    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    # Guardar en archivo CSV
    df.to_csv("./data/routes.csv", index=False)
    print("Archivo 'routes.csv' generado con éxito.")

# Generación de datos con rutas de entre 3 y 20 nodos
generate_data(num_lines=10, min_nodes=3, max_nodes=20)
