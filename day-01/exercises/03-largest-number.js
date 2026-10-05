// ==========================================
// Exercise 3: Find Largest Number
// ==========================================

function findLargest(numbers) {
    let largest = numbers[0];

    for (let number of numbers) {
        if (number > largest) {
            largest = number;
        }
    }

    return largest;
}

let numbers = [10, 25, 7, 50, 15];

let result = findLargest(numbers);

console.log("Numbers:", numbers);
console.log("Largest Number:", result);