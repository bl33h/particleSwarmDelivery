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
    - Modificado el 09/11/2024
"""

import time
from algorithms.pso import run_pso
from algorithms.ga import run_ga
import numpy as np

# pso algorithm
def run_pso_algorithm():
    print("\n--- Ejecutando PSO ---")
    start_time = time.time()
    pso_results = run_pso()
    end_time = time.time()
    print(pso_results)
    print(f"Tiempo de ejecución de PSO: {end_time - start_time:.2f} segundos\n")

# ga algorithm
def run_ga_algorithm():
    print("\n--- Ejecutando GA ---")
    start_time = time.time()
    ga_results = run_ga()
    end_time = time.time()
    print(ga_results)
    print(f"Tiempo de ejecución de GA: {end_time - start_time:.2f} segundos\n")

# compare algorithms
def compare_algorithms():
    print("\n--- Comparativa entre PSO y GA ---")

    start_pso = time.time()
    pso_results, mean_pso, std_pso = run_pso()
    end_pso = time.time()
    pso_time = end_pso - start_pso

    start_ga = time.time()
    ga_results, mean_ga, std_ga = run_ga()
    end_ga = time.time()
    ga_time = end_ga - start_ga

    print("\nResultados de PSO:")
    print(pso_results)
    print(f"Tiempo de ejecución de PSO: {pso_time:.2f} segundos\n")

    print("Resultados de GA:")
    print(ga_results)
    print(f"Tiempo de ejecución de GA: {ga_time:.2f} segundos\n")

    # times comparison
    if pso_time < ga_time:
        print(">> PSO fue más rápido que GA.")
    elif ga_time < pso_time:
        print(">> GA fue más rápido que PSO.")
    else:
        print(">> Ambos algoritmos tuvieron tiempos de ejecución similares.")
        
    # costs comparison
    print(f"\nDesviación estándar de los costos mínimos:")
    print(f"PSO: {std_pso:.2f}")
    print(f"GA: {std_ga:.2f}")
    
    print(f"\nCosto promedio de las rutas:")
    print(f"PSO: {mean_pso:.2f}")
    print(f"GA: {mean_ga:.2f}")
    
    if mean_pso < mean_ga:
        print(">> PSO obtuvo un menor costo promedio.")
    elif mean_ga < mean_pso:
        print(">> GA obtuvo un menor costo promedio.")
    else:
        print(">> Ambos algoritmos obtuvieron costos promedio similares.")
    
    

def main():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Ejecutar PSO")
        print("2. Ejecutar GA")
        print("3. Comparativa Express (PSO vs GA)")
        print("4. Salir")
        choice = input("\nSelecciona una opción: ")

        if choice == '1':
            run_pso_algorithm()
        elif choice == '2':
            run_ga_algorithm()
        elif choice == '3':
            compare_algorithms()
        elif choice == '4':
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción inválida. Por favor, selecciona nuevamente.")

if __name__ == "__main__":
    main()
