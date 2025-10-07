import random


HEIGHT = 10
WIDTH =10
CELLS = HEIGHT * WIDTH
TERRAINS = ['grass', 'dirt', 'water']
MAX_ENERGIES = {'deer':10, 'wolf':20}
ENERGIES = {'grass':10, 'deer':20}
MAX_HYDRO = {'deer':15, 'wolf':22}
SPAWN_CHANCES = {'grass': .3, 'deer':.21, 'wolf': .08}
ANIMALS = ['deer', 'wolf']
ACTIONS = ['eat','move','reproduce','nothing','drink']
DIRECTIONS =[(1,0),(0,1),(-1,0),(0,-1)]
WATER_CHANCE = .25
DEER_POP = int(CELLS * .3)
WOLF_POP = int(CELLS * .15)

class World:
    
    def __init__(self, height=HEIGHT, width=WIDTH):
        self._height = height
        self._width = width
        self._cells = height * width
        self._grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(self, (i, j)))
            self._grid.append(row)
        self.seed_cells()
        self.print_grid()
        
    def seed_cells(self):
        for row in self._grid:
            for cell in row:
                if random.random() < WATER_CHANCE:
                    cell.set_terrain('water')
                    continue
                else:
                    cell.set_terrain('grass')
                animal_roll = random.random()
                if  animal_roll < DEER_POP/CELLS:
                    cell.set_occupant(Animal('deer', cell))
                elif animal_roll < DEER_POP/CELLS + WOLF_POP/CELLS:
                    cell.set_occupant(Animal('wolf', cell))
                    
    def progress_sim(self):
        for i in range(self._height):
            for j in range(self._width):
                occupant = self._grid[i][j].get_occupant()
                if occupant is not None:
                    if occupant.get_flag() is False:
                        choice = occupant.decision()
                        self.handle_choice(occupant, choice)

        for i in range(self._height):
            for j in range(self._width):
                occupant = self._grid[i][j].get_occupant()
                terrain = self._grid[i][j].get_terrain()
                if occupant is not None:
                    occupant.reset_flag()
                if terrain == 'dirt':
                    if random.random() < SPAWN_CHANCES['grass']:
                        self._grid[i][j].set_terrain('grass')

    def print_grid(self):
        for row in self._grid:
            print_row = []
            for cell in row:
                space = ''
                terrain = cell.get_terrain()
                animal = cell.get_occupant()
                if animal is not None:
                    animal = animal.get_type()
                if terrain == 'dirt':
                    space = 'd'
                elif terrain == 'grass':
                    space = 'g'
                elif terrain == 'water':
                    space = 'w'

                if animal == 'deer':
                    space = 'D'
                elif animal == 'wolf':
                    space = 'W'
                print_row.append(space)
            print(print_row)

    def forward_step(self):
        self.progress_sim()
        self.print_grid()

    def get_animal_at(self, x, y):
        t=self._grid[y][x].get_occupant()
        if t is not None:
            t = t.get_type()
        return t

    def get_terrain_at(self, x, y):
        t = self._grid[y][x].get_terrain()
        return t
        
    def handle_choice(self, occupant, choice):
        cell = occupant.get_cell()
        coords = cell.get_coords()
        if choice == 'nothing':
            occupant.reduce_hydro(-1)
        if choice == 'reproduce':
            for direction in DIRECTIONS:
                new_x = (direction[1] + coords[1]) % self._width
                new_y = (direction[0] + coords[0]) % self._height
                if self._grid[new_y][new_x].get_occupant() is None and self._grid[new_y][new_x].get_terrain() != 'water':
                    # Reproduce 
                    new_animal = Animal(occupant.get_type(), self._grid[new_y][new_x], occupant.output_genetics())
                    new_animal.set_flag()
                    self._grid[new_y][new_x].set_occupant(new_animal)
                    break
                    
        if choice == 'drink':
            for direction in DIRECTIONS:
                new_x = (direction[1] + coords[1]) % self._width
                new_y = (direction[0] + coords[0]) % self._height
                if self._grid[new_y][new_x].get_terrain() == 'water':
                    occupant.drink()
                    break
    
        if choice == 'eat':
            if occupant.get_type() == 'deer':
                if cell.get_terrain() == 'grass':
                    occupant.eat('grass')
                    cell.set_terrain('dirt')
                    
            else:
                for direction in DIRECTIONS:
                    new_x = (direction[1] + coords[1]) % self._width
                    new_y = (direction[0] + coords[0]) % self._height
                    if self._grid[new_y][new_x].get_occupant() is not None:
                        if self._grid[new_y][new_x].get_occupant().get_type() == 'deer':
                            occupant.eat('deer')
                            self._grid[new_y][new_x].set_occupant(None)
                        
        if choice == 'move_north':
            new_x = (coords[1]) % self._width
            new_y = (coords[0]+1) % self._height
            if self._grid[new_y][new_x].get_occupant() is None and self._grid[new_y][new_x].get_terrain() != 'water':
                occupant.set_cell(self._grid[new_y][new_x])
                self._grid[new_y][new_x].set_occupant(occupant)
            else:
                choice == 'move_east'
                
        if choice == 'move_east':
            new_x = (coords[1]+1) % self._width
            new_y = (coords[0]) % self._height
            if self._grid[new_y][new_x].get_occupant() is None and self._grid[new_y][new_x].get_terrain() != 'water':
                occupant.set_cell(self._grid[new_y][new_x])
                self._grid[new_y][new_x].set_occupant(occupant)
            else:
                choice == 'move_south'
                
        if choice == 'move_south':
            new_x = (coords[1]) % self._width
            new_y = (coords[0]-1) % self._height
            if self._grid[new_y][new_x].get_occupant() is None and self._grid[new_y][new_x].get_terrain() != 'water':
                occupant.set_cell(self._grid[new_y][new_x])
                self._grid[new_y][new_x].set_occupant(occupant)
            else:
                choice == 'move_west'
                
        if choice == 'move_west':
            new_x = (coords[1]-1) % self._width
            new_y = (coords[0]) % self._height
            if self._grid[new_y][new_x].get_occupant() is None and self._grid[new_y][new_x].get_terrain() != 'water':
                occupant.set_cell(self._grid[new_y][new_x])
                self._grid[new_y][new_x].set_occupant(occupant)

        occupant.set_flag()
        occupant.reduce_energy(1)
        if occupant.get_hydro()<=0:
            occupant.reduce_energy(1)
        else:
            occupant.reduce_hydro(1)
        if occupant.get_energy() <= 0:
            cell.occupant = None
            
class Cell:
    def __init__(self, grid, coords):
        self._occupant = None
        self._terrain = None
        self._grid = grid
        self._coords = coords

    def set_occupant(self, occupant):
        self._occupant = occupant

    def set_terrain(self, terrain):
        self._terrain = terrain

    def get_occupant(self):
        return self._occupant

    def get_terrain(self):
        return self._terrain

    def get_coords(self):
        return self._coords

    def get_neighbors_animals(self):
        neighbors = []
        for direction in DIRECTIONS:
            new_x = (direction[1] + self._coords[1]) % WIDTH
            new_y = (direction[0] + self._coords[0]) % HEIGHT
            a=self._grid.get_animal_at(new_x, new_y)
            neighbors.append(a)
        return neighbors
        
    def get_neighbors_terrains(self):
        neighbors = []
        for direction in DIRECTIONS:
            new_x = (direction[1] + self._coords[1]) % WIDTH
            new_y = (direction[0] + self._coords[0]) % HEIGHT
            a=self._grid.get_terrain_at(new_x, new_y)
            neighbors.append(a)
        return neighbors
        
class Terrain:
    def __init__(self, type):
        self._type = type

class Water(Terrain):
    def __init__(self):
        super().__init__('water')

class Ocean:
    def __init__(self):
        pass

class Grass(Terrain):
    def __init__(self):
        super().__init__('grass')

class Dirt(Terrain):
    def __init__(self):
        super().__init__('dirt')

    def regrow(self):
        roll = random.random()
        if roll <= SPAWN_CHANCES['grass']:
            return True
        return False

class Animal:
    def __init__(self, type, cell, genome=None):
        self._type = type
        self._cell = cell
        self._energy = MAX_ENERGIES[type]
        self._age = 0
        self._hydro = MAX_HYDRO[type]
        self._flag = False
        if genome is None:
            self.set_genetics()
        else:
            self._this_dirt_weight = genome[0]
            self._this_grass_weight = genome[1]
            self._NESW_weights = genome[2]
            self._eat_weights = genome[3]
            self._move_weights = genome[4]
            self._repro_weights =genome[5]
            self._nothing_weights = genome[6]
            self._drink_weights =genome[7]
            self._n_weight = genome[8]
            self._e_weight = genome[9]
            self._s_weight = genome[10]
            self._w_weight = genome[11]
            self._genome = genome[12]
    
    def set_genetics(self):
        """
        14 digit: 1. N_occupant 2. E_occupant 3. S_occupant 4. w_occupant
                5. N_terrain 6. E_terrain 7. S_terrain 8. W_terrain
                9. This_terrain
                10. Wolves_total 11. Deer_total 12. Energy level
                13. N_water 14 E_water 15 S_water 16 W_water 17. Water_level
                18. Empties Total 19. grasses_tot, 20. Dirt tot 21. water_tot, 
        """
        self._this_dirt_weight = random.uniform(-10,10)
        self._this_grass_weight = random.uniform(-10,10)
        self._NESW_weights = [random.uniform(-10,10) for i in range(4)]
        self._eat_weights = [random.uniform(-10,10) for i in range(21)]
        self._move_weights = [random.uniform(-10,10) for i in range(21)]
        self._repro_weights = [random.uniform(-10,10) for i in range(21)]
        self._nothing_weights = [random.uniform(-10,10) for i in range(21)]
        self._drink_weights = [random.uniform(-10,10) for i in range(21)]
        self._n_weight = [random.uniform(-10,10) for i in range(21)]
        self._e_weight = [random.uniform(-10,10) for i in range(21)]
        self._s_weight = [random.uniform(-10,10) for i in range(21)]
        self._w_weight = [random.uniform(-10,10) for i in range(21)]
        self._genome = [self._eat_weights, self._move_weights, self._repro_weights, self._nothing_weights, self._drink_weights]

    def output_genetics(self):
        genes = [
            self._this_dirt_weight,
            self._this_grass_weight,
            self._NESW_weights,
            self._eat_weights,
            self._move_weights,
            self._repro_weights,
            self._nothing_weights,
            self._drink_weights,
            self._n_weight,
            self._e_weight,
            self._s_weight,
            self._w_weight,
            self._genome
        ]
        return genes
        
    def check_living(self):
        if self._energy <= 0:
            return False
        return True

    def eat(self, target):
        self._energy = max(self._energy + ENERGIES[target], MAX_ENERGIES[self._type])

    def drink(self):
        self._hydro = MAX_HYDRO[self._type]

    def get_energy(self):
        return self._energy

    def get_hydro(self):
        return self._hydro

    def get_age(self):
        return self._age

    def increment_age(self):
        self._age += 1

    def reduce_energy(self, amount = 1):
        self._energy -= 1

    def reduce_hydro(self, amount = 1):
        self._hydro -= 1

    def get_type(self):
        return self._type

    def get_cell(self):
        return self._cell

    def set_cell(self, cell):
        self._cell = cell

    def set_flag(self):
        self._flag = True

    def get_flag(self):
        return self._flag

    def reset_flag(self):
        self._flag = False
        
    def decision(self):
        """
        Gather info about surrounding cells and own info
        """
        this_terrain = self._cell.get_terrain()
        occupants = self._cell.get_neighbors_animals()
        terrains = self._cell.get_neighbors_terrains()
        deers = 0
        wolves = 0
        empties = 0
        dirts = 0
        waters = 0
        grasses = 0
        for occupant in occupants:
            if occupant == 'deer':
                occupant = 1
                deers += 1
            elif occupant == 'wolf':
                occupant = -1
                wolves += 1 
            else:
                occupant = 0
                empties += 1
                
        for terrain in terrains:
            if terrain == 'dirt':
                terrain = '-1'
                dirts += 1
            elif terrain == 'grass':
                terrain = '1'
                grasses += 1
            else:
                waters += 1
        if this_terrain == 'dirt':
            this_cell = self._this_dirt_weight
        elif this_terrain == 'grass':
            this_cell = self._this_grass_weight
        e_deficit = MAX_ENERGIES[self._type] - self._energy
        w_deficit = MAX_HYDRO[self._type] - self._hydro
        results = []
        for i in range(5):
            sum = 0
            for j in range(4):
                a = occupants [j]
                if a == 'deer':
                    s = 1
                if a == 'wolf':
                    s = -1
                else:
                    continue
                sum += s * self._genome[i][j]
            for j in range(4):
                if terrains[j] == 'water':
                    sum += self._genome[i][j+12]
                else:
                    if terrains[j] == 'grass':
                        s = 1
                    else:
                        s = -1
                    sum += s * self._genome[i][j+4]
            sum += this_cell * self._genome[i][8]
            sum += wolves * self._genome[i][9]
            sum += deers * self._genome[i][10]
            sum += empties * self._genome[i][17]
            sum += e_deficit * self._genome[i][11]
            sum += w_deficit * self._genome[i][16]
            sum += grasses * self._genome[i][18]
            sum += dirts * self._genome[i][19]
            sum += waters * self._genome[i][20]
            results.append(sum)
        m = max(results)
        ind = results.index(m)
        decision = ACTIONS[ind]
        if decision == 'move':
            genes = [self._n_weight, self._e_weight, self._s_weight, self._w_weight]
            results = []
            for i in range(4):
                sum = 0
                for j in range(4):
                    a = occupants[j]
                    if a == 'deer':
                        s = 1
                    if a == 'wolf':
                        s = -1
                    else:
                        continue
                    sum += s * genes[i][j]
                for j in range(4):
                    if terrains[j] == 'water':
                        sum += genes[i][j+12]
                    else:
                        if terrains[j] == 'grass':
                            s = 1
                        else:
                            s = -1
                        sum += s * genes[i][j+4]
                sum += this_cell * genes[i][8]
                sum += wolves * genes[i][9]
                sum += deers * genes[i][10]
                sum += empties * genes[i][17]
                sum += e_deficit * genes[i][11]
                sum += w_deficit * genes[i][16]
                sum += grasses * genes[i][18]
                sum += dirts * genes[i][19]
                sum += waters * genes[i][20]
                results.append(sum)
            print(results)
            m = max(results)
            ind = results.index(m)
            if ind == 0:
                decision = 'move_north'
            elif ind == 1:
                decision = 'move_east'
            elif ind == 2:
                decision = 'move_south'
            else:
                decision = 'move_west'
        print(decision)
        return decision
        
class Deer(Animal):
    def __init__(self, cell):
        super().__init__('deer', cell)

class Wolf(Animal):
    def __init__(self, cell):
        super().__init__('wolf', cell)
        
world = World()
for _ in range(5):
    i = input()
    world.forward_step()
