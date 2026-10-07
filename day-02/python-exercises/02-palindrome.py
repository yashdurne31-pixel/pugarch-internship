def is_palindrome(text):
    return text == text[::-1]


text = "madam"

result = is_palindrome(text)

print("Original Word:", text)
print("Is Palindrome:", result)