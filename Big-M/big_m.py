import numpy as np

# Objective function coefficients
c = [6, -7, -4]

# Constraint coefficients
A = [
    [2, 5, -1],
    [-1, 1, 2],
    [3, 2, 2]
]

# Right-hand side
b = [18, 14, 26]

# Constraint types
signs = ['<=', '>=', '=']

# Decision variables
variables = ['x1', 'x2', 'x3']


# Add slack, surplus and artificial variables

extra_vars = []
artificial_vars = []

for sign in signs:

    if sign == '<=':
        extra_vars.append(f's{len(extra_vars) + 1}')

    elif sign == '>=':
        extra_vars.append(f's{len(extra_vars) + 1}')
        artificial_vars.append(f'a{len(artificial_vars) + 1}')

    elif sign == '=':
        artificial_vars.append(f'a{len(artificial_vars) + 1}')


all_vars = variables + extra_vars + artificial_vars

print("Variables:", all_vars)


# Convert constraints to standard form

standard_A = []

for i in range(len(A)):

    row = [0] * len(all_vars)

    # Decision variables
    for j in range(len(A[i])):
        row[j] = A[i][j]

    if signs[i] == '<=':

        # Slack variable
        row[all_vars.index(extra_vars[0])] = 1

    elif signs[i] == '>=':

        # Surplus variable
        row[all_vars.index(extra_vars[1])] = -1

        # Artificial variable
        row[all_vars.index(artificial_vars[0])] = 1

    elif signs[i] == '=':

        # Artificial variable
        row[all_vars.index(artificial_vars[1])] = 1

    standard_A.append(row)


# Big-M coefficients

M = 1000000

cj = [6, -7, -4, 0, 0, -M, -M]

# Initial basic variables
basis = ['s1', 'a1', 'a2']

# cB values of basic variables
cB = [0, -M, -M]


# Convert to NumPy arrays
A = np.array(standard_A, dtype=float)
b = np.array(b, dtype=float)
cB = np.array(cB, dtype=float)
cj = np.array(cj, dtype=float)


# Simplex iterations

iteration = 0

while True:

    iteration += 1

    # Calculate Zj
    Zj = np.dot(cB, A)

    # Calculate Cj - Zj
    Cj_Zj = cj - Zj



    # Print tableau


    print("\n" + "=" * 70)
    print("Iteration", iteration)
    print("=" * 70)

    print("Basis\tcB", end="\t")

    for var in all_vars:
        print(var, end="\t")

    print("b")

    for i in range(len(A)):

        print(basis[i], end="\t")
        print(round(cB[i], 2), end="\t")

        for value in A[i]:
            print(round(value, 2), end="\t")

        print(round(b[i], 2))

    print("Zj\t\t", end="")

    for value in Zj:
        print(round(value, 2), end="\t")

    print()

    print("Cj-Zj\t\t", end="")

    for value in Cj_Zj:
        print(round(value, 2), end="\t")

    print()



    # Check optimality


    if np.max(Cj_Zj) <= 0:

        print("\nOptimal solution reached.")
        break



    # Find entering variable


    entering_col = np.argmax(Cj_Zj)

    print("\nEntering variable:",
          all_vars[entering_col])



    # Ratio test


    ratios = []

    for i in range(len(A)):

        if A[i][entering_col] > 0:

            ratios.append(b[i] / A[i][entering_col])

        else:

            ratios.append(float('inf'))


    leaving_row = np.argmin(ratios)

    print("Ratios:", ratios)

    print("Leaving variable:",
          basis[leaving_row])



    # Pivot operation


    pivot = A[leaving_row][entering_col]

    # Make pivot element 1
    A[leaving_row] = A[leaving_row] / pivot
    b[leaving_row] = b[leaving_row] / pivot


    # Make all other entries in pivot column 0
    for i in range(len(A)):

        if i == leaving_row:
            continue

        factor = A[i][entering_col]

        A[i] = A[i] - factor * A[leaving_row]
        b[i] = b[i] - factor * b[leaving_row]


    # Update basis
    basis[leaving_row] = all_vars[entering_col]
    cB[leaving_row] = cj[entering_col]


# Final answer

print("\n" + "=" * 70)
print("FINAL ANSWER")
print("=" * 70)

solution = np.zeros(len(variables))

for i in range(len(basis)):

    if basis[i] in variables:

        j = variables.index(basis[i])
        solution[j] = b[i]


print("\nOptimal solution:")

for i in range(len(variables)):

    print(
        variables[i],
        "=",
        round(solution[i], 3)
    )


# Calculate objective value
Z = np.dot(c, solution)

print("\nOptimal objective value =", round(Z, 3))
