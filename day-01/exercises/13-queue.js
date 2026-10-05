// Exercise 13: Queue Implementation

class Queue {

    constructor() {
        this.items = [];
    }

    enqueue(item) {
        this.items.push(item);
    }

    dequeue() {
        return this.items.shift();
    }

    front() {
        return this.items[0];
    }

    isEmpty() {
        return this.items.length === 0;
    }
}

let queue = new Queue();

queue.enqueue(10);
queue.enqueue(20);
queue.enqueue(30);

console.log("Queue:", queue.items);
console.log("Front Element:", queue.front());

console.log("Removed:", queue.dequeue());

console.log("Queue After Dequeue:", queue.items);