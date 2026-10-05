// Exercise 14: Maximum Subarray Sum

function maximumSubarraySum(numbers) {

    let currentSum = numbers[0];
    let maximumSum = numbers[0];

    for (let i = 1; i < numbers.length; i++) {

        currentSum = Math.max(
            numbers[i],
            currentSum + numbers[i]
        );

        maximumSum = Math.max(
            maximumSum,
            currentSum
        );
    }

    return maximumSum;
}

let numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4];

let result = maximumSubarraySum(numbers);

console.log("Numbers:", numbers);
console.log("Maximum Subarray Sum:", result);