# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:02:52 2021

@author: 2rome
"""

from TSP import TSP

if __name__ == '__main__':
    tsp = TSP() #Crear el objeto
    fichero = "ulysses16.tsp"
    #tsp.obtener_desde_archivo_tsp(fichero)  #Lee de un archivo .tsp
    tsp.obtener_random(12) #Genera un escenario aleatorio de la dimension que le pases
    tsp.greedy_solve() #Genera una solucion de ruta
    tsp.draw_with_solution() #dibujar la solucion
    #tsp.draw() #dibujar solo las ciudades
    
    tsp.r_solve() #Genera una solucion de ruta
    tsp.draw_with_solution() #dibujar la solucion
    tsp.backtracking_solve()