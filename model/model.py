import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = dict()
        self._graph = nx.Graph()
        self._nodes = []
        self._edges = []


    def buildGraph(self, durataMin):
        self._idMap = dict()
        self._graph = nx.Graph()
        self._nodes = []
        self._edges = []
        self._nodes = DAO.getAlbums(durataMin)
        for node in self._nodes:
            self._idMap[node.AlbumId] = node
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getAllEdges(durataMin)
        for edge in self._edges:
            self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]])
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAlbums(self):
        return self._nodes

    def getInfoConnessa(self, album):
        conn = nx.node_connected_component(self._graph, album)
        tot = 0
        for node in conn:
            tot += node.dTot
        return len(conn), tot