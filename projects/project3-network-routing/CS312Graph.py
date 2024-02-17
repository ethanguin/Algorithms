#!/usr/bin/python3

class PQArray:
    def __init__(self, max_size, fill_item):
        self.queue = [fill_item] * max_size
        self.length = max_size
        if fill_item is None:
            self.length = 0

    def insert(self, index, key):
        self.queue[index] = key
        self.length += 1

    def decreaseKey(self, index, key):
        self.queue[index] = key

    def deleteMin(self):
        if self.isEmpty():
            return None
        min_index = 0
        for i in range(len(self.queue)):
            if self.queue[min_index] is None:
                min_index = i
            if self.queue[i] is None:
                continue
            else:
                if self.queue[i] < self.queue[min_index]:
                    min_index = i

        self.length -= 1
        self.queue[min_index] = None
        return min_index

    def isEmpty(self):
        return self.length == 0


class CS312GraphEdge:
    def __init__(self, src_node, dest_node, edge_length):
        self.src = src_node
        self.dest = dest_node
        self.length = edge_length

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(src={} dest={} length={})'.format(self.src, self.dest, self.length)


class CS312GraphNode:
    def __init__(self, node_id, node_loc):
        self.node_id = node_id
        self.loc = node_loc
        self.neighbors = []  # node_neighbors

    def addEdge(self, neighborNode, weight):
        self.neighbors.append(CS312GraphEdge(self, neighborNode, weight))

    def __str__(self):
        neighbors = [edge.dest.node_id for edge in self.neighbors]
        return 'Node(id:{},neighbors:{})'.format(self.node_id, neighbors)


class CS312Graph:
    def __init__(self, nodeList, edgeList):
        self.nodes = []
        for i in range(len(nodeList)):
            self.nodes.append(CS312GraphNode(i, nodeList[i]))

        for i in range(len(nodeList)):
            neighbors = edgeList[i]
            for n in neighbors:
                self.nodes[i].addEdge(self.nodes[n[0]], n[1])

    def __str__(self):
        s = []
        for n in self.nodes:
            s.append(n.neighbors)
        return str(s)

    def getNodes(self):
        return self.nodes

    def dijkstraArray(self, start_node_id):
        # Initialize distances array with infinity for all nodes and previous array with null
        num_nodes = len(self.nodes)
        distances = [float('inf')] * num_nodes
        pq = PQArray(num_nodes, float('inf'))
        prev = [None] * num_nodes
        distances[start_node_id] = 0
        pq.decreaseKey(start_node_id, 0)

        while not pq.isEmpty():
            # Pop the node with the smallest distance from the priority queue
            current_node_id = pq.deleteMin()

            # Explore neighbors of the current node
            for edge in self.nodes[current_node_id].neighbors:
                neighbor_id = edge.dest.node_id
                new_distance = distances[current_node_id] + edge.length

                # If a shorter path is found, update distance and previous node
                if new_distance < distances[neighbor_id]:
                    distances[neighbor_id] = new_distance
                    prev[neighbor_id] = edge
                    pq.decreaseKey(neighbor_id, new_distance)

        # Construct the shortest paths from start node to each node
        shortest_paths = []
        for node_id, distance in enumerate(distances):
            path = []
            if distance is float('inf'):
                shortest_paths.append(path)
                continue

            current_node_id = node_id
            while current_node_id is not None:
                if prev[current_node_id] is not None:  # Check if valid previous node
                    path.append(prev[current_node_id])
                    current_node_id = prev[current_node_id].src.node_id
                else:
                    break
            shortest_paths.append(path)

        return shortest_paths
