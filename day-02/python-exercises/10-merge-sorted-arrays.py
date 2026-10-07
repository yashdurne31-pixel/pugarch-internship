def merge_sorted_arrays(first, second):
    result = []
    i = 0
    j = 0

    while i < len(first) and j < len(second):
        if first[i] < second[j]:
            result.append(first[i])
            i += 1
        else:
            result.append(second[j])
            j += 1

    while i < len(first):
        result.append(first[i])
        i += 1

    while j < len(second):
        result.append(second[j])
        j += 1

    return result


first = [1, 3, 5]
second = [2, 4, 6]

result = merge_sorted_arrays(first, second)

print("Array 1:", first)
print("Array 2:", second)
print("Merged Array:", result)