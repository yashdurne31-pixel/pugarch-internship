// Exercise 7: Find Missing Number

function findMissingNumber(numbers) {

    let n = numbers.length + 1;

    let expectedSum = (n * (n + 1)) / 2;

    let actualSum = 0;

    for (let number of numbers) {
        actualSum += number;
    }

    return expectedSum - actualSum;
}

let numbers = [1, 2, 3, 5];

let result = findMissingNumber(numbers);

console.log("Numbers:", numbers);
console.log("Missing Number:", result);