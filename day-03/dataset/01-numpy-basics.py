import numpy as np


scores = np.array([
    [80, 70, 90],
    [65, 75, 85],
    [90, 88, 92],
    [55, 60, 58]
])


print("Scores:")
print(scores)

print("\nShape:", scores.shape)
print("Dimensions:", scores.ndim)

print("\nColumn 1:", scores[:, 0])
print("Row 1:", scores[0])

print("\nOverall Average:", np.mean(scores))
print("Column Averages:", np.mean(scores, axis=0))
print("Row Averages:", np.mean(scores, axis=1))

print("\nHighest Score:", np.max(scores))
print("Lowest Score:", np.min(scores))