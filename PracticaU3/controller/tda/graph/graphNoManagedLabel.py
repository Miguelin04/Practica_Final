from controller.tda.graph.graphNoManeged import GraphNoManaged
from controller.exception.arrayPositionException import ArrayPositionException
from math import nan, inf
import heapq

class GraphNoManagedLabel(GraphNoManaged):
    def __init__(self, num_vert):
        super().__init__(num_vert)
        self.__labels = []
        self.__labelsVertex={}
        for i in range(0, self.num_vertex):
            self.__labels.append(None)

    @property
    def getListAdjacent(self):
        return self.__listAdjacent
        
    def getVertex(self, label):
        try:
            return self.__labelsVertex[str(label)]
        except Exception as error:
            return -1    
    
    def label_vertex(self, v, label):
        self.__labels[v] = label
        self.__labelsVertex[str(label)] = v
        
    def getLabel(self, v):
        return self.__labels[v]
    
    def exist_edge_E(self, label1, label2):
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            return self.exist_edges(v1, v2)
        else:
            return False
        
    def insert_edges_weight_E(self, label1, label2, weight): #sirve para insertar aristas con peso
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            self.insert_edges_weight(v1, v2, weight)
        else:
            raise ArrayPositionException("Vertex not found") 
        
    def insert_edges_E(self, label1, label2): #sirve para insertar aristas
        self.insert_edges_weight_E(label1, label2, nan)
    
    def weight_edges_E(self, label1, label2): #sirve para obtener el peso de las aristas
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            return self.weight_edges(v1, v2)
        else:
            raise ArrayPositionException("Vertex not found") 
        
    def adjacent_E(self, label1): #sirve para obtener los vertices adyacentes
        v1 = self.getVertex(label1)
        if v1 != -1:
            return self.adjacent(v1).toArray
        else:
            raise ArrayPositionException("Vertex not found")
        
    @property
    def serializar(self):
        adyacencias = []
        for i in range(len(self.__labels)):
            list_adj = self.adjacent_E(self.__labels[i])
            for j in range(len(list_adj)):
                dic = {}
                dic["from"] = i + 1
                dic["to"] = self.adjacent(i).getNode(j)._destination + 1
                adyacencias.append(dic)
        return {
           "vertices": self.num_vertex,
            "aristas": self.num_edges,
            "etiquetas": self.__labels,
            "etiquetasVertice": self.__labelsVertex,
            "adyacencias": adyacencias
              
        }

       
    @classmethod 
    def deserializar(self, dic):
        graph = GraphNoManagedLabel(int(dic["vertices"]))
        graph.__labelsVertex = dic["etiquetasVertice"]
        graph.__labels = dic["etiquetas"]
        graph.__listAdjacent = dic["adyacencias"]
        graph.__numEdg = dic["aristas"]
        return graph
    ### Método Dijkstra
    def dijkstra(self, start_label):
        start = self.getVertex(start_label)
        distances = {v: float('infinity') for v in range(self.num_vertex)}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_distance > distances[current_vertex]:
                continue

            list_adj = self.adjacent(current_vertex).toArray
            for adj in list_adj:
                neighbor = adj._destination
                weight = adj._weight
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    def camino_dijkstra(self, start_label, end_label):
        start = self.getVertex(start_label)
        end = self.getVertex(end_label)
        if start == -1 or end == -1:
            raise ArrayPositionException("Start or end vertex not found")

        distances = {vertex: float('infinity') for vertex in range(self.num_vertex)}
        previous_vertices = {vertex: None for vertex in range(self.num_vertex)}
        distances[start] = 0
        vertices = set(range(self.num_vertex))

        while vertices:
            current = min(vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current)

            if distances[current] == float('infinity'):
                break

            for adj in self.adjacent(current).toArray:
                neighbor = adj._destination
                cost = adj._weight
                alternative_route = distances[current] + cost
                if alternative_route < distances[neighbor]:
                    distances[neighbor] = alternative_route
                    previous_vertices[neighbor] = current

        path, current = [], end
        while previous_vertices[current] is not None:
            path.insert(0, current)
            current = previous_vertices[current]
        if path:
            path.insert(0, current)
        return [self.getLabel(v) for v in path], distances[end]

    ### Método Floyd
    def floyd(self):
        num_v = self.num_vertex
        distances = [[inf] * num_v for _ in range(num_v)]
        next_node = [[None] * num_v for _ in range(num_v)]

        for v in range(num_v):
            distances[v][v] = 0

        for v in range(num_v):
            list_adj = self.adjacent_E(self.getLabel(v))
            for adj in list_adj:
                u = adj._destination
                weight = adj._weight
                distances[v][u] = weight
                next_node[v][u] = u

        for k in range(num_v):
            for i in range(num_v):
                for j in range(num_v):
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        next_node[i][j] = next_node[i][k]

        return distances, next_node

    def camino_floyd(self, start_label, end_label):
        start = self.getVertex(start_label)
        end = self.getVertex(end_label)
        if start == -1 or end == -1:
            raise ArrayPositionException("Start or end vertex not found")
        distances, next_node = self.floyd()
        if next_node[start][end] is None:
            return [], inf
        path = [start]
        while start != end:
            start = next_node[start][end]
            path.append(start)
        return [self.getLabel(v) for v in path], distances[self.getVertex(start_label)][self.getVertex(end_label)]
