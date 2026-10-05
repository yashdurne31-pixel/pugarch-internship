// Exercise 6: Remove Duplicates

function removeDuplicates(numbers) {

    let uniqueNumbers = [];

    for (let number of numbers) {

        if (!uniqueNumbers.includes(number)) {
            uniqueNumbers.push(number);
        }
    }

    return uniqueNumbers;
}

let numbers = [1, 2, 2, 3, 4, 4, 5];

let result = removeDuplicates(numbers);

console.log("Original Array:", numbers);
console.log("Without Duplicates:", result);