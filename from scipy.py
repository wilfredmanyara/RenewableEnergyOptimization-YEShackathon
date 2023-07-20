from scipy.optimize import linprog
import numpy as np

def optimize_renewable_energy(solar_capacity, wind_capacity, consumers):
    num_consumers = len(consumers)
    num_variables = 2 + num_consumers  # Two variables for solar and wind, plus one for each consumer demand

    # Objective function coefficients (negative because we want to minimize energy generation cost)
    c = [-1 * solar_capacity, -1 * wind_capacity] + [0] * num_consumers

    # Coefficients matrix for the constraint inequalities
    A_ub = [[1, 0] + [0] * num_consumers,  # Solar capacity constraint
            [0, 1] + [0] * num_consumers,  # Wind capacity constraint
            [-1, 0] + [0] * num_consumers,  # Solar energy cannot be negative
            [0, -1] + [0] * num_consumers]  # Wind energy cannot be negative

    # Right-hand side of constraint inequalities
    b_ub = [solar_capacity, wind_capacity, 0, 0]

    # Coefficients matrix for the constraint equalities (energy demand must be met for each consumer)
    A_eq = []
    b_eq = []
    for consumer in consumers:
        energy_demand = consumer['demand']
        coefficients = [0] * (2 + num_consumers)
        coefficients[2 + consumers.index(consumer)] = 1  # Consumer's demand variable
        A_eq.append(coefficients)
        b_eq.append(energy_demand)

    # Bounds for solar and wind energy generation (0 to capacity)
    bounds = [(0, solar_capacity), (0, wind_capacity)] + [(0, None)] * num_consumers

    # Solve linear programming problem
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    if result.success:
        solar_energy_allocated, wind_energy_allocated = result.x[:2]
        energy_surplus = solar_capacity - solar_energy_allocated + wind_capacity - wind_energy_allocated

        print(f"Optimal solar energy allocated: {solar_energy_allocated} MW")
        print(f"Optimal wind energy allocated: {wind_energy_allocated} MW")

        total_cost = -result.fun  # The minimized energy cost (negative of the objective function value)
        print(f"Total energy cost: {total_cost}")

        for consumer, energy_demand in zip(consumers, b_eq):
            energy_allocated = result.x[2 + consumers.index(consumer)]
            print(f"Energy allocated to {consumer['name']}: {energy_allocated} MW")

        if energy_surplus > 0:
            print(f"Energy surplus: {energy_surplus} MW")
        else:
            print("Energy demand perfectly met.")
    else:
        print("Optimization failed.")

# Example usage:
solar_capacity = 100  # MW
wind_capacity = 150   # MW

consumers = [
    {'name': 'Consumer A', 'demand': 50},
    {'name': 'Consumer B', 'demand': 30},
    {'name': 'Consumer C', 'demand': 70}
]

optimize_renewable_energy(solar_capacity, wind_capacity, consumers)
