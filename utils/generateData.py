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

#Semilla para reproducibilidad
np.random.seed(42)

def generate_data(num_lines=100, min_nodes=20, max_nodes=10000):
    data = {
        "route_id": [],
        "nodes": [],
        "demands": [],
        "fuel_costs": [],
        "distances": []
    }

    for i in range(num_lines):
        #Generar una longitud aleatoria de ruta entre min_nodes y max_nodes
        num_nodes = np.random.randint(min_nodes, max_nodes + 1)

        #Generar una lista de nodos únicos para cada ruta
        nodes = np.random.choice(range(1, 10000), num_nodes, replace=False)
        
        #Generar demandas para cada nodo en la ruta
        demands = [max(0, np.random.normal(10, 3)) for _ in range(num_nodes)]
        
        #Generar costos de combustible para cada nodo en la ruta
        fuel_costs = [round(np.random.uniform(1, 5), 2) for _ in range(num_nodes)]
        
        #Generar distancias entre cada par de nodos consecutivos en la ruta
        distances = [round(np.random.uniform(5, 100), 2) for _ in range(num_nodes - 1)]
        
        #Guardar en el diccionario
        data["route_id"].append(i + 1)
        data["nodes"].append(nodes.tolist())
        data["demands"].append(demands)
        data["fuel_costs"].append(fuel_costs)
        data["distances"].append(distances)

    #Convertir a DataFrame
    df = pd.DataFrame(data)
    
    #Guardar en archivo CSV
    df.to_csv("./data/routes.csv", index=False)
    print("Archivo 'routes.csv' generado con éxito.")

#Generar 100 líneas
generate_data(num_lines=100, min_nodes=3, max_nodes=10)
