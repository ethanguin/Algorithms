#!/usr/bin/python3

class PQArray:
    def __init__(self):
        self.queue = []

    def insert(self, index, key):
        self.queue.append((index, key))

    def decreaseKey(self, index, key):
        self.queue[index]

    def deleteMin(self):
        if self.isEmpty():
            return None
        min_index = 0
        min_priority = self.queue[0][1]
        for i in range(1, len(self.queue)):
            if self.queue[i][1] < min_priority:
                min_priority = self.queue[i][1]
                min_index = i
        return self.queue.pop(min_index)[0]

    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False


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
        previous = [(None, None)] * num_nodes
        distances[start_node_id] = 0

        # Initialize priority queue with all the nodes and their distances
        pq = PQArray()
        for node in self.nodes:
            pq.insert(node.node_id, distances[node.node_id])

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
                    previous[neighbor_id] = (current_node_id, edge.length)
                    pq.insert(neighbor_id, new_distance)

        # Construct the shortest paths from start node to each node
        shortest_paths = {}
        for node_id, distance in enumerate(distances):
            path = []
            current_node_id = node_id
            while current_node_id is not None:
                if previous[current_node_id][0] is not None:  # Check if valid tuple
                    path.insert(0, (current_node_id, previous[current_node_id][1]))  # Include edge length
                    current_node_id = previous[current_node_id][0]
                else:
                    path.insert(0, (start_node_id, previous[current_node_id][1]))
                    break
            shortest_paths[node_id] = (distance, path)

        return shortest_paths
