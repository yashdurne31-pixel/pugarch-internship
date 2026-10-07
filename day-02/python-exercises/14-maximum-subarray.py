def maximum_subarray_sum(numbers):
    current_sum = numbers[0]
    maximum_sum = numbers[0]

    for number in numbers[1:]:
        current_sum = max(number, current_sum + number)
        maximum_sum = max(maximum_sum, current_sum)

    return maximum_sum


numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

result = maximum_subarray_sum(numbers)

print("Numbers:", numbers)
print("Maximum Subarray Sum:", result)