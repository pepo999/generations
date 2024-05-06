import sys
import os
import random
import time
from classes import Zork, Animate
# from classes import TIME

TIME = 0
world_size_x = 170 # 160
world_size_y = 40
population_size = 100
max_gen = 0

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
    global max_gen

    world_grid = world(world_size_x, world_size_y)
    population = []

    # Initialize population
    for i in range(population_size):
        position = [random.randint(0, world_size_x - 2), random.randint(0, world_size_y - 2)]
        generation = 1
        # hostility = random.randint(1, 3)
        if i < population_size // 3:
            hostility = 3
        # elif i < counts[0] + counts[1]:
            # hostility = 2
        else:
            hostility = 1

        repr_count = 0
        energy = random.randint(1000, 1500)
        distance = random.randint(1, hostility * 5 + 20) + 20
        rest = 100

        zork = Zork(position, generation, hostility, repr_count, energy, distance, rest) 
        population.append(zork)

    animator = Animate(world_grid)

    run = True
    
    while run:
        if len(population) == 1:
            os.system,('cls')
            sys.stdout.flush()
            print(f"""\n\nmaximum generation reached: {max_gen}
time reached: {TIME}

the survivor:
hostility level:{population[0].hostility}
times reproduced:{population[0].repr_count}
generation:{population[0].generation}
seeing distance:{population[0].distance}""")
            sys.exit(0)
        if len(population) == 0 or len(population) >= 500:
            os.system('cls')
            print(f"\n\nmaximum generation reached: {max_gen}\n\ntime reahced: {TIME}" + "\n" * 30)
            sys.exit(0)

        
        for zork in population:
            if zork.generation > max_gen:
                max_gen = zork.generation
            zork.energy -= 1
            if zork.hostility == 3:
                zork.energy -= 1
            if zork.energy <= 0 or zork.repr_count >= 5:
                zork.die(population)

            snu = [z.position for z in population if z.hostility == zork.hostility and z.position != zork.position and zork.rest <= 0 and z.rest <= 0] 
            eatable = [z.position for z in population if z.hostility < zork.hostility]
            positions = snu + eatable

            avoid = [z.position for z in population if zork.rest > 0 or z.rest > 0]
            if zork.hostility == 1:
                avoid = [z.position for z in population if z.hostility > zork.hostility or (zork.rest > 0 and z.rest > 0)]


            r_x, r_y = zork.perceive(population, distance=zork.distance, start_position=zork.position, positions=positions, avoid=avoid)
            # r_x, r_y = zork.perceive(population, distance=zork.distance, start_position=zork.position)
            # r_x, r_y = None, None
            # if zork.hostility == 3:
                # r_x, r_y = zork.perceive(population, distance=zork.distance, start_position=zork.position)

            r_x, r_y = zork.perceive(population, distance=zork.distance, start_position=zork.position, positions=positions, avoid=avoid, xy=zork.position)

            if r_x is not None or r_y is not None:
                zork.move(population, r_x=r_x, r_y=r_y)
            if r_x is None and r_y is None and bool(random.randint(0,1)):
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
            world_grid[y][x] = f"{color}{zork.generation}\033[0m"

        animator.print_world(population, TIME)

        TIME += 1
        # time.sleep(0.1)
        # time.sleep(0.5)

if __name__ == "__main__":
    main()


