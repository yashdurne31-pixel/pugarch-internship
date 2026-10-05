// ==========================================
// Exercise 2: Check Palindrome
// ==========================================

function isPalindrome(str) {
    let reversed = str.split("").reverse().join("");

    return str === reversed;
}

let word = "madam";

let result = isPalindrome(word);

console.log("Original Word:", word);
console.log("Is Palindrome:", result);