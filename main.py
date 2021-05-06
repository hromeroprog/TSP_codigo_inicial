# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:02:52 2021

@author: 2rome
"""

from TSP import TSP
from profundidad_y_poda import branchAndBound

#Función main implementada por Hugo Romero
#Sirve como base para que haya un primer vistazo a como se trabajaría
if __name__ == '__main__':
    tsp = TSP() #Crear el objeto
    # fichero = "ulysses16.tsp"
    # tsp.obtener_desde_archivo_tsp(fichero)  #Lee de un archivo .tsp
    tsp.obtener_random(10) #Genera un escenario aleatorio de la dimension que le pases
    
    tsp.greedy_solve() #Genera una solucion de ruta
    tsp.draw_with_solution() #dibujar la solucion
    tsp.draw() #dibujar solo las ciudades
    tsp.opt2()
    tsp.draw_with_solution() #dibujar la solucion
    
    tsp.aplicar_mejor_solucion_desde_archivo()
    tsp.draw_with_solution()
    tsp.shuffle()
    
    tsp.draw_with_solution()
    branchAndBound(tsp)
    tsp.draw_with_solution()
    
    
    # No se recomienda probar el backtracking con el archivo .tsp,
    # si este tiene demasiadas dimensiones empezar con generaciones
    # aleatorias y tratar de reducir la computacion con podas y/o heuristicas.
    # La complejidad crece muy rápidamente y se puede bloquear el ordenador.
    
    #tsp.backtracking_solve()
    #tsp.draw_with_solution()
