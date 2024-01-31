import keyboard
import os
import random
COLS = 20 # X
ROWS = 20# Y
EMPTY = '.'
PLAYER = '1'
ANTHILL = '2'
ANT = '3'
ANTHILLS_MIN = 2
ANTHILL_MAX = 4
ANTS_PER_ANTHILL_MIN = 4
ANTS_PER_ANTHILL_MAX = 8
PLAYER_Y = random.randint(1, ROWS -1 )
PLAYER_X = random.randint(1, COLS-1 )
STEP_COUNTER = 0
anthill_ants_amount = 0
totalants = 0

class Field:
    def __init__(self) -> None:
        self.ESCAPED_ANTS = 0
        self.KILLED_ANTS = 0
        self.rows = ROWS
        self.cols = COLS
        self.cells = [
            [Cell(y, x) for x in range(self.cols)] for y in range(self.rows)
        ]
        self.player = Player(Field, PLAYER_Y, PLAYER_X)
        self.anthills = []
        self.ants = []
        
        
    def draw(self) -> None:
        for row in self.cells:
            for cell in row:
                if self.player is not None and cell.y == self.player.y and cell.x == self.player.x:
                    print(PLAYER, end=' ')
                elif any(cell.y == anthill.y and cell.x == anthill.x for anthill in self.anthills):
                    print(ANTHILL, end=' ')
                elif any(cell.y == ant.y and cell.x == ant.x for ant in self.ants):
                    print(ANT, end=' ')
                else:
                    print(cell, end=' ')
            print()

    def get_empty_cells(self) -> list:
        empty_cells = [
            cell for row in self.cells for cell in row
            if cell.x != self.player.x
            and cell.y != self.player.y
            and not any(cell.y == anthill.y
            and cell.x == anthill.x for anthill in self.anthills)
        ]
        return empty_cells

    def get_neighbours(self, y, x):
        neighbours_coords = []
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if row == 0 and col == 0:
                    continue
                neighbours_coords.append(
                    (y + row, x + col)
                    )
        return neighbours_coords

    def spawn_anthills(self, num_anthills: int) -> None:
        for i in range(num_anthills):
            empty_cells = self.get_empty_cells()
            random.shuffle(empty_cells)
            if i < len(empty_cells):
                anthill = Anthill(empty_cells[i].y, empty_cells[i].x)
                self.anthills.append(anthill)
                empty_cells[i].content = anthill

    def spawn_ants(self) -> None:
        for anthill in self.anthills:
            if not anthill.ants_counter:
                continue
            neighbours_coords = self.get_neighbours(
                anthill.y,
                anthill.x
                )
            if not neighbours_coords:
                continue
            for y, x in neighbours_coords:
                if y < 0 or y > self.rows - 1:
                    continue
                if x < 0 or x > self.cols - 1:
                    continue
                if self.cells[y][x].content:
                    continue
                ant = Ant(y, x)
                self.cells[y][x].content = ant
                self.ants.append(ant)
                anthill.ants_counter -= 1
                print("содан муравей в:", ant.x,ant,y)
                break

    def is_on_field(self, y: int, x: int) -> bool:
        return (y > -1 and y < ROWS) and (x > -1 and x < COLS)
                                                                 
    def move_ants(self):
        for ant in self.ants:
            neighbours_coords = self.get_neighbours(ant.y, ant.x)
            random.shuffle(neighbours_coords)
            if not neighbours_coords:
                continue
            for y, x in neighbours_coords:
                if not self.is_on_field(y, x):
                    self.ants.remove(ant)
                    self.cells[ant.y][ant.x].content = None
                    self.ESCAPED_ANTS += 1
                    break
                if field.player.x == x and field.player.y == y:
                    self.ants.remove(ant)
                    self.cells[ant.y][ant.x].content = None
                    self.KILLED_ANTS += 1                    
                new_cell = self.cells[y][x]
                if new_cell.content:
                    continue
                self.cells[ant.y][ant.x].content = None
                new_cell.content = ant      
                ant.y = y
                ant.x = x
                if ANTS_PER_ANTHILL_MAX * ANTHILL_MAX == self.ESCAPED_ANTS:
                    pass
    
    def field_ant_counter(self):
        global fieldantscounter
        global anthill_ants_amount
        global totalants
        fieldantscounter = len(self.ants)
        for anthill in self.anthills:
            anthill_ants_amount += anthill.ants_counter
        totalants = anthill_ants_amount + fieldantscounter
        return(totalants)


class Cell:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.image = EMPTY

    def draw(self):
        if self.content:
            print(self.content.image)
        else:
            print(self.image)

    def __str__(self) -> str:
        return self.image


class Player:
    def __init__(self, field, y, x) -> None:
        self.y = y
        self.x = x
        self.field = field
        self.field.player = self
        self.image = PLAYER

    def __str__(self) -> str:
        return self.image


class Anthill:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = ANTHILL
        self.ants_counter = random.randint(ANTS_PER_ANTHILL_MIN,ANTS_PER_ANTHILL_MAX)


class Ant:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.image = ANT

    def __str__(self):
        return self.image


class Game:
    def __init__(self, field) -> None:
        self.field = field
        self.game = True
        self.run()

    def run(self):
        global tempX
        global tempY
        global STEP_COUNTER
        self.field.spawn_anthills(random.randint(ANTHILLS_MIN, ANTHILL_MAX))
        self.total_ants = self.field.field_ant_counter()
        print(VFX_frame * COLS,)
        print(VFX_frame2 * VFX_choto , "Ловкий муравьед", )
        print(VFX_frame * COLS,)
        print("""
            муравьед(игрок) - 1
            муравейник - 2
            муравей - 3
              """)
        print("""
ваша цель: съесть как можно больше муравьев
пока они не сбежали с поля""", )
        print(VFX_frame * COLS, )
        print("нажмите любую кнопку для начала игры")
        print(VFX_frame * COLS )
        while self.game:
            key = keyboard.read_event() 
            tempX = self.field.player.x
            tempY = self.field.player.y
            
            def checkcollisions():
                if not isinstance(self.field.cells[tempY][tempX].content, Anthill):
                    self.field.player.x, self.field.player.y = tempX, tempY
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'right' and self.field.player.x < COLS - 1:
                    tempX += 1
                    STEP_COUNTER += 1
                    checkcollisions()
                if key.name == 'left' and self.field.player.x:
                    tempX -= 1
                    STEP_COUNTER += 1
                    checkcollisions()
                if key.name == 'up' and self.field.player.y:
                    tempY -= 1
                    STEP_COUNTER += 1
                    checkcollisions()
                if key.name == 'down' and self.field.player.y < ROWS - 1:
                    tempY += 1
                    STEP_COUNTER += 1
                    checkcollisions()
                self.field.move_ants()
                if key.name == 'esc':
                    break
                
            self.field.spawn_ants()
            self.field.field_ant_counter()
            print('')
            os.system('cls')
            print(VFX_frame * COLS )
            print(VFX_frame2 * VFX_choto , "GAME")
            print(VFX_frame * COLS )
            self.field.draw()
            print(VFX_frame * COLS )
            print("текущий ход:", STEP_COUNTER)
            print("осталось муравьев:", fieldantscounter)
            print(VFX_frame * COLS )
            if fieldantscounter == 0:
                break
        os.system('cls') 
        print(VFX_frame * COLS )
        print(VFX_frame2 * VFX_choto , "конец игры")
        print(VFX_frame * COLS )
        print("сделано ходов:", STEP_COUNTER)
        print("количество сбежавших муравьев:",self.field.ESCAPED_ANTS)
        print("количество съеденных муравьев:", self.field.KILLED_ANTS)
        print(VFX_frame * COLS )
        
VFX_frame = "=="            
VFX_frame2 = " "
VFX_choto = COLS - 3
field = Field()
player = Player(field, PLAYER_Y, PLAYER_X)
Game(field)
