// Exercise 10: Merge Sorted Arrays

function mergeSortedArrays(arr1, arr2) {

    let result = [];

    let i = 0;
    let j = 0;

    while (i < arr1.length && j < arr2.length) {

        if (arr1[i] < arr2[j]) {
            result.push(arr1[i]);
            i++;
        } else {
            result.push(arr2[j]);
            j++;
        }
    }

    while (i < arr1.length) {
        result.push(arr1[i]);
        i++;
    }

    while (j < arr2.length) {
        result.push(arr2[j]);
        j++;
    }

    return result;
}

let arr1 = [1, 3, 5];
let arr2 = [2, 4, 6];

let result = mergeSortedArrays(arr1, arr2);

console.log("Array 1:", arr1);
console.log("Array 2:", arr2);
console.log("Merged Array:", result);