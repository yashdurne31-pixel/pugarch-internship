// Exercise 9: First Non-Repeating Character

function firstNonRepeating(str) {

    let frequency = {};

    for (let char of str) {
        frequency[char] = (frequency[char] || 0) + 1;
    }

    for (let char of str) {

        if (frequency[char] === 1) {
            return char;
        }
    }

    return null;
}

let input = "swiss";

let result = firstNonRepeating(input);

console.log("String:", input);
console.log("First Non-Repeating Character:", result);