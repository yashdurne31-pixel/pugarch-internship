// Exercise 12: Stack Implementation

class Stack {

    constructor() {
        this.items = [];
    }

    push(item) {
        this.items.push(item);
    }

    pop() {
        return this.items.pop();
    }

    peek() {
        return this.items[this.items.length - 1];
    }

    isEmpty() {
        return this.items.length === 0;
    }
}

let stack = new Stack();

stack.push(10);
stack.push(20);
stack.push(30);

console.log("Stack:", stack.items);
console.log("Top Element:", stack.peek());

console.log("Removed:", stack.pop());

console.log("Stack After Pop:", stack.items);