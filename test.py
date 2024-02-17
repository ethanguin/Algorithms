class PQArray:
    def __init__(self):
        self.queue = []

    def insert(self, item, key):
        self.queue.append((item, key))

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


def main():
    pq = [float('inf')] * 8
    print(pq)
    print("")
    pq[4] = 0
    print(pq)


main()
