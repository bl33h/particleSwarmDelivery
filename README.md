# Proyecto Final 
Desarrollo de un algoritmo de enjambre de partículas para optimizar rutas de entrega, considerando demanda variable, costo de combustible y otros gastos. Además se realiza una comparación con Algoritmos Genéticos.

## Descripción de los avances (22/10/2024)
* Se ha avanzado en la implementación del algoritmo de Enjambre de Partículas (PSO) para la optimización de rutas de entrega. 
* El modelo inicial incluye una estructura básica donde las rutas se representan como permutaciones de nodos, y se ha definido una función objetivo que toma en cuenta tanto las distancias entre ubicaciones como los costos de combustible y las demandas variables de entrega, modeladas como una distribución aleatoria. 
* Además, se han generado de manera aleatoria tanto las distancias entre los nodos como los costos de combustible y las demandas en cada punto de entrega. 
* El algoritmo ha sido configurado para iterar y mejorar las soluciones, buscando minimizar el costo total de la ruta.

## Descripción de los avances (07/11/2024)
* Se ha implementado un algoritmo Genético (GA) para optimizar las rutas de entrega, ofreciendo una alternativa comparativa al Enjambre de Partículas (PSO).
* El modelo inicial del GA considera rutas de entrega como permutaciones de nodos, y se ha desarrollado una función de aptitud que evalúa cada ruta en función de la distancia entre ubicaciones, el costo de combustible y la demanda variable de entrega en cada nodo.
* La demanda y los costos de combustible para cada nodo se han generado de manera aleatoria, permitiendo que el algoritmo optimice en un escenario realista con variabilidad de demanda y costos.
* En el proceso, el GA utiliza operadores de selección, cruce (crossover) y mutación:
    * Selección: Se implementa una selección por torneo, favoreciendo rutas con menores costos totales.
    * Cruce: Se emplea un cruce en un punto, con un filtro para preservar rutas válidas y evitar nodos repetidos.
    * Mutación: Introduce variabilidad adicional mediante el intercambio aleatorio de nodos en algunas rutas.
* El algoritmo se configura para iterar durante varias generaciones, mejorando progresivamente las rutas para reducir el costo total, considerando tanto las demandas como los costos asociados a cada nodo.