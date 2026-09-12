import numpy as np

# Transportation cost matrix
cost = np.array([
    [8,  6, 10, 9],
    [9, 12, 13, 7],
    [14, 9, 16, 5]
], dtype=float)

# VAM allocation
allocation = np.array([
    [0, 10, 25, 0],
    [45, 0, 5, 0],
    [0, 10, 0, 30]
], dtype=float)


# MODI Method

m, n = allocation.shape

# u values for rows
u = [None] * m

# v values for columns
v = [None] * n

# Start with u1 = 0
u[0] = 0


# Find u and v

changed = True

while changed:

    changed = False

    for i in range(m):

        for j in range(n):

            # Only occupied cells are used
            if allocation[i][j] > 0:

                if u[i] is not None and v[j] is None:

                    v[j] = cost[i][j] - u[i]
                    changed = True

                elif u[i] is None and v[j] is not None:

                    u[i] = cost[i][j] - v[j]
                    changed = True


print("u values:", u)
print("v values:", v)


# Calculate opportunity costs

delta = np.zeros((m, n))

for i in range(m):

    for j in range(n):

        # Only calculate for unoccupied cells
        if allocation[i][j] == 0:

            delta[i][j] = cost[i][j] - (u[i] + v[j])


print("\nOpportunity cost (Delta) matrix:")
print(delta)


# Check optimality

negative = False

for i in range(m):

    for j in range(n):

        if allocation[i][j] == 0 and delta[i][j] < 0:
            negative = True


if negative:

    print("\nSolution is not optimal.")
    print("An improvement is required.")

else:

    print("\nSolution is optimal.")
    print("No improvement is required.")


# Calculate total transportation cost

total_cost = np.sum(allocation * cost)

print("\nOptimal allocation:")
print(allocation)

print("\nMinimum transportation cost =", total_cost)
