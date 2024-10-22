# Proyecto Final 
Desarrollo de un algoritmo de enjambre de partículas para optimizar rutas de entrega, considerando demanda variable, costo de combustible y otros gastos. Además se realiza una comparación con Algoritmos Genéticos.

## Descripción de los avances (220/10/2024)
* Se ha avanzado en la implementación del algoritmo de Enjambre de Partículas (PSO) para la optimización de rutas de entrega. 
* El modelo inicial incluye una estructura básica donde las rutas se representan como permutaciones de nodos, y se ha definido una función objetivo que toma en cuenta tanto las distancias entre ubicaciones como los costos de combustible y las demandas variables de entrega, modeladas como una distribución aleatoria. 
* Además, se han generado de manera aleatoria tanto las distancias entre los nodos como los costos de combustible y las demandas en cada punto de entrega. 
* El algoritmo ha sido configurado para iterar y mejorar las soluciones, buscando minimizar el costo total de la ruta.