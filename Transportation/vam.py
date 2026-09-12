import numpy as np

# Transportation cost matrix
cost = np.array([
    [8,  6, 10, 9],
    [9, 12, 13, 7],
    [14, 9, 16, 5]
], dtype=float)

# Supply and demand
supply = np.array([35, 50, 40], dtype=float)
demand = np.array([45, 20, 30, 30], dtype=float)

# Allocation matrix
allocation = np.zeros((3, 4))

# Active rows and columns
rows = [True, True, True]
cols = [True, True, True, True]

# VAM

while np.sum(supply) > 0:

    row_penalty = [-1] * 3
    col_penalty = [-1] * 4

    # Calculate row penalties
    for i in range(3):

        if not rows[i]:
            continue

        values = []

        for j in range(4):
            if cols[j]:
                values.append(cost[i][j])

        values.sort()

        if len(values) >= 2:
            row_penalty[i] = values[1] - values[0]
        else:
            row_penalty[i] = values[0]


    # Calculate column penalties
    for j in range(4):

        if not cols[j]:
            continue

        values = []

        for i in range(3):
            if rows[i]:
                values.append(cost[i][j])

        values.sort()

        if len(values) >= 2:
            col_penalty[j] = values[1] - values[0]
        else:
            col_penalty[j] = values[0]


    # Find largest penalty
    max_row_penalty = max(row_penalty)
    max_col_penalty = max(col_penalty)

    if max_row_penalty >= max_col_penalty:

        i = np.argmax(row_penalty)

        # Find cheapest cell in this row
        j = -1
        minimum = float('inf')

        for k in range(4):
            if cols[k] and cost[i][k] < minimum:
                minimum = cost[i][k]
                j = k

    else:

        j = np.argmax(col_penalty)

        # Find cheapest cell in this column
        i = -1
        minimum = float('inf')

        for k in range(3):
            if rows[k] and cost[k][j] < minimum:
                minimum = cost[k][j]
                i = k


    # Allocate as much as possible
    amount = min(supply[i], demand[j])

    allocation[i][j] = amount

    supply[i] -= amount
    demand[j] -= amount


    # Remove exhausted row/column
    if supply[i] == 0:
        rows[i] = False

    if demand[j] == 0:
        cols[j] = False


print("\nVAM Allocation:")
print(allocation)

# Calculate transportation cost
total_cost = np.sum(allocation * cost)

print("\nTotal transportation cost =", total_cost)
