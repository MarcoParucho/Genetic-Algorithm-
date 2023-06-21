"""
    Author:Marco Parucho
    Date: 06/14/2023
    Description: Create a solution of the salesmen problem using genetic algorithms
"""
import random
import math
import os

#quality of life improvements.... Additions made after first submission. 
#creating a function that makes sure the user only enters an integer when asked for the number of cities. 
def get_number_cities():
    while True:
        try:
            number_of_cities = int(input("Enter the number of cities: "))
            return number_of_cities
        except ValueError:
            print("Error. Please enter an integer.")

#this function will make sure the user only enter characters and not any digits when asked for a city name
def get_city_name(city_number):
    while True:
        city_name = input(f"Enter the name of the city:").strip() #removes all the spaces. For example "New York City" will now work
        if city_name.replace(" ", "").isalpha():
            return city_name 
        print("Error. Please enter a valid city name.")

#This function makes sure the user enter correct and logical data for latitude within the -90|90 degrees range
def get_latitude(city_name):
    while True:
        latitude = input(f"Enter the latitude of {city_name}: ")
        
        try: 
            latitude = float(latitude)
            if -90 <= latitude <= 90:
                return latitude
            print("Error. Please insert a latitue withing the correct range.")
        except ValueError:
            print("Error. Please enter a valid float number.")

#This functio has the same task as the get_latitude but for longitude. 180 degree range
def get_longitude(city_name):
    while True: 
        longitude = input(f"Enter the longitude of {city_name}:")
        try:
            longitude = float(longitude)
            if -180 <= longitude <= 180:
                return longitude
            print("Error. Please enter a longitude within the correct range.")
        except:
            print("Error. Please enter a valid float number.")
#this function provides individual so we can start testing the best solutions possible.
def initialize_population(population_size, cities):
    population = []

    for i in range(population_size):
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

    for i in range(num_generations):
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
    numb_cities = get_number_cities() #quality of life improvement.

    for i in range(numb_cities):
        name = get_city_name(i+1)
        latitude = get_latitude(name) #improvement 
        longitude = get_longitude(name) #improvement
        city = (name, (latitude, longitude))
        cities.append(city)

        os.system("cls")

    
    best_route = tsp_genetic_algorithm(cities, population_size, num_generations)
    best_route.append(best_route[0])  # Append the first city to complete the loop
    total_distance = trip_distance(best_route)

    city_names = [city[0] for city in best_route]
    city_coordinates = [city[1] for city in best_route]

    print("Best Route:", city_names)
    
#creating this function so the users have the option to run the program again without having to open the .py file again
def main():
    while True:
        run_trip()

        choice = input("\nRun program again? (Y/N): ")
        os.system("cls")
        if choice != "Y":
            break


main()