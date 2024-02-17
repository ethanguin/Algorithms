#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        self.source = None
        self.dest = None
        self.shortest_paths = None
        self.network = None

    def initializeNetwork(self, network):
        assert (type(network) is CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE
        path = self.shortest_paths[destIndex][1]  # Get the list of (node_id, edge_length) tuples
        path_edges = []
        total_length = 0
        for i in range(len(path) - 1):
            node_id, edge_length = path[i]  # Unpack the tuple
            next_node_id, next_edge_length = path[i + 1]  # Unpack the next tuple
            node = self.network.nodes[node_id]
            next_node = self.network.nodes[next_node_id]
            edge = CS312GraphEdge(node, next_node, next_edge_length)
            path_edges.append((node.loc, next_node.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if use_heap is False:
            self.shortest_paths = self.network.dijkstraArray(srcIndex)
        else:
            self.shortest_paths = self.network.dijkstraArray(srcIndex)
        t2 = time.time()
        return t2 - t1
