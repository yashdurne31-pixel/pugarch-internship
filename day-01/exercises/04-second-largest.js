// Exercise 4: Find Second Largest Number

function findSecondLargest(numbers) {

    let largest = -Infinity;
    let secondLargest = -Infinity;

    for (let number of numbers) {

        if (number > largest) {
            secondLargest = largest;
            largest = number;
        } 
        else if (number > secondLargest && number !== largest) {
            secondLargest = number;
        }
    }

    return secondLargest;
}

let numbers = [10, 50, 30, 20, 40];

let result = findSecondLargest(numbers);

console.log("Numbers:", numbers);
console.log("Second Largest Number:", result);