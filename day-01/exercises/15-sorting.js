// Exercise 15: Sorting Without Built-in Sort

function bubbleSort(numbers) {

    let arr = [...numbers];

    for (let i = 0; i < arr.length; i++) {

        for (let j = 0; j < arr.length - i - 1; j++) {

            if (arr[j] > arr[j + 1]) {

                let temp = arr[j];

                arr[j] = arr[j + 1];

                arr[j + 1] = temp;
            }
        }
    }

    return arr;
}

let numbers = [5, 2, 8, 1, 3];

let result = bubbleSort(numbers);

console.log("Original Array:", numbers);
console.log("Sorted Array:", result);