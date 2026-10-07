class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def front(self):
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0


queue = Queue()

queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)

print("Queue:", queue.items)
print("Front Element:", queue.front())
print("Removed:", queue.dequeue())
print("Queue After Dequeue:", queue.items)