def find_largest(numbers):
    largest = numbers[0]

    for number in numbers:
        if number > largest:
            largest = number

    return largest


numbers = [10, 25, 7, 50, 15]

result = find_largest(numbers)

print("Numbers:", numbers)
print("Largest Number:", result)