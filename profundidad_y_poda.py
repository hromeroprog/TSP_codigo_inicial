# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:54:23 2021

@author: 2rome
"""
from TSP import TSP
import time

#Adaptación realizada por Hugo Romero sobre el código de ng24_7 en geeksforgeeks
def copyToFinal(curr_path, final_path, N):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]

#Función g(TSP, list, int, int) implementada por Hugo Romero
#funcion heuristica, modificar cuando se desee para podar las ramas
#esta heuristica reduce unas 6 veces el tiempo de ejecucion
def g(tsp, visited, level, adding_node): 
    bound = 0
    for i in range(tsp.dimension):
        if not visited[i] and i != adding_node:
            bound += min([coste for coste in tsp.graph[i] if coste > 0])
    return bound

#Adaptación realizada por Hugo Romero sobre el código de ng24_7 en geeksforgeeks
def TSPRec(tsp: TSP,curr_weight, level, curr_path, visited, final_path, final_res):
    if level == tsp.dimension:
        curr_res = curr_weight + tsp.graph[curr_path[level - 1]][curr_path[0]]
        if curr_res < final_res[0]:
            copyToFinal(curr_path, final_path, tsp.dimension)
            final_res[0] = curr_res
        return
  
    for i in range(tsp.dimension): 
        if (tsp.graph[curr_path[level-1]][i] != 0 and visited[i] == False):
            curr_weight += tsp.graph[curr_path[level - 1]][i]
            curr_bound = g(tsp, visited, level, i)
            if curr_bound + curr_weight < final_res[0]:
                #print(f'Bound: {curr_bound}\tWeight: {curr_weight}\tCurrentBestSol: {final_res}\tPath: {curr_path}')
                curr_path[level] = i
                visited[i] = True
                TSPRec(tsp, curr_weight, level + 1, curr_path, visited, final_path, final_res)
                
            curr_weight -= tsp.graph[curr_path[level - 1]][i]
            # Also reset the visited array
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True
  
#Adaptación realizada por Hugo Romero sobre el código de ng24_7 en geeksforgeeks
def branchAndBound(tsp):
    start = time.time()
    final_path = [None] * (tsp.dimension + 1)
    curr_path = [-1] * (tsp.dimension + 1)
    visited = [False] * tsp.dimension
    visited[0] = True
    curr_path[0] = 0
    final_res = [float('inf')]
    TSPRec(tsp, 0, 1, curr_path, visited, final_path, final_res)
    tsp.solution = list(map(lambda x: x+1, final_path[:-1]))
    end = time.time()
    print(f'Solución profundidad y poda generada: {tsp.compute_dist()}m. {end-start} segundos.')
    return(end-start)