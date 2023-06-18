"""
    Author: Marco Parucho
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
        individual = cities.copy()
        random.shuffle(individual) #will avoid cities from appearing again
        population.append(individual)
    
    return population



#This function finds the total distance of the trip, it uses the distance_between function which is in charge of find the distance from city to city
def trip_distance(trip):
    distance = 0
    for i in range(len(trip)):
        city_current = trip[i][1]
        city_next = trip[(i+1) % len(trip)][1]
        distance += distance_between(city_current, city_next)
    
    return distance

def distance_between(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

#Genetic Algorithms function. calling this function will help the user find the best route for n cities by using their latitude and longitude.
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
    #converting tuple to list
    parent1_list = list(parent1)
    parent2_list = list(parent2)
    #slicing
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return tuple(child1), tuple(child2)

#this function is responsible for mutating each offspring with a rate of my chosing this checks to see if there are any better solutions
def mutate(offspring):
    rate = 0.01
    for i in range(len(offspring)):
        individual = offspring[i]
        if random.random() < rate:
            individual_list = list(individual)
            random_index = random.randint(0, len(individual_list) - 1)
            coord = individual_list[random_index][1]  # Getting the coordinates
            mutated_coord = tuple(1 - c for c in coord)  # Mutating the coordinates
            individual_list[random_index] = (individual_list[random_index][0], mutated_coord)  # Combining the mutated coordinates with the original city name
            offspring[i] = tuple(individual_list)


#populating with new offspring
def replace_population(population, offspring):
    population[:len(offspring)] = offspring
    return population

#this function will display the routes and total distance of each run
def run_trip():
    cities = [] 
    population_size = 100
    generations = 50

    print("\t    WELCOME\n\t----------------\n")
    print("This program will help you find the best possible route between n number of cities by using their coordinates\n")



    #Allowing the user to enter city info to avoid mistakes when entering data into code
    numb_cities = int(input("Enter the number of cities: "))
    for i in range(numb_cities):
        name = input(f"Enter the name of city #{i+1}: ")
        latitude = float(input(f"Enter the latitude of {name}: "))
        longitude = float(input(f"Enter the longitude of {name}: "))
        city = (latitude, longitude)
        #adding into the list
        cities.append((name, city))
   
        os.system('cls')

    for i in range(5):
        best_route = tsp_genetic_algorithm(cities, population_size, generations)
        total_distance = trip_distance(best_route)
        
        city_names = [city[0] for city in best_route]
        city_coordinates = [city[1] for city in best_route]
        
        print("Test #", i+1, ": Best Route:", city_names, "Total Distance:", total_distance)

    
    input("\nPress any key to close...")

run_trip()