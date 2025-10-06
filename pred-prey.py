import random


HEIGHT = 20
WIDTH = 40
CELLS = HEIGHT * WIDTH
TERRAINS = ['grass', 'dirt', 'water']
MAX_ENERGIES = {'deer':10, 'wolf':20}
ENERGIES = {'grass':10, 'deer':20}
MAX_HYDRO = {'deer':15, 'wolf':22}
SPAWN_CHANCES = {'grass': .3, 'deer':.21, 'wolf': .08}
ANIMALS = ['deer', 'wolf']
ACTIONS = ['eat','move','reproduce','nothing','drink']

class World:
    def __init__(self, height=HEIGHT, width=WIDTH):
        self._height = height
        self._width = width
        self._cells = height * width
        self._grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Cell(self, (i, j))
            self._grid.append(row)

class Cell:
    def __init__(self, grid, coords):
        self._occupant = None
        self._terrain = None

    def set_occupant(self, occupant):
        if self._occupant is None:
            self._occupant = occupant
            return True
        return False

    def set_terrain(self, terrain):
        self._terrain = terrain

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
    def __init__(self, type, cell):
        self._type = type
        self._cell = cell
        self._energy = MAX_ENERGIES[type]
        self._age = 0
        self._hydro = MAX_HYDRO[type]
    
    def set_genetics(self):
        """
        14 digit: 1. N_occupant 2. E_occupant 3. S_occupant 4. w_occupant
                5. N_terrain 6. E_terrain 7. S_terrain 8. W_terrain
                9. This_terrain
                10. Wolves_total 11. Deer_total 12. Energy level
                13. N_water 14 E_water 15 S_water 16 W_water 17. Water_level
                18. Empties Total 19. grasses_tot, 20. Dirt tot 21. water_tot, 
        """
        self._this_dirt_weight = random.random(-10,10)
        self._this_grass_weight = random.random(-10,10)
        self._NESW_weights = [random.random(-10,10) for i in range(4)]
        self._eat_weights = [random.random(-10,10) for i in range(21)]
        self._move_weights = [random.random(-10,10) for i in range(21)]
        self._repro_weights = [random.random(-10,10) for i in range(21)]
        self._nothing_weights = [random.random(-10,10) for i in range(21)]
        self._drink_weights = [random.random(-10,10) for i in range(21)]
        self._n_weight = [random.random(-10,10) for i in range(21)]
        self._e_weight = [random.random(-10,10) for i in range(21)]
        self._s_weight = [random.random(-10,10) for i in range(21)]
        self._w_weight = [random.random(-10,10) for i in range(21)]
        self._genome = [self._eat_weights, self._move_weights, self._repro_weights, self._nothing_weights, self._drink_weights]
    
    def check_living(self):
        if self._energy <= 0:
            return False
        return True

    def eat(self, target):
        self._energy = max(self._energy + ENERGIES[target], MAX_ENERGIES[self._type])

    def decision(self):
        """
        Gather info about surrounding cells and own info
        """
        this_terrain = self._cell.get_terrain()
        n_occupant, n_terrain = self.cell.get_n_details()
        e_occupant, e_terrain = self.cell.get_e_details()
        s_occupant, s_terrain = self.cell.get_s_details()
        w_occupant, w_terrain = self.cell.get_w_details()
        occupants = self.cell.get_neighbors()
        terrains = self.celll.get_terrains()
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
            elif terrain == 'grass':
                this_cell = self._this_grass_weight
        e_deficit = MAX_ENERGIES[self._type] - self._energy
        w_deficit = MAX_HYDRP[self._type] - self._hydro
        results = []
        for i in range(5):
            sum = 0
            for j in range(4):
                if terrain == 'water':
                    sum += self._genome[i][j+13]
                else:
                    sum += occupants[j] * self._genome[i][j]
            for j in range(4):
                sum += terrains[j+4] * self._genome[i][j+4]
            sum += this_cell * self._genome[i][8]
            sum += wolves * self._genome[i][9]
            sum += deer * self._genome[i][10]
            sum += empties * self._genome[i][27]
            sum += e_deficit * self._genome[i][11]
            sum += w_deficit * self._genome[i][16]
            sum += grasses * self._genome[i][18]
            sum += dirts * self._genome[i][19]
            sum += waters * self._genome[i][20]
            results.append(sum)
        m = max(results)
        ind = results.index(m)
        
class Deer(Animal):
    def __init__(self, cell):
        super().__init__('deer', cell)

class Wolf(Animal, cell):
    def __init__(self, cell):
        super().__init__('wolf', cell)
