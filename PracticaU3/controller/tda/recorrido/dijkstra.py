import heapq
from controller.exception.arrayPositionException import ArrayPositionException
from controller.tda.graph.graphNoManagedLabel import GraphNoManagedLabel

class Dijkstra(GraphNoManagedLabel):
    def __init__(self, graph):
        super().__init__(graph.num_vertex)
        self._graph = graph

    def camino_corto(self, start_label, end_label):
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

            for adj in self._graph.adjacent_E(self.getLabel(current)):
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
