def bubble_sort(numbers):
    result = numbers.copy()

    for i in range(len(result)):
        for j in range(len(result) - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


numbers = [5, 2, 8, 1, 3]

result = bubble_sort(numbers)

print("Original Array:", numbers)
print("Sorted Array:", result)
