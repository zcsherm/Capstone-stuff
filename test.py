"""
First make the virtual enviornment, just a grid with a bunch of cells
"""

import random

WIDTH = 100
HEIGHT = 100
QUANT = 150

MOVEMENTS = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]

DIAGONALS = [
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]
DIRECTIONS = ['n',
             's',
             'e',
             'w']

SURVIVAL_RULES: {'near': near_survive_func,
                'away': away_suvive_func,
                'kill': kill_survive_func}

REPRODUCE_RULE: {'near': near_reproduce_func,
                'away' : away_reproduce_func,
                'kill': kill_reproduce_func}

COLORS = ['red', 'blue', 'green']

COLOR_ATTR = { 'red': [['near', 'red', 2, 4], ['near', 'red', 3, 4]],
              'blue': [['near', 'red', 0, 1], ['near', 'red', 0, 0]],
              'green': [['kill', 'red', 0, 7], ['near', 'red', 2, 7]]
}
class Cell:
    
    def __init__(self, row, column):
        self._row = row
        self._col = column
        self._occupant = None
        
    def set_occupant(self, new_occupant):
        if self._occupant is not None and new_occupant is not None:
            return False
        self._occupant = new_occupant

    def get_occupant(self):
        return self._occupant
    
    def get_coordinates(self):
        return self._row, self._col
        
class Grid:
    def __init__(self):
        grid = []
        for i in range(HEIGHT, 0, -1):
            row = []
            for q in range(WIDTH):
                row.append(Cell(i, q))
            grid.append(row)
        self._grid = grid

    def new_game(self,  number_of_lives = QUANT):
        for i in range(QUANT):
            while True:
                new_y = random.randint(0, HEIGHT-1)
                new_x = random.randint(0, WIDTH-1)
                if self._grid[new_y][new_x].get_occupant() is None:
                    color = random.choice(COLORS)
                    self._grid[new_y][new_x].set_occupant(Life(color, self, (new_y, new_x)))

    def next_turn(self):
        for row in self._grid:
            for cell in row:
                if cell.get_occupant() is not None:
                    life = cell.get_occupant
                    life.next_gen()

    def run_simulation(self):
        while True:
            next = input('Advance?')
            self.next_turn()
            self.print_grid()

    def print_grid(self):
        for row in self._grid:
            printable = []
            for cell in row:
                occupant = cell.get_occupant()
                if occupant is None:
                    printable.append(' ')
                elif occupant.get_color() == 'red':
                    printable.append('r')
                elif occupant.get_color() == 'blue':
                    printable.append('b')
                elif occupant.get_color() == 'green':
                    printable.append('g')
                else:
                    printable.append('?')
            print(printable)
class Life:
    def __init__(self, color, grid, cell):
        self._color = color
        self._grid = grid
        self._cell = cell
        self._fitness_attributes = COLOR_ATTR[color]
        self._fitness_func = self._fitness_attributes[0][0]

    def check_survival(self):
        return self._fitness_func(*self._fitness_attributes[0])

    def check_reproduce(self):
        return self._fitness_func(*self._fitness_attrributes[1])

    def reproduce(self):
        for direction in random.shuffle(MOVEMENTS + DIAGONALS):
            new_x = self.cell[1] + direction[1]
            new_y = self.cell[0] + direction[0]
            if not (0 <= new_x <= WIDTH -1) or not (0 <= new_y <= HEIGHT - 1):
                continue
            if self.grid[new_y][new_x].get_occupant is None:
                self.grid[new_y][new_x].set_occupant(Life(self._color, self._grid, (new_y, new_x)))
                break

    def die(self):
        self.grid[self.cell[0][self.[1]].set_occupant(None) 

    def survive_func(self, type, target, min, max):
        count = 0
        for direction in MOVEMENTS + DIAGONALS:
            new_x = self.cell[1] + direction[1]
            new_y = self.cell[0] + direction[0]
            if not (0 <= new_x <= WIDTH -1) or not (0 <= new_y <= HEIGHT - 1):
                continue
            if self.grid[new_y][new_x].get_occupant.get_color() == target:
                count += 1
        if min <= count <= max:
            return 1
        return 0

    def next_gen(self):
        if self.check_survival == 1:
            if self.check_reproduce == 1:
                self.reproduce()
        else:
            self.die()

    def get_color(self):
        return self._color




"""

Determining fitness (reproduction using simple rules:
Types:
Next to x y's, could be a range
Not next to x y's
Have killed x y's
"""


class FitnessAction:
    def __init__(self, type, target, surv_quantity_min=0, surv_quantity_max=99, repr_quantity_min=0, repr_quantity_max=99):
        self._type = type
        self._target = target
        self._surv_quantity_min = surv_quantity_min
        self._surv_quantity_max = surv_quantity_max
        self._repr_quantity_min = repr_quantity_min
        self._repr_quantity_max = repr_quantity_max

    def set_survive_function(self):
        self._survive_function = SURVIVAL_RULES[self._type](target, self._quantity_min, self._quantity_max)

    def set_reproduce_function(self):
        self._reproduce_function = SURVIVAL_RULES[self._type](self._target, self._quantity_min, self._quantity_max)

    def get_survival(self, cell):
        """
        :param cell: The cell space the life occupies (ie (22,14))
        """
        self._survive_function(cell, self._target, self._quantity_min, self._quantity_max)


