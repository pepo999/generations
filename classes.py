import random
import sys
import os
import time

# TIME = 0
world_size_x = 20 # 160
world_size_y = 20

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
    def __init__(self, position, speed, rotation, hostility, metabolism, energy, size, rest):
        self.position = position
        self.speed = speed
        self.rotation = rotation
        self.hostility = hostility
        self.metabolism = metabolism
        self.energy = energy + size
        self.size = size
        self.rest = rest

    def eat(self, target):
        self.energy += target.energy

    def move(self, population, r_x= None, r_y=None):
        global TIME
        global world_size_x
        global world_size_y
        
        # if  self.speed != 0 and TIME % self.speed == 0:
        if self.speed != 0:
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
                            self.reproduce(population)
                            self.rest = random.randint(100,1000)
                            zork.rest = random.randint(100,1000)
                            if self.hostility == 1:
                                self.reproduce(population)
                                self.reproduce(population)
                                self.reproduce(population)
                            if self.hostility == 2:
                                self.reproduce(population)
                            # if zork.hostility == 3:
                                # self.rest = self.rest * 2
                                # zork.rest = zork.rest * 2
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

    def reproduce(self, population):
        # Create a new Zork with mixed values but same hostility level
        new_speed = self.speed
        new_rotation = self.rotation
        new_metabolism = self.metabolism
        new_energy = random.randint(1000, 1500)
        new_size = self.size
        new_zork = Zork([self.position[0], self.position[1]], new_speed, new_rotation, self.hostility, new_metabolism, new_energy, new_size, 200)
        population.append(new_zork)



    def perceive(self, population, start_position, distance=None, x=None, y=None):
        global movements

        snu = [z.position for z in population if z.hostility == self.hostility and z.position != self.position and self.rest <= 0 and z.rest <= 0] 
        eatable = [z.position for z in population if z.hostility < self.hostility]
        positions = snu + eatable

        avoid = []
        # if self.hostility == 1:
            # avoid = [z.position for z in population if z.hostility > self.hostility]


        if distance is None:
            distance = self.hostility * 5 + 20
        if x is None:
            x = self.position[0]
        if y is None:
            y = self.position[1]

        xy = [x , y]

        l = list(movements.items())
        random.shuffle(l)
        # sys.stdout.flush()
        # print(l)


        for m in l:
            
            summed = [x + y for x, y in zip(xy, m[1])]
            if not 0 <= summed[0] < world_size_x - 1 or not 0 <= summed[1] < world_size_y - 1:
                # continue
                return None, None
            # os.system('cls')
            # sys.stdout.flush()
            # print(xy, 'going to', summed)
            # time.sleep(2)
            if summed in positions:
                os.system('cls')
                print(start_position, 'FOUND :', summed)
                sys.stdout.flush()
                time.sleep(5)
                return m[1][0], m[1][1]
            if summed in avoid:
                return m[1][0] * -1, m[1][1] * -1
            else:
                distance -= 1
                # return self.perceive(population, start_position, distance, x, y)
                return self.perceive(population, start_position, distance, summed[0], summed[1])
        return None, None




    def perceive_old(self, population, start_position, distance=None, x=None, y=None, r_x=None, r_y=None, seen=[]):

        # sys.stdout.flush()
        # print(f"d:{distance} x:{x} y:{y} r_x:{r_x} r_y:{r_y} seen:{len(seen)}")
        # time.sleep(0.5)


        if distance is None:
            distance = self.hostility * 5 + 20
        if x is None:
            x = self.position[0]
        if y is None:
            y = self.position[1]


        if start_position not in seen:
            seen.append(start_position)

        if [x, y] not in seen:
            seen.append([x, y])

        if distance <= 0:
            return None, None

        # sys.stdout.flush()
        # print(f"d:{distance} x:{x} y:{y} r_x:{r_x} r_y:{r_y} seen:{len(seen)}")
        # time.sleep(0.5)

        snu = [z.position for z in population if z.hostility == self.hostility and z.position != self.position and self.rest <= 0 and z.rest <= 0] 
        eatable = [z.position for z in population if z.hostility < self.hostility]
        positions = snu + eatable

        avoid = []
        if self.hostility == 1:
            avoid = [z.position for z in population if z.hostility > self.hostility]

        # if r_x and r_y:
            # sys.stdout.flush()
            # os.system('cls')
            # print(f'Found a mate/FOOOOOD!\n me:{self.position}, host:{self.hostility} rest:{self.rest} dir:[{r_x},{r_y}]')
            # time.sleep(2)
            # return r_x, r_y

        if [x+1, y] in positions and [x+1, y] != start_position: 
            r_x = 1
            r_y = 0
        if [x+1, y] in avoid:
            r_x = -1
            r_y = 0

        if [x, y+1] in positions and [x, y+1] != start_position:
            r_x = 0
            r_y = 1
        if [x, y+1] in avoid:
            r_x = 0
            r_y = -1

        if [x-1, y] in positions and [x-1, y] != start_position:
            r_x = -1
            r_y = 0
        if [x-1, y] in avoid:
            r_x = 1
            r_y = 0

        if [x, y-1] in positions and [x, y-1] != start_position:
            r_x = 0
            r_y = -1
        if [x, y-1] in avoid:
            r_x = 0
            r_y = 1

        if [x+1, y+1] in positions and [x+1, y+1] != start_position:
            r_x = 1
            r_y = 1
        if [x+1, y+1] in avoid:
            r_x = -1
            r_y = -1

        if [x-1, y-1] in positions and [x-1, y-1] != start_position:
            r_x = -1
            r_y = -1
        if [x-1, y-1] in avoid:
            r_x = 1
            r_y = 1

        if [x+1, y-1] in positions and [x+1, y-1] != start_position:
            r_x = 1
            r_y = -1
        if [x+1, y-1] in avoid:
            r_x = -1
            r_y = 1

        if [x-1, y+1] in positions and [x-1, y+1] != start_position:
            r_x = -1
            r_y = 1
        if [x-1, y+1] in avoid:
            r_x = 1
            r_y = -1

        if r_x and r_y:
            sys.stdout.flush()
            os.system('cls')
            print(f'Found a mate/FOOOOOD!\n me:{self.position}, host:{self.hostility} rest:{self.rest} dir:[{r_x},{r_y}]')
            time.sleep(2)
            return r_x, r_y



        distance -= 1
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

        if [x, y] in seen or 0 <= x < 40 or 0 <= y < 40:
            return None, None


        return self.perceive(population, start_position, distance, x, y, r_x, r_y, seen=seen)


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


