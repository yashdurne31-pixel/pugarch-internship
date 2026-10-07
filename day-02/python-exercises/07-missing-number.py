def find_missing_number(numbers):
    n = len(numbers) + 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(numbers)

    return expected_sum - actual_sum


numbers = [1, 2, 3, 5]

result = find_missing_number(numbers)

print("Numbers:", numbers)
print("Missing Number:", result)