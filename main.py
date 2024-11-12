"""
 * Nombre: main.py
 * Autores:
    - Fernanda Esquivel, 21542
    - Melissa Pérez, 21385
    - Sara Echeverría, 21371
    - Ricardo Méndez, 21289
    - Fabián Juárez, 21440
 * Descripción: Programa principal que ejecuta los algoritmos PSO y GA para optimizar rutas de entrega.
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: 
    - Creado el 09/11/2024
    - Modificado el 11/11/2024
"""

import time
from algorithms.pso import run_pso
from algorithms.ga import run_ga
from prettytable import PrettyTable
from utils.generateData import generate_data
import numpy as np
import pandas as pd
import ast
import graphviz
from IPython.display import display

#Generar data
filename = "routes"
generate_data(num_lines=10, min_nodes=3, max_nodes=20, filename=filename)

def print_results(results):
    table = PrettyTable()
    table.field_names = ["route_id", "mejor_ruta", "costo_minimo"]
    
    for result in results:
        route_id = result[0]
        best_route = " -> ".join(result[2])  #Convertir a formato "A -> B -> C"
        best_cost = result[3]
        table.add_row([route_id, best_route, best_cost])
    
    print(table)

# pso algorithm
def run_pso_algorithm():
    print("\n--- Ejecutando PSO ---")
    start_time = time.time()
    pso_results, mean_cost, std = run_pso(filename)
    end_time = time.time()
    print_results(pso_results)
    print(f"Tiempo de ejecución de PSO: {end_time - start_time:.2f} segundos\n")

# ga algorithm
def run_ga_algorithm():
    print("\n--- Ejecutando GA ---")
    start_time = time.time()
    ga_results, mean_cost, std = run_ga(filename)
    end_time = time.time()
    print_results(ga_results)
    print(f"Tiempo de ejecución de GA: {end_time - start_time:.2f} segundos\n")

# compare algorithms
def compare_algorithms():
    print("\n--- Comparativa entre PSO y GA ---")

    start_pso = time.time()
    pso_results, mean_pso, std_pso = run_pso(filename)
    end_pso = time.time()
    pso_time = end_pso - start_pso

    start_ga = time.time()
    ga_results, mean_ga, std_ga = run_ga(filename)
    end_ga = time.time()
    ga_time = end_ga - start_ga

    print(f"* Número de rutas a optimizar: {len(ga_results)}\n")

    table = PrettyTable()
    table.field_names = ["Algoritmo", "Tiempo (s)", "Media", "Desviación estándar"]
    table.add_row(["PSO", f"{pso_time:.2f}", f"{mean_pso:.2f}", f"{std_pso:.2f}"])
    table.add_row(["GA", f"{ga_time:.2f}", f"{mean_ga:.2f}", f"{std_ga:.2f}"])
    print(table)

    '''
    print("\nResultados de PSO:")
    print(pso_results)
    print(f"Tiempo de ejecución de PSO: {pso_time:.2f} segundos\n")

    print("Resultados de GA:")
    print(ga_results)
    print(f"Tiempo de ejecución de GA: {ga_time:.2f} segundos\n")
    '''

    # times comparison
    if pso_time < ga_time:
        print(">> PSO fue más rápido que GA.")
    elif ga_time < pso_time:
        print(">> GA fue más rápido que PSO.")
    else:
        print(">> Ambos algoritmos tuvieron tiempos de ejecución similares.")
    
    '''
    # costs comparison
    print(f"\nDesviación estándar de los costos mínimos:")
    print(f"PSO: {std_pso:.2f}")
    print(f"GA: {std_ga:.2f}")
    
    print(f"\nCosto promedio de las rutas:")
    print(f"PSO: {mean_pso:.2f}")
    print(f"GA: {mean_ga:.2f}")
    '''
    
    if mean_pso < mean_ga:
        print(">> PSO obtuvo un menor costo promedio.")
    elif mean_ga < mean_pso:
        print(">> GA obtuvo un menor costo promedio.")
    else:
        print(">> Ambos algoritmos obtuvieron costos promedio similares.")

import pandas as pd
import ast
import graphviz
from IPython.display import display

def plot_route(route_id, results_pso, results_ga, csv_path="./data/routes.csv"):
    #Leer el archivo CSV para obtener las distancias y los nodos
    data = pd.read_csv(csv_path)
    
    #Filtrar la información de la ruta seleccionada por ID (IDs comienzan desde 1)
    row = data[data["route_id"] == route_id].iloc[0]
    nodes = ast.literal_eval(row["nodes"])
    distances = np.array(ast.literal_eval(row["distances"]))
    
    #Obtener las rutas óptimas de PSO y GA
    try:
        route_pso = next(result for result in results_pso if result[0] == route_id)
        route_ga = next(result for result in results_ga if result[0] == route_id)
    except StopIteration:
        print(f"No se encontró la ruta con ID {route_id}")
        return
    
    best_route_pso = route_pso[2]
    best_route_ga = route_ga[2]
    cost_pso = route_pso[3]
    cost_ga = route_ga[3]
    
    #Crear el gráfico combinado
    dot = graphviz.Digraph(comment=f'Ruta ID {route_id} - PSO y GA')
    dot.attr(label=f'Comparación de Rutas para Ruta ID {route_id}\nPSO (costo: {cost_pso}) vs GA (costo: {cost_ga})', fontsize="16")
    
    #Graficar la ruta del PSO en el lado izquierdo
    with dot.subgraph(name='cluster_pso') as p:
        p.attr(label=f'PSO - Costo: {cost_pso}')
        p.attr(color='blue')
        for i in range(len(best_route_pso) - 1):
            start_node = best_route_pso[i]
            end_node = best_route_pso[i + 1]
            start_index = nodes.index(start_node)
            end_index = nodes.index(end_node)
            distance = round(distances[start_index, end_index], 2)  # Distancia con dos decimales
            p.node(f'PSO_{start_node}', str(start_node))  # Prefijo 'PSO_' para evitar conflictos de nombres
            p.node(f'PSO_{end_node}', str(end_node))
            p.edge(f'PSO_{start_node}', f'PSO_{end_node}', label=f"Dist: {distance}")
    
    #Graficar la ruta del GA en el lado derecho
    with dot.subgraph(name='cluster_ga') as g:
        g.attr(label=f'GA - Costo: {cost_ga}')
        g.attr(color='red')
        for i in range(len(best_route_ga) - 1):
            start_node = best_route_ga[i]
            end_node = best_route_ga[i + 1]
            start_index = nodes.index(start_node)
            end_index = nodes.index(end_node)
            distance = round(distances[start_index, end_index], 2)  # Distancia con dos decimales
            g.node(f'GA_{start_node}', str(start_node))  # Prefijo 'GA_' para evitar conflictos de nombres
            g.node(f'GA_{end_node}', str(end_node))
            g.edge(f'GA_{start_node}', f'GA_{end_node}', label=f"Dist: {distance}")
    
    #Guardar y mostrar el gráfico
    dot.format = 'png'
    dot.render(f'graphRoute', view=True)
    #display(dot)

def ask_and_plot():
    pso_results, mean_pso, std_pso = run_pso(filename)

    size = len(pso_results)
    route_id = int(input(f"Ingrese el ID de la ruta que desea graficar (existen {size} rutas): "))
    
    ga_results, mean_ga, std_ga = run_ga(filename)
    plot_route(route_id, pso_results, ga_results)

def main():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Ejecutar PSO")
        print("2. Ejecutar GA")
        print("3. Comparativa Express (PSO vs GA)")
        print("4. Graficar una ruta")
        print("5. Salir")
        choice = input("\nSelecciona una opción: ")

        if choice == '1':
            run_pso_algorithm()
        elif choice == '2':
            run_ga_algorithm()
        elif choice == '3':
            compare_algorithms()
        elif choice == '4':
            ask_and_plot()
        elif choice == '5':
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción inválida. Por favor, selecciona nuevamente.")

if __name__ == "__main__":
    main()