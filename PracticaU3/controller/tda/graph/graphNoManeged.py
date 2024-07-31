from controller.exception.arrayPositionException import ArrayPositionException
from controller.tda.graph.adjacent import Adjacent
from controller.tda.graph.graphManaged import GraphManaged

class GraphNoManaged(GraphManaged):
    def __init__(self, num_vert) -> None:
        super().__init__(num_vert)
        self.__listAdjacent = [[] for _ in range(num_vert)]

    def insert_edges_weight(self, v1, v2, weight):
        if v1 < self.num_vertex and v2 < self.num_vertex:
            if not self.exist_edges(v1, v2):
                edg = self.num_edges + 1
                self.setNumEdg(edg)
                adj = Adjacent()
                adj._destination = v2
                adj._weight = weight

                adj1 = Adjacent()
                adj1._destination = v1
                adj1._weight = weight

                self.adjacent(v1).addNode(adj, self.adjacent(v1)._length)
                self.adjacent(v2).addNode(adj1, self.adjacent(v2)._length)
                self.paint_graph()
        else:
            raise ArrayPositionException("Delimite out")

    def get_list_adjacent(self):
        return self.__listAdjacent
