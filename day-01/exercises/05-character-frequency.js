// Exercise 5: Character Frequency

function characterFrequency(str) {

    let frequency = {};

    for (let char of str) {

        if (frequency[char]) {
            frequency[char]++;
        } else {
            frequency[char] = 1;
        }
    }

    return frequency;
}

let input = "hello";

let result = characterFrequency(input);

console.log("String:", input);
console.log("Character Frequency:", result);