import random
import sys
import time
sys.path.append('../')
from controller.tda.graph.graphNoManagedLabel import GraphNoManagedLabel
from controller.tda.graph.graphNoManagedLabel import GraphNoManaged


try :
 gp = GraphNoManagedLabel(num_vert=5)
 inicio = time.time()
 gp.camino_dijkstra(0, 5)
 fin = time.time()
 print("Dijkstra")
 print(f"Tiempo de ejecución: {fin-inicio}")
 inicio = time.time()
 gp.camino_floyd(0, 5)
 fin = time.time()
 print(f"Tiempo de ejecución: {fin-inicio}")
 print("Floyd")
except Exception as e:
 print(e)
