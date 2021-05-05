# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:43:59 2021

@author: 2rome
"""
from matplotlib import pyplot as plt
from tools import angle, read_file
import random
import math
import numpy as np

class TSP:
    def __init__(self):
        self.nombre = ''
        self.dimension = 0
        self.problema = {}
        self.solution = []
        self.figures = 0
        self.graph = []
    
    def generate_graph(self):
        self.graph = [[self.distance(city1, city2) for city2 in list(self.problema.keys())] for city1 in list(self.problema.keys())]
        
    #GENERA UN ESCENARIO DESDE UN ARCHIVO TSP
    def obtener_desde_archivo_tsp(self, tsp_name):
        tsp_file = f"./TSP_interesantes/{tsp_name}"
        lines = read_file(tsp_file)
        self.nombre = [line.partition('NAME:')[2] for line in lines if 'NAME: ' in line][0].strip()
        self.dimension = int([line.partition('DIMENSION:')[2] for line in lines if 'DIMENSION: ' in line][0])
        index_for_search = [index for index,line in enumerate(lines) if 'NODE_COORD_SECTION' in line][0]  +1
        cities_data = lines[index_for_search:index_for_search + self.dimension]
        self.problema = {}
        for city in cities_data:
            idx,x,y = map(float, city.split(' '))
            self.problema[int(idx)] = (x,y)
        
        self.generate_graph()
        print(f'Fichero {tsp_name} parseado con exito')
    
    #GENERA UN ESCENARIO ALEATORIO DE {dimension} CIUDADES
    def obtener_random(self, dimension):
        self.nombre = f'Aleatorio {dimension} dimensiones'
        self.dimension = dimension
        self.problema = {}
        for i in range(1, dimension+1):
            self.problema[i] =  round(random.random()*50,2), round(random.random()*50, 2)
        self.generate_graph()
    
    #POR IMPLEMENTAR, DE MOMENTO HACE UNA SOLUCION ALEATORIA
    def solve(self):
        self.solution = list(self.problema.keys())
        random.shuffle(self.solution)
        self.ordenar_solucion()
    
    #SOLUCION CON ALGORITMO GREEDY
    def greedy_solve(self):
        self.solution = list(self.problema.keys())
        to_put = set(self.solution)
        
        new_solution = [self.solution[0]]
        to_put.remove(self.solution[0])
        
        
        while(len(to_put) > 1):
            current = new_solution[-1]
            current_distance = float('inf')
            current_best = -1
            
            for city in to_put:
                dist = self.distance(current, city)
                if dist < current_distance:
                    current_distance = dist
                    current_best = city
            
            new_solution.append(current_best)
            to_put.remove(current_best)  
        new_solution.append(to_put.pop())
        
        self.solution = new_solution
        self.ordenar_solucion()  #Puede que haya que quitarlo para estudiar la complejidad
        print(f'Solución greedy generada: {self.compute_dist()}m')
    
    
    #SOLUCION CON ALGORITMO BASADO EN GRADOS RESPECTO AL CENTRO
    def r_solve(self):
        x = [coord[0] for coord in self.problema.values()]
        y = [coord[1] for coord in self.problema.values()]
        
        center = [np.mean(x), np.mean(y)]
        self.solution.sort(key=lambda point: angle(self.problema[point], center))
        print(f'Solucion r: {self.compute_dist()} m')
        self.ordenar_solucion()  #Puede que haya que quitarlo para estudiar la complejidad
        print(f'Solucion r: {self.compute_dist()} m')
    
    
    # def backtracking_solve(self):
    #     answer = []
    #     paths = []
    #     graph = self.graph.copy()
  
    #     # Boolean array to check if a node
    #     # has been visited or not
    #     v = [False for i in range(self.dimension)]
      
    #     # Mark 0th node as visited
    #     v[0] = True
  
    #     # Find the minimum weight Hamiltonian Cycle
    #     self.tsp_backtracking(graph, v, 0, self.dimension, 1, 0, answer, paths)
    #     print(min(answer))
    #     print(paths)
    #     print(v)
        
    # def tsp_backtracking(self,graph, v, currPos, n, count, cost, answer, paths):
    #     if (count == n and graph[currPos][0]):
    #         answer.append(cost + graph[currPos][0])
    #         return
    #     # BACKTRACKING STEP
    #     # Loop to traverse the adjacency list
    #     # of currPos node and increasing the count
    #     # by 1 and cost by graph[currPos][i] value
    #     for i in range(self.dimension):
    #         if (v[i] == False and graph[currPos][i]):
    #         # Mark as visited
    #             v[i] = True
    #             self.tsp_backtracking(graph, v, i, n, count + 1, cost + graph[currPos][i], answer, paths)
              
    #             # Mark ith node as unvisited
    #             v[i] = False
    
    #CALCULA LA LONGITUD DE LA RUTA ACTUAL DEL PROBLEMA
    def compute_dist(self):
        total_dist = 0
        for index in range(len(self.solution)):
            total_dist += self.distance(self.solution[index], self.solution[(index+1)%len(self.solution)])
        return total_dist

    #CALCULA LA DISTANCIA ENTRE DOS CIUDADES
    def distance(self, city1, city2):
        return math.sqrt((self.problema[city1][0]-self.problema[city2][0])**2 + (self.problema[city1][1]-self.problema[city2][1])**2)


    #DESPLAZA LA SOLUCION PARA QUE LA RUTA COMIENCE POR LA PRIMERA CIUDAD
    def ordenar_solucion(self):
        primero = None
        while(primero != list(self.problema.keys())[0]):
            primero = self.solution.pop(0)
            self.solution.append(primero)
            
        self.solution = self.solution[:-1]
        self.solution.insert(0,primero)


    #DIBUJA EL PROBLEMA
    def draw(self):
        x = [coord[0] for coord in self.problema.values()]
        y = [coord[1] for coord in self.problema.values()]
        names = list(self.problema.keys())
        
        width = 9.6
        height = 7.2
        bool_dim = self.dimension > 20
        figsize = [width+(width*bool_dim), height+(height*bool_dim)]
        plt.figure(self.figures, figsize = figsize)
        
        self.figures+=1
        plt.scatter(x,y,s=15, marker = 'x', c = 'black')
        for txt,x_coord, y_coord in zip(names, x, y):
            plt.annotate(txt, (x_coord, y_coord))
        plt.xlim(min(x)-1, max(x) +1)
        plt.suptitle(f'{self.nombre} sin solucion', fontsize = 14)
    
    #DIBUJA LA SOLUCION
    def draw_with_solution(self):
        self.draw()
        for index in range(len(self.solution)):
            x_values = self.problema[self.solution[index]][0], self.problema[self.solution[(index+1)%len(self.solution)]][0]
            y_values = self.problema[self.solution[index]][1], self.problema[self.solution[(index+1)%len(self.solution)]][1]
            plt.plot(x_values, y_values, 'red')
        plt.suptitle(f'{self.nombre} con solucion', fontsize = 14)
        plt.title('Ruta: ' + ', '.join(map(str, self.solution + [self.solution[0]])), fontsize = 10)
    
    def __str__(self):
        result = f'Problema de {self.dimension} ciudades:'
        for city in self.problema.keys():
            result += f'\n{city}: {self.problema[city]}' 
        return result

                   