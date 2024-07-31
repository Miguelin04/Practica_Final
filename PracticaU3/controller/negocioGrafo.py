from controller.tda.graph.graphNoManagedLabel import GraphNoManagedLabel
from controller.casinoControl import CasinoControl
from controller.distancia import Distancia
import os, re, json
from controller.tda.graph.adjacent import Adjacent
from models.casino import Casino

class NegocioGrafo():
    def __init__(self):
        self.__grafo = None
        self.__ndao = CasinoControl()
        self.__dirPhysical = "static/d3/grafo.js"
        self.__json_folder = "data/grafo.json"
        
    @property
    def _grafo(self):
        if self.__grafo is None:
            self.create_graph()
        return self.__grafo

    @_grafo.setter
    def _grafo(self, value):
        self.__grafo = value

    def create_graph(self, origen=None, destino=None, reiniciar=False):
        if os.path.exists(self.__json_folder) and not reiniciar:
            list = self.__ndao._list()
            if list._length > 0:
                self.__grafo = GraphNoManagedLabel(list._length)
                arr = list.toArray
                [self.__grafo.label_vertex(i, negocio._nombre) for i, negocio in enumerate(arr)]

                if os.path.exists(self.__dirPhysical):
                    with open(self.__dirPhysical, 'r') as file:
                        for line in file:
                            if "from:" in line:
                                line = line.strip()
                                try:
                                    o_match = re.search(r'from:\s*(\d+)', line)
                                    d_match = re.search(r'to:\s*(\d+)', line)
                                    w_match = re.search(r'label:"([\d.]+)"', line)
                                    
                                    if o_match and d_match and w_match:
                                        o = o_match.group(1)
                                        d = d_match.group(1)
                                        w = w_match.group(1)
                                        
                                        negocioOrigen = self.__ndao._list().binary_search_models_int(int(o), "_id")
                                        negocioDestino = self.__ndao._list().binary_search_models_int(int(d), "_id")
                                        
                                        if negocioOrigen and negocioDestino:
                                            self.__grafo.insert_edges_weight_E(negocioOrigen._nombre, negocioDestino._nombre, float(w))
                                        else:
                                            print(f"Error: no se encontraron negocios para los IDs {o} y {d}")
                                    else:
                                        print(f"Error: línea no coincide con el formato esperado: {line}")
                                except Exception as e:
                                    print(f"Error al procesar la línea: {line}. Excepción: {e}")

                if origen and destino:
                    if isinstance(origen, Casino) and isinstance(destino, Casino):
                        peso = round(Distancia().haversine(origen._latitud, origen._longitud, destino._latitud, destino._longitud), 3)
                        self.__grafo.insert_edges_weight_E(origen._nombre, destino._nombre, peso)
                    else:
                        print("Error: origen o destino no son del tipo Casino")
                    
                self.__grafo.paint_graph()
                self.saveGraph # Llamar al método para guardar el grafo
            else:
                list = self.__ndao._list()
                if list._length > 0:
                    self.__grafo = GraphNoManagedLabel(list._length)
                    arr = list.toArray
                    for i in range(0, len(arr)):
                        self.__grafo.label_vertex(i, arr[i]._nombre)
                    self.__grafo.paint_graph()
                    self.saveGraph
        else:
            print("El archivo JSON no existe o está vacío. Creando un grafo vacío.")
            list = self.__ndao._list()
            if list._length > 0:
                self.__grafo = GraphNoManagedLabel(list._length)
                arr = list.toArray
                for i in range(0, len(arr)):
                    self.__grafo.label_vertex(i, arr[i]._nombre)
                self.__grafo.paint_graph()
                self.saveGraph

    @property      
    def saveGraph(self):
        if self.__grafo is not None:
            json_folder = "data"
            json_file = os.path.join(json_folder, "grafo.json")
            grafo_serializado = self.__grafo.serializar
            
            if os.path.exists(json_file):
                os.remove(json_file)
                
            with open(json_file, 'w') as file:
                json.dump(grafo_serializado, file, indent=4)
            return True
        else:
            return False
        
    @property
    def loadGraph(self):
        json_folder = "data"
        json_file = os.path.join(json_folder, "grafo.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                data = json.load(file)
                return GraphNoManagedLabel.deserializar(data)
        else:
            print(f"El archivo {json_file} no existe.")
            return None
