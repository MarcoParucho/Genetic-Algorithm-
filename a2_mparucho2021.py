"""
    Author: Marco Parucho
    Date: 06/14/2023
    Description: Create a solution of the salesmen problem using genetic algorithms
"""
import random
import math

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
        city_current = trip[i]
        city_next = trip[(i+1) % len(trip)]
        distance += distance_between(city_current, city_next)
    
    return distance

def distance_between(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def tsp_genetic_algorithm(cities, population_size, num_generations):
    population = initialize_population(population_size, cities)
    
    for _ in range(num_generations):
        fitness_scores = [trip_distance(individual) for individual in population]
        parents = selection(population, fitness_scores)
        offspring = select_parents(parents)
        mutate(offspring)
        replace_population(population, offspring)
    
    best = min(population, key=trip_distance)
    
    return best

def selection(population, fitness_scores):
    choices_amount = 2
    parents = []
    
    while len(parents) < len(population):
        choices = random.choices(population, k=choices_amount, weights=fitness_scores)
        parents.extend(choices)
    
    return parents

def select_parents(parents):
    offspring = []

    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i+1]

        child1, child2 = crossover(parent1, parent2)
        offspring.extend([child1, child2])
    
    return offspring

#this function is responsible for performing the cross over.
#it works similar to how a human is made in the sense that half of the DNA is taken from the father/mother and united together to make one child. 
#This is perfomed by slicing the point of paren1 and parent2  and uniting them with the "+" symbol.
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

#this function is responsible for mutating each offspring with a rate of my chosing this checks to see if there are any better solutions
def mutate(offspring):
    rate = 0.02
    for individual in offspring:
        if random.random() < rate:
            individual_list = list(individual)
            random_index = random.randint(0, len(individual_list) - 1)
            individual_list[random_index] = tuple(1 - coord for coord in individual_list[random_index])
            individual = tuple(individual_list)

#populating with new offspring
def replace_population(population, offspring):
    population[:len(offspring)] = offspring
    return population

#this function will display the routes and total distance of each run
def run_trip():
    cities = [( 25.7617,-80.1918), (34.0522,-118.2437), (40.7608,-111.8910), (40.6782,-73.9442), (32.7765,-79.9311)] #Miami, Los Angeles, Salt Lake City, Brooklyn, Charleston
    population_size = 100
    generations = 50

    for i in range(5):
        best_route = tsp_genetic_algorithm(cities, population_size, generations)
        total_distance = trip_distance(best_route)
        print("Test #", i+1, ": Best Route:", best_route, "Total Distance:", total_distance)

run_trip()