// Exercise 11: Find Common Elements

function findCommonElements(arr1, arr2) {

    let common = [];

    for (let value of arr1) {

        if (arr2.includes(value) && !common.includes(value)) {
            common.push(value);
        }
    }

    return common;
}

let arr1 = [1, 2, 3, 4];
let arr2 = [3, 4, 5, 6];

let result = findCommonElements(arr1, arr2);

console.log("Array 1:", arr1);
console.log("Array 2:", arr2);
console.log("Common Elements:", result);