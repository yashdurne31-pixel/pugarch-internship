// Exercise 1: Reverse a String

function reverseString(str) {
    return str.split("").reverse().join("");
}

let input = "hello";

let result = reverseString(input);

console.log("Original String:", input);
console.log("Reversed String:", result);