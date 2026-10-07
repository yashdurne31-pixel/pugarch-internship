def find_common_elements(first, second):
    common = []

    for value in first:
        if value in second and value not in common:
            common.append(value)

    return common


first = [1, 2, 3, 4]
second = [3, 4, 5, 6]

result = find_common_elements(first, second)

print("Array 1:", first)
print("Array 2:", second)
print("Common Elements:", result)