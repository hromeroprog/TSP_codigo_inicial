# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:43:59 2021

@author: 2rome
Todo el codigo ha sido generado con el objetivo de que sirva como punto de partida 
para el trabajo de TSP. Las funciones no han sido especialmente optimizadas
y se recomienda hacer modificaciones propias en caso de que el analisis genere problemas
"""

from matplotlib import pyplot as plt
from tools import read_file
import random
import math
import time


class TSP:
   #Función __init__(TSP) implementada por Hugo Romero
   #CONSTRUCTOR DE LA CLASE TSP
    def __init__(self):
        self.nombre = ''
        self.filename = ''
        self.dimension = 0
        self.problema = {}
        self.solution = []
        self.figures = 0
        self.graph = []
    
    #Función generate_graph(self) implementada por Hugo Romero
    #Calcula y almacena en graph las aristas (carreteras) entre ciudades (todas, dado que es un nodo completo)
    def generate_graph(self):
        self.graph = [[self.distance(city1, city2) for city2 in list(self.problema.keys())] for city1 in
                      list(self.problema.keys())]
    
    #Función obtener_desde_archivo_tsp(self, string) implementada por Hugo Romero
    # Genera un escenario a partir de un archivo .tsp, debe estar en la carpeta TSP_interesantes
    # Se espera que sea un archivo tsp de vertices (coordenadas), no de aristas.
    def obtener_desde_archivo_tsp(self, tsp_name):
        tsp_file = f"./TSP_interesantes/{tsp_name}"
        lines = read_file(tsp_file)
        self.nombre = [line.partition('NAME:')[2] for line in lines if 'NAME: ' in line][0].strip()
        self.filename = tsp_name
        self.dimension = int([line.partition('DIMENSION:')[2] for line in lines if 'DIMENSION: ' in line][0])
        index_for_search = [index for index, line in enumerate(lines) if 'NODE_COORD_SECTION' in line][0] + 1
        cities_data = lines[index_for_search:index_for_search + self.dimension]
        self.problema = {}
        for city in cities_data:
            idx, x, y = map(float, city.split(' '))
            self.problema[int(idx)] = (x, y)

        self.generate_graph()
        self.solution = list(self.problema.keys())
        print(f'Fichero {tsp_name} parseado con exito')
    
    #Función aplicar_mejor_solucion_desde_archivo(self) implementada por Hugo Romero
    #Si el escenario proviene de un fichero tsp, lee la solucion del archivo de
    #solucion correspondiente
    def aplicar_mejor_solucion_desde_archivo(self):
        if '.tsp' not in self.filename:
            print(f'El escenario {self.nombre} no fue generado apartir de un archivo .tsp')
            return
        solution_file = "./TSP_interesantes/" + self.filename.replace('.tsp', '') + ".opt.tour"
        lines = read_file(solution_file)
        index_for_search = [index for index, line in enumerate(lines) if 'TOUR_SECTION' in line][0] + 1

        next_line = lines[index_for_search]
        # if else porque a veces la solucion a parece en una sola linea y a veces en varias
        if sum([str(city) in next_line for city in self.solution]) == self.dimension:
            self.solution = list(map(int, next_line.split(' ')))
        else:
            self.solution = list(map(int, lines[index_for_search:index_for_search + self.dimension]))
            print(self.solution)
        self.ordenar_solucion()
        print(f'Solucion desde archivo: {self.compute_dist()} m')
    
    #Función obtener_random(self, int) implementada por Hugo Romero
    # Genera un escenario aleatorio de {dimension} CIUDADES
    def obtener_random(self, dimension):
        self.nombre = f'Aleatorio {dimension} dimensiones'
        self.dimension = dimension
        self.problema = {}
        for i in range(1, dimension + 1):
            self.problema[i] = round(random.random() * 50, 2), round(random.random() * 50, 2)
        self.generate_graph()
        self.solution = list(self.problema.keys())
    
    #Función shuffle(self) implementada por Hugo Romero
    # PARA DESORDENAR LAS CIUDADES DE LA SOLUCION
    # Puede ser util para evaluar varias soluciones sobre un mismo escenario
    # pero que una soluciones no influyan sobre las otras
    def shuffle(self):
        random.shuffle(self.solution)
        self.ordenar_solucion()
    
    #Función greedy_solve(self) -> float implementada por Hugo Romero
    #Solucion con algoritmo greedy, la siguiente ciudad es la mas cercana no visitada
    #Devuelve el tiempo de ejecucion del algoritmo
    def greedy_solve(self):
        start = time.time()
        to_put = set(self.solution)
        new_solution = [self.solution[0]]
        to_put.remove(self.solution[0])
        while (len(to_put) > 1):
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
        end = time.time()
        self.ordenar_solucion()
        print(f'Solución greedy generada: {self.compute_dist()}m')
        return end - start

    
    #Función opt2(self) -> float implementada por Hugo Romero
    #La funcion adapta el pseudocodigo de la pagina
    #de wikipedia del 2-opt
    def opt2(self):
        start = time.time()
        improved = True
        while improved:
            improved = False
            best_distance = self.compute_dist()
            for i in range(1, self.dimension - 2):
                for j in range(i + 2, self.dimension):
                    new_route = self.solution.copy()
                    new_route[i:j] = self.solution[j - 1:i - 1:-1]  # operador 2opt
                    new_distance = sum(
                        [self.distance(new_route[index], new_route[(index + 1) % len(new_route)]) for index in
                         range(len(new_route))])

                    if new_distance < best_distance:
                        self.solution = new_route
                        best_distance = new_distance
                        improved = True
                    if improved:
                        break
                if improved:
                    break
        end = time.time()
        self.ordenar_solucion()
        print(f'Solucion 2-opt: {self.compute_dist()} m')
        return end - start

    def backtracking_solve(self):
        """
        Método realizada por:
            - Hugo Romero
            - - Grupo 10: Ramsés Contreras, Alejandro de la Vega, Ricardo Grande
        Calls backtracking method and stores solution's path and minimum weight. Calls for optimized
        backtracking are commented.
        :return: backtracking execution time
        """
        answer = []
        paths = []
        graph = self.graph.copy()

        # USED IN DFBnB: Stores best solution found
        #temp_sol = [float("inf")]

        # Boolean array to check if a node
        # has been visited or not
        v = [False for i in range(self.dimension)]

        # Mark 0th node as visited
        v[0] = True

        # Find the minimum weight Hamiltonian Cycle
        start = time.time()
        self.tsp_backtracking(graph, v, 0, self.dimension, 1, 0, answer, "1", paths)
        # Splits solution by separator and converts each element to int to be stored as a list of ints
        self.solution = [int(x) for x in paths[answer.index(min(answer))].split("->")]
        end = time.time()
        print(min(answer))
        print(self.solution)

        # USED IN DFBnB: Finds the minimum weight Hamiltonian Cycle using DFBnB
        # start = time.time()
        # self.tsp_backtracking_dfbb(graph, v, 0, self.dimension, 1, 0, answer, "1", paths, temp_sol)
        # self.solution = [int(x) for x in paths[answer.index(min(answer))].split("->")]
        # end = time.time()
        # print(min(answer))

        self.ordenar_solucion()
        print(f'Solucion backtracking: {self.compute_dist()} m')
        return end - start

    def tsp_backtracking(self, graph, v, currPos, n, count, cost, answer, path, all_paths):
        """
        Adaptación realizada por:
            - Hugo Romero
            - Grupo 10: Ramsés Contreras, Alejandro de la Vega, Ricardo Grande
        sobre el código de Mohit Kumar en geeksforgeeks.org
        :param graph: matriz representando el grafo del problema
        :param v: vector booleano de nodos, true si han sido visitados, false si no.
        :param currPos: nodo actual
        :param n: número total de nodos
        :param count: número de nodos visitados
        :param cost: coste acumulado
        :param answer: lista con el coste de todas las soluciones encontradas
        :param path: recorrido local de la rama
        :param all_paths: lista con los recorridos de todas las soluciones encontradas
        :return:
        """
        if count == n and graph[currPos][0]:
            answer.append(cost + graph[currPos][0])
            # Append local path to all_paths (stores all solutions' paths)
            all_paths.append(path)
            return
        # BACKTRACKING STEP
        # Loop to traverse the adjacency list
        # of currPos node and increasing the count
        # by 1 and cost by graph[currPos][i] value
        for i in range(self.dimension):
            if v[i] is False and graph[currPos][i]:
                # Mark as visited
                v[i] = True
                self.tsp_backtracking(graph, v, i, n, count + 1, cost + graph[currPos][i],
                                      answer, path + "->" + str(i + 1), all_paths)

                # Mark ith node as unvisited
                v[i] = False

    def tsp_backtracking_dfbnb(self, graph, v, currPos, n, count, cost, answer, path, all_paths, best_sol):
        """
        Adaptación realizada por:
            - Grupo 10: Ramsés Contreras, Alejandro de la Vega, Ricardo Grande
        sobre el código de Mohit Kumar en geeksforgeeks.org para incluir la mejora de poda.
        :param graph: matriz representando el grafo del problema
        :param v: vector booleano de nodos, true si han sido visitados, false si no.
        :param currPos: nodo actual
        :param n: número total de nodos
        :param count: número de nodos visitados
        :param cost: coste acumulado
        :param answer: lista con el coste de todas las soluciones encontradas
        :param path: recorrido local de la rama
        :param all_paths: lista con los recorridos de todas las soluciones encontradas
        :param best_sol: almacena la mejor solución encontrada hasta el momento
        :return:
        """
        if count == n and graph[currPos][0]:
            answer.append(cost + graph[currPos][0])
            # Append local path to all_paths (stores all solutions' paths)
            all_paths.append(path)
            # Updates best solution found
            best_sol[0] = (cost + graph[currPos][0])
            return
        # BACKTRACKING STEP
        # Loop to traverse the adjacency list
        # of currPos node and increasing the count
        # by 1 and cost by graph[currPos][i] value
        for i in range(self.dimension):
            if v[i] is False and graph[currPos][i]:
                # Expand only if current branch has lower weight than best solution found so far
                if cost + graph[currPos][i] < best_sol[0]:
                    # Mark as visited
                    v[i] = True
                    self.tsp_backtracking_dfbnb(graph, v, i, n, count + 1, cost + graph[currPos][i],
                                                answer, path + "->" + str(i + 1), all_paths, best_sol)

                    # Mark ith node as unvisited
                    v[i] = False


    #Función compute_dist(self) -> float implementada por Hugo Romero
    #Calcula la distancia actual de la ruta solucion
    def compute_dist(self):
        total_dist = 0
        for index in range(len(self.solution)):
            total_dist += self.distance(self.solution[index], self.solution[(index + 1) % len(self.solution)])
        return total_dist
    
    #Función distance(self, int, int) -> float implementada por Hugo Romero
    # Devuelve la distancia entre dos ciudades
    def distance(self, city1, city2):
        return math.sqrt((self.problema[city1][0] - self.problema[city2][0]) ** 2 + (
                self.problema[city1][1] - self.problema[city2][1]) ** 2)
    
    #Función ordenar_solucion(self) implementada por Hugo Romero
    # Desplaza (shift) la solucion para que la ruta comience por la primera ciudad
    def ordenar_solucion(self):
        primero = None
        while (primero != list(self.problema.keys())[0]):
            primero = self.solution.pop(0)
            self.solution.append(primero)

        self.solution = self.solution[:-1]
        self.solution.insert(0, primero)
    
    #Función draw(self) implementada por Hugo Romero
    # Dibuja el problema
    def draw(self):
        x = [coord[0] for coord in self.problema.values()]
        y = [coord[1] for coord in self.problema.values()]
        names = list(self.problema.keys())

        width = 9.6
        height = 7.2
        bool_dim = self.dimension > 20
        figsize = [width + (width * bool_dim), height + (height * bool_dim)]
        plt.figure(self.figures, figsize=figsize)

        self.figures += 1
        plt.scatter(x, y, s=15, marker='x', c='black')
        for txt, x_coord, y_coord in zip(names, x, y):
            plt.annotate(txt, (x_coord, y_coord))
        plt.xlim(min(x) - 1, max(x) + 1)
        plt.suptitle(f'{self.nombre} sin solucion', fontsize=14)

    #Función draw(self) implementada por Hugo Romero
    # Dibuja el problema con la solucion actual
    def draw_with_solution(self):
        self.draw()
        for index in range(len(self.solution)):
            x_values = self.problema[self.solution[index]][0], \
                       self.problema[self.solution[(index + 1) % len(self.solution)]][0]
            y_values = self.problema[self.solution[index]][1], \
                       self.problema[self.solution[(index + 1) % len(self.solution)]][1]
            plt.plot(x_values, y_values, 'red')
        plt.suptitle(f'{self.nombre} con solucion', fontsize=14)
        plt.title('Ruta: ' + ', '.join(map(str, self.solution + [self.solution[0]])), fontsize=10)
        # plt.show() #En algunos casos necesitareis descomentar esta linea para que se vean las figuras generadas
        
    #Función __str__(self) -> string implementada por Hugo Romero
    # Devuelve un string del problema, con el nombre la dimension y la solucion
    def __str__(self):
        result = f'Problema {self.nombre}\n\t-{self.dimension} ciudades'
        result += f"\n\t-Actual solucion:\t{', '.join(map(str, self.solution))}"
        return result
