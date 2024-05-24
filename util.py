import math
import random
import matplotlib.pyplot as plt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def generate_coord(distance) -> int:
    # Generates a random number between 0 and distance
    return int(random.random() * distance)


def generate_cities(size) -> list[City]:
    # Create a list of City objects with random coordinates (x, y)
    return [City(x=generate_coord(1000), y=generate_coord(1000)) for _ in range(size)]


def save_map(filename, map_data):
    # Save the coordinates of the cities in a file
    with open(filename, 'w') as f:
        for city in map_data:
            f.write(f"{city.x} {city.y}\n")


def load_map(filename):
    # Load the coordinates of the cities from a file
    map_data = []
    with open(filename, 'r') as f:
        for coord in f:
            x, y = map(int, coord.split())
            map_data.append(City(x, y))
    return map_data


def path_cost(route):
    # Calculate the total distance of a route
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])


def visualize_tsp(title, cities):
    # Plot the route with each city as a dot
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)
