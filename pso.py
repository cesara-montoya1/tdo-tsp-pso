import random
from util import path_cost


class Particle:
    # Inicializar partícula
    def __init__(self, route, cost=None):
        self.route = route  # Ruta de la partícula
        self.pbest = route  # Mejor ruta conocida por la partícula (pbest)
        # Si no se le especifica un costo actual, se calcula el costo de la ruta
        self.current_cost = cost if cost else self.path_cost()
        # Mejor costo conocido (pbest_cost)
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = []  # Velocidad de la partícula

    # Reiniciar velocidad
    def clear_velocity(self):
        self.velocity.clear()

    # Actualizar el costo y el pbest
    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()  # Calcular el costo actual de la ruta
        # Si el costo actual es mejor que el pbest, se actualiza el pbest
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    # Calcular el costo de la ruta
    def path_cost(self):
        return path_cost(self.route)


class PSO:
    # Inicializar el PSO
    def __init__(self, iterations, population_size,
                 gbest_probability=1.0, pbest_probability=1.0, cities=None):
        self.cities = cities  # Lista de ciudades
        self.gbest = None  # Mejor ruta global (gbest)
        self.gcost_iter = []  # Historial de costos globales
        self.iterations = iterations  # Número de iteraciones
        self.population_size = population_size  # Tamaño de la población
        self.particles = []  # Lista de partículas
        self.gbest_probability = gbest_probability  # Probabilidad de usar gbest
        self.pbest_probability = pbest_probability  # Probabilidad de usar pbest

        # Inicializar con una solución factible cada partícula
        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    # Generar una ruta aleatoria
    def random_route(self):
        return random.sample(self.cities, len(self.cities))

    # Generar la población inicial (soluciones aleatorias excepto una que es voraz)
    def initial_population(self):
        random_population = [self.random_route()
                             for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]

    # Generar una ruta voraz
    def greedy_route(self, start_index):
        unvisited = self.cities[:]  # Lista de ciudades no visitadas
        del unvisited[start_index]
        # Ruta inicial con la ciudad de inicio
        route = [self.cities[start_index]]
        while len(unvisited):
            # Encontrar la ciudad más cercana no visitada
            index, nearest_city = min(
                enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]  # Eliminar la ciudad visitada de la lista
        return route

    # Ejecutar el PSO
    def run(self):
        # Inicializa el gbest como la partícula con el mejor puntaje (pbest)
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print(f"Initial cost is {self.gbest.pbest_cost}")

        # Realiza el ciclo hasta el número de iteraciones
        for t in range(self.iterations):
            # Actualiza el gbest como el valor mínimo de los pbest de las partículas
            self.gbest = min(self.particles, key=lambda p: p.pbest_cost)

            # Guarda el valor del gbest en una lista para mantener el historial de evolución
            self.gcost_iter.append(self.gbest.pbest_cost)

            # Ciclo para actualizar las partículas
            for particle in self.particles:
                particle.clear_velocity()  # Reiniciar la velocidad de la partícula
                temp_velocity = []  # Lista temporal de velocidad
                gbest = self.gbest.pbest[:]  # Copia del mejor global (gbest)
                # Copia de la ruta actual de la partícula
                new_route = particle.route[:]

                # Actualizar la velocidad basada en el pbest de la partícula
                for i in range(len(self.cities)):
                    if new_route[i] != particle.pbest[i]:
                        swap = (i, particle.pbest.index(
                            new_route[i]), self.pbest_probability)
                        temp_velocity.append(swap)
                        new_route[swap[0]], new_route[swap[1]
                                                      ] = new_route[swap[1]], new_route[swap[0]]

                # Actualizar la velocidad basada en el gbest
                for i in range(len(self.cities)):
                    if new_route[i] != gbest[i]:
                        swap = (i, gbest.index(
                            new_route[i]), self.gbest_probability)
                        temp_velocity.append(swap)
                        gbest[swap[0]], gbest[swap[1]
                                              ] = gbest[swap[1]], gbest[swap[0]]

                particle.velocity = temp_velocity  # Actualizar la velocidad de la partícula

                # Aplicar la velocidad a la ruta de la partícula
                for swap in temp_velocity:
                    if random.random() <= swap[2]:
                        new_route[swap[0]], new_route[swap[1]
                                                      ] = new_route[swap[1]], new_route[swap[0]]

                particle.route = new_route  # Actualizar la ruta de la partícula
                # Actualizar el costo y el pbest de la partícula
                particle.update_costs_and_pbest()
