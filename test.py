"""
First make the virtual enviornment, just a grid with a bunch of cells
"""

import numpy as np

WIDTH = 100
HEIGHT = 100

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
    (-1,-1),
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
class Cell:
    
    def __init__(self, row, column):
        self._row = row
        self._col = column
        self._occupant = None
        
    def set_occupant(self, new_occupant):
        if self._occupant is not None:
            return
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

def near_survive_func(cell, target, low_bound, high_bound):
    count = 0
    for direction in MOVEMENTS + DIAGONALS:
        new_x = cell[1] + direction[1]
        new_y = cell[0] + direction[0]
        if not (0 <= new_x <= WIDTH -1) or not (0 <= new_y <= HEIGHT - 1):
            continue
        if grid[new_y][new_x].get_occupant.get_color() == target:
            count += 1
    if low_bound <= count <= highbound:
        return 1
    return False
