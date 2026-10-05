// Exercise 8: Find Duplicate Number

function findDuplicate(numbers) {

    let seen = new Set();

    for (let number of numbers) {

        if (seen.has(number)) {
            return number;
        }

        seen.add(number);
    }

    return null;
}

let numbers = [1, 2, 3, 4, 3];

let result = findDuplicate(numbers);

console.log("Numbers:", numbers);
console.log("Duplicate Number:", result);