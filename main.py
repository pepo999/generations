import sys
import os
import random
import time
from classes import Zork, Animate
# from classes import TIME

TIME = 0
world_size_x = 20 # 160
world_size_y = 20
population_size = 2

colors = {
    1: "\033[32m",  # Green
    2: "\033[33m",  # Yellow
    3: "\033[31m",  # Red
}

def world(size_x, size_y):
    return [[' ' for _ in range(size_x)] for _ in range(size_y)]


def main():
    global TIME
    global world_size_x
    global world_size_y
    global population_size

    world_grid = world(world_size_x, world_size_y)
    population = []

    # Initialize population
    for _ in range(population_size):
        position = [random.randint(0, world_size_x - 2), random.randint(0, world_size_y - 2)]
        speed = random.randint(1, 3)
        rotation = random.randint(0, 360)
        hostility = random.randint(1, 3)
        metabolism = random.randint(1, 5)
        energy = random.randint(1000, 1500)
        size = random.randint(1, 5)
        rest = 100

        zork = Zork(position, speed, rotation, hostility, metabolism, energy, size, rest) 
        population.append(zork)

    animator = Animate(world_grid)
    
    while True:
        if len(population) == 0 or len(population) >= 500:
            sys.exit(0)
        for zork in population:
            zork.energy -= 1
            if zork.hostility == 3:
                zork.energy -= 1
            if zork.energy <= 0:
                zork.die(population)
            r_x, r_y = zork.perceive(population, distance=None, start_position=zork.position)
            # if bool(random.randint(0,1)):
            if r_x is not None and r_y is not None:
                zork.move(population, r_x=r_x, r_y=r_y)
            if r_x is None and r_y is None:
                zork.move(population)
            if zork.rest > 0:
                zork.rest -= 1

        # Clear world grid
        for y in range(world_size_y):
            for x in range(world_size_x):
                world_grid[y][x] = ' '

        # Update world state
        for zork in population:
            x, y = zork.position
            color = colors[zork.hostility]
            world_grid[y][x] = f"{color}O\033[0m"

        animator.print_world(population, TIME)

        TIME += 1
        time.sleep(0.05)
        # time.sleep(0.5)

if __name__ == "__main__":
    main()


