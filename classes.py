import random
import sys
import os
import time

# TIME = 0
world_size_x = 170 # 160
world_size_y = 40

movements = {
        "u": (0,-1), 
        "d": (0,1),
        "l": (-1,0),
        "r": (1,0),
        "ur": (1,-1),
        "ul": (-1,-1),
        "dr": (1,1),
        "dl": (-1,1)
        }

class Zork:
    def __init__(self, position, generation, hostility, repr_count, energy, distance, rest):
        self.position = position
        self.generation = generation
        self.hostility = hostility
        self.repr_count = repr_count
        self.energy = energy
        self.distance = distance
        self.rest = rest

    def eat(self, target):
        self.energy += (target.energy // 2)

    def move(self, population, r_x= None, r_y=None):
        global TIME
        global world_size_x
        global world_size_y
        
        x = self.position[0]
        y = self.position[1]
        if r_y is None:
            r_y = random.randint(-1, 1)
        if r_x is None:
            r_x = random.randint(-1, 1)
        x += r_x
        y += r_y
        x = max(0, min(x, world_size_x - 2))
        y = max(0, min(y, world_size_y - 2))
        self.position = [x, y]
        for zork in population:
            if zork != self and zork.position == self.position:
                if zork.hostility == self.hostility:
                    if zork.rest > 0 or self.rest > 0 and self.hostility != 1:
                        pass
                    else:
                        for _ in range(4 - zork.hostility):
                            self.reproduce(population, zork)
                        self.rest = random.randint(100,1000)
                        zork.rest = random.randint(100,1000)
                elif self.hostility > zork.hostility:
                    # self.die(population)
                    # self.rest = 0
                    self.eat(zork)
                    zork.die(population)

    def die(self, population):
        if self.hostility == 2 and bool(random.randint(0, 1)):
            self.energy += 500
            return
        population.remove(self)

    def reproduce(self, population, mate):
        # Create a new Zork with mixed values but same hostility level
        self.repr_count += 1
        mate.repr_count += 1
        generation = self.generation
        if generation < mate.generation:
            generation = mate.generation
        new_generation = generation + 1
        new_repr_count = 0
        new_energy = random.randint(1000, 1500)
        new_distance = self.distance
        if new_distance < mate.distance:
            new_distance = mate.distance
        new_zork = Zork([self.position[0], self.position[1]], new_generation, self.hostility, new_repr_count, new_energy, new_distance, 300)
        population.append(new_zork)

        
    def perceive(self, population, start_position, distance, positions, avoid, xy=None):
        global movements

        if xy is None:
            xy = self.position

        l = list(movements.items())
        random.shuffle(l)

        for d in range(distance):
            for m in l:
                summed = [x + y for x, y in zip(xy, m[1])]
                # sys.stdout.flush()
                # print('summed', summed)
        
                if not 0 <= summed[0] < world_size_x - 1 or not 0 <= summed[1] < world_size_y - 1:
                    continue

                if summed in positions:
                    return m[1][0], m[1][1]

                if summed in avoid:
                    return m[1][0] * -1, m[1][1] * -1
                else:
                    distance -= 1
                    if distance <= 0:
                        # break
                        return None, None
                    # result = self.perceive(population, start_position, distance, positions, avoid, xy=[summed[0], summed[1]])
                    # if result != (None, None):
                        # return result
        return None, None



    def perceive_old(self, population, start_position, distance, positions, avoid, x=None, y=None):
        global movements

        # snu = [z.position for z in population if z.hostility == self.hostility and z.position != self.position and self.rest <= 0 and z.rest <= 0] 
        # eatable = [z.position for z in population if z.hostility < self.hostility]
        # positions = snu + eatable

        # avoid = [z.position for z in population if self.rest > 0 or z.rest > 0]
        # if self.hostility == 1:
            # avoid = [z.position for z in population if z.hostility > self.hostility or (self.rest > 0 and z.rest > 0)]


        # if distance is None:
            # distance = random.randint(1, self.hostility * 10)

        if x is None:
            x = self.position[0]

        if y is None:
            y = self.position[1]

        xy = [x, y]

        l = list(movements.items())
        random.shuffle(l)

        for m in l:
            summed = [x + y for x, y in zip(xy, m[1])]
        
            if not 0 <= summed[0] < world_size_x - 1 or not 0 <= summed[1] < world_size_y - 1:
                continue

            if summed in positions:
                return m[1][0], m[1][1]

            if summed in avoid:
                return m[1][0] * -1, m[1][1] * -1
            else:
                distance -= 1
                if distance <= 0:
                    break
                    # return None, None
                result = self.perceive(population, start_position, distance, positions, avoid, x=summed[0], y=summed[1])
                if result != (None, None):
                    return result
        return None, None

class Animate:
    def __init__(self, world):
        self.world = world

    def print_world(self, population, TIME):
        green = [zork for zork in population if zork.hostility == 1]
        yellow = [zork for zork in population if zork.hostility == 2]
        red = [zork for zork in population if zork.hostility == 3]
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        sys.stdout.flush()
        print('\033[H')
        sys.stdout.flush()
        print('\r' * len(self.world), end='')  # Move cursor to beginning of line
        print(f"Time: {TIME} - Total population: {len(population)} green:{len(green)} yellow:{len(yellow)} red:{len(red)}                \n")
        for row in self.world:
            sys.stdout.flush()
            print(''.join(row))


