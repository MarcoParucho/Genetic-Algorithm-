"""
    Author:Marco Parucho
    Date: 06/14/2023
    Description: Create a solution of the salesmen problem using genetic algorithms
"""
import random
import math
import os

#this function provides individual so we can start testing the best solutions possible.
def initialize_population(population_size, cities):
    population = []

    for _ in range(population_size):
        individual = random.sample(cities, len(cities))
        population.append(individual)

    return population

#This function finds the total distance of the trip, it uses the distance_between function which is in charge of find the distance from city to city
def trip_distance(trip):
    distance = 0
    for i in range(len(trip)):
        city_current = trip[i][1]
        city_next = trip[(i + 1) % len(trip)][1]
        distance += distance_between(city_current, city_next)

    return distance

def distance_between(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

#this function makes sure that cities are only visited once.
def repair_solution(solution):
    visited_cities = set()
    repaired_solution = []

    for city in solution:
        city_name = city[0]
        if city_name not in visited_cities:
            repaired_solution.append(city)
            visited_cities.add(city_name)

    return repaired_solution

def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    parents = random.choices(population, weights=probabilities, k=len(population))

    return parents

def select_parents(parents):
    offspring = []

    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]

        child1, child2 = crossover(parent1, parent2)
        offspring.extend([repair_solution(child1), repair_solution(child2)])

    return offspring

#this function is responsible for performing the cross over.
#it works similar to how a human is made in the sense that half of the DNA is taken from the father/mother and united together to make one child. 
#This is perfomed by slicing the point of paren1 and parent2  and uniting them with the "+" symbol.
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point]
    child2 = parent2[:point]

    for gene in parent2:
        if gene not in child1:
            child1.append(gene)

    for gene in parent1:
        if gene not in child2:
            child2.append(gene)

    return child1, child2

#this function is responsible for mutating each offspring with a rate of my chosing this checks to see if there are any better solutions
def mutate(offspring):
    rate = 0.03
    for individual in offspring:
        if random.random() < rate:
            individual_list = list(individual)
            population_size = len(individual_list)
            if population_size > 1:
                random_indices = random.sample(range(population_size), 2)
                individual_list[random_indices[0]], individual_list[random_indices[1]] = individual_list[random_indices[1]], individual_list[random_indices[0]]
            individual = tuple(individual_list)

def replace_population(population, offspring):
    population[:len(offspring)] = offspring
    return population

def tsp_genetic_algorithm(cities, population_size, num_generations):
    population = initialize_population(population_size, cities)

    for _ in range(num_generations):
        fitness_scores = [1 / trip_distance(individual) for individual in population]
        parents = selection(population, fitness_scores)
        offspring = select_parents(parents)
        mutate(offspring)
        replace_population(population, offspring)

    best = min(population, key=trip_distance)

    return best
#this function will display the routes and total distance of each run
def run_trip():
    cities = []
    population_size = 100
    num_generations = 50

    print("     WELCOME - TSP solver")
    print("------------------------------\n")
    #Allowing the user to enter city info to avoid mistakes when entering data into code
    numb_cities = int(input("Enter the number of cities: "))
    for i in range(numb_cities):
        name = input(f"Enter the name of city {i+1}: ")
        latitude = float(input(f"Enter the latitude of city {name}: "))
        longitude = float(input(f"Enter the longitude of city {name}: "))
        city = (name, (latitude, longitude))
        cities.append(city)

        os.system("cls")

    for i in range(5):
        best_route = tsp_genetic_algorithm(cities, population_size, num_generations)
        best_route.append(best_route[0])  # Append the first city to complete the loop
        total_distance = trip_distance(best_route)

        city_names = [city[0] for city in best_route]
        city_coordinates = [city[1] for city in best_route]

        print("Test #", i+1, ": Best Route:", city_names)
       
    input("\nEnter any key to close the program... ")


run_trip()
