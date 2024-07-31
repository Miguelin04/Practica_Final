from math import inf
from controller.exception.arrayPositionException import ArrayPositionException
from controller.tda.graph.graphNoManagedLabel import GraphNoManagedLabel

class Floyd(GraphNoManagedLabel):
    def __init__(self, graph):
        super().__init__(graph.num_vertex)
        self._graph = graph

    def floyd(self):
        distances = [[inf] * self.num_vertex for _ in range(self.num_vertex)]
        next_node = [[None] * self.num_vertex for _ in range(self.num_vertex)]

        for u in range(self.num_vertex):
            for adj in self._graph.adjacent_E(self.getLabel(u)):
                v = adj._destination
                distances[u][v] = adj._weight
                next_node[u][v] = v

        for k in range(self.num_vertex):
            for i in range(self.num_vertex):
                for j in range(self.num_vertex):
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        next_node[i][j] = next_node[i][k]

        return distances, next_node

    def camino_corto(self, start_label, end_label):
        start = self.getVertex(start_label)
        end = self.getVertex(end_label)
        if start == -1 or end == -1:
            raise ArrayPositionException("Start or end vertex not found")

        distances, next_node = self.floyd()
        if next_node[start][end] is None:
            return [], float('inf')

        path = [start]
        while start != end:
            start = next_node[start][end]
            path.append(start)

        return [self.getLabel(v) for v in path], distances[self.getVertex(start_label)][self.getVertex(end_label)]