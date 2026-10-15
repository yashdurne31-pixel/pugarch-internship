"use strict";
function firstItem(items) {
    return items[0];
}
function printResult(result) {
    if (result.success) {
        console.log("Result:", result.data);
    }
    else {
        console.error("Request failed:", result.error);
    }
}
console.log(firstItem([10, 20, 30]));
printResult({ success: true, data: "Type narrowing works" });
printResult({ success: false, error: "Example error" });
