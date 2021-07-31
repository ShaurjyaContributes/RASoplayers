from person import Person
from config import ENEMY_CONFIG, GRID_CONFIG


class Enemy(Person):
    '''Characteristics of an enemy'''

    def __init__(self, name="Enemy", height=None, width=None, speed=None, x=None, y=None):
        '''Contructor for enemy objects'''
        if name is None:
            name = "Enemy"
        if height is None:
            height = 1 * ENEMY_CONFIG['SIZE']
        if width is None:
            width = 1 * ENEMY_CONFIG['SIZE']
        if speed is None:
            speed = 1
        super(Enemy, self).__init__(name, height, width, speed)
        if x is not None and y is not None:
            self.pos['x'] = x
            self.pos['y'] = y
        else:
            self.pos['x'] = 0
            self.pos['y'] = GRID_CONFIG['HEIGHT'] - 1
        self.lives = 1
        self.damage = 1
        self.left_lim = self.pos['x']
        self.right_lim = self.pos['x'] + 25
        self.direction = 0

    def createMe(self, scene=None, code=GRID_CONFIG['CODE']['ENEMY']):
        '''Create the board'''
        super(Enemy, self).createMe(scene=scene, code=code)

    def reverse_direction(self):
        '''Change the direction of enemy'''
        self.direction = (self.direction + 1) % 2

    def move(self, action=None, scene=None):
        '''Function to handle movement of the person'''
        try:

            if self.pos['x'] == self.left_lim or self.pos['x'] == self.right_lim:
                self.reverse_direction()

            action = ENEMY_CONFIG['DIRECTIONS'][self.direction]

            if scene is None:
                raise AttributeError
            elif self.pos['x'] <= scene.window_left and action == 'LEFT':
                raise IndexError
            elif self.pos['x'] == (GRID_CONFIG['ACTUAL_WIDTH']-ENEMY_CONFIG['SIZE']-1) and action == 'RIGHT':
                raise IndexError
            elif self.pos['x'] == self.left_lim and action == 'LEFT':
                return IndexError
            elif self.pos['x'] == self.right_lim and action == 'RIGHT':
                return IndexError
            else:
                if action == 'LEFT':
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'] - (1 * self.speed), 'y': self.pos['y']}):
                        if scene._grid[scene.actual_height - 1][self.pos['x'] - (1 * self.speed)] != GRID_CONFIG['CODE']['BLANK']:
                            self.pos['x'] = self.pos['x'] - (1 * self.speed)
                        else:
                            self.reverse_direction()
                    else:
                        self.reverse_direction()
                elif action == 'RIGHT':
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'] + (1 * self.speed), 'y': self.pos['y']}):
                        if scene._grid[scene.actual_height - 1][self.pos['x'] + (1 * self.speed)] != GRID_CONFIG['CODE']['BLANK']:
                            self.pos['x'] = self.pos['x'] + (1 * self.speed)
                        else:
                            self.reverse_direction()
                    else:
                        self.reverse_direction()
                else:
                    pass
        except(IndexError, AttributeError):
            return
