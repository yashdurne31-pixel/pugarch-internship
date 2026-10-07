def find_second_largest(numbers):
    largest = float("-inf")
    second_largest = float("-inf")

    for number in numbers:
        if number > largest:
            second_largest = largest
            largest = number
        elif number > second_largest and number != largest:
            second_largest = number

    return second_largest


numbers = [10, 50, 30, 20, 40]

result = find_second_largest(numbers)

print("Numbers:", numbers)
print("Second Largest Number:", result)