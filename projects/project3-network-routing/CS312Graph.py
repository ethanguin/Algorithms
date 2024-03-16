#!/usr/bin/python3

class PQHeap:
    def __init__(self):
        self.heap = []
        self.index_map = {}

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    @staticmethod
    def leftChild(i):
        return 2 * i + 1

    @staticmethod
    def rightChild(i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.index_map[self.heap[i][1]] = i
        self.index_map[self.heap[j][1]] = j

    def bubbleUp(self, i):
        while i > 0 and self.heap[self.parent(i)][0] > self.heap[i][0]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def bubbleDown(self, i):
        min_index = i
        left = self.leftChild(i)
        right = self.rightChild(i)
        n = len(self.heap)

        if left < n and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left

        if right < n and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right

        if i != min_index:
            self.swap(i, min_index)
            self.bubbleDown(min_index)

    def insert(self, value, priority):
        self.heap.append((priority, value))
        index = len(self.heap) - 1
        self.index_map[value] = index
        self.bubbleUp(index)

    def decreaseKey(self, value, new_priority):
        if value in self.index_map:
            index = self.index_map[value]
            old_priority, value = self.heap[index]
            self.heap[index] = (new_priority, value)
            if new_priority < old_priority:
                self.bubbleUp(index)
            else:
                self.bubbleDown(index)

    def deleteMin(self):
        if self.isEmpty():
            return None

        min_value = self.heap[0][1]
        del self.index_map[min_value]

        if len(self.heap) > 1:
            last_element = self.heap.pop()
            self.heap[0] = last_element
            self.index_map[last_element[1]] = 0
            self.bubbleDown(0)
        else:
            self.heap.pop()

        return min_value

    def isEmpty(self):
        return len(self.heap) == 0


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

    def dijkstra(self, start_node_id, useHeap):
        # Initialize distances array with infinity for all nodes and previous array with null
        num_nodes = len(self.nodes)
        distances = [float('inf')] * num_nodes
        if not useHeap:
            pq = PQArray(num_nodes, float('inf'))
        else:
            pq = PQHeap()
            for node in self.nodes:
                pq.insert(node.node_id, float('inf'))

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
