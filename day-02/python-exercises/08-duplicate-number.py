def find_duplicate(numbers):
    seen = set()

    for number in numbers:
        if number in seen:
            return number

        seen.add(number)

    return None


numbers = [1, 2, 3, 4, 3]

result = find_duplicate(numbers)

print("Numbers:", numbers)
print("Duplicate Number:", result)