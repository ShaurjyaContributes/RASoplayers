from person import Person
from config import PLAYER_CONFIG, GRID_CONFIG
import os


class Player(Person):
    '''Characteristics of a player'''

    def __init__(self, name="Mario", height=None, width=None, speed=None):
        '''Contructor for player objects'''
        if name is None:
            name = "Mario"
        if height is None:
            height = 1 * PLAYER_CONFIG['SIZE']
        if width is None:
            width = 1 * PLAYER_CONFIG['SIZE']
        if speed is None:
            speed = 1
        super(Player, self).__init__(name, height, width, speed)
        self.lives = PLAYER_CONFIG['START_LIVES']
        self.power = []
        self.coins = 0
        self.score = 0

    def reset_pos(self):
        '''Reset the position of the player to start'''
        self.pos = {'x': 0, 'y': (GRID_CONFIG['HEIGHT'] - 1)}

    def createMe(self, scene=None, code=GRID_CONFIG['CODE']['PLAYER']):
        '''Function that creates the player on the seen'''
        super(Player, self).createMe(scene=scene, code=code)

    def move(self, action=None, scene=None):
        '''Function to handle movement of the person'''
        try:
            if scene is None:
                raise AttributeError
            if self.pos['y'] < self.base and action == 'JUMP'and (scene._grid[self.pos['y']+1][self.pos['x']] != GRID_CONFIG['CODE']['OBSTACLE']):
                return
            elif self.pos['x'] <= scene.window_left and action == 'LEFT':
                raise IndexError
            elif self.pos['x'] == (GRID_CONFIG['ACTUAL_WIDTH']-PLAYER_CONFIG['SIZE']-1) and action == 'RIGHT':
                raise IndexError
            else:
                if action == 'LEFT':
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'] - (1 * self.speed), 'y': self.pos['y']}):
                        self.pos['x'] = self.pos['x'] - (1 * self.speed)
                elif action == 'RIGHT':
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'] + (1 * self.speed), 'y': self.pos['y']}):
                        if self.pos['x'] > ((scene.window_left + scene.window_right)/2):
                            scene.shift_window(player=self)
                        self.pos['x'] = self.pos['x'] + (1 * self.speed)
                elif action == 'JUMP':
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'], 'y': self.pos['y'] - 1}):
                        os.system("aplay -q Sounds/jump.wav &")
                        self.jump_from = self.base - self.pos['y']
                        self.gravity = False
                        self.pos['y'] = self.pos['y'] - 1
                else:
                    pass

                if (self.pos['y'] < self.base) and self.gravity and (scene._grid[self.pos['y']+1][self.pos['x']] != GRID_CONFIG['CODE']['OBSTACLE']):
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'], 'y': self.pos['y'] + 1}):
                        self.pos['y'] = self.pos['y'] + 1

                if (not self.gravity) and ((self.base - self.jump_from - self.max_jump) != self.pos['y']) and action != 'JUMP'and (scene._grid[self.pos['y']-(1*self.height)][self.pos['x']] != GRID_CONFIG['CODE']['OBSTACLE']):
                    if self.check_surround(scene=scene, pos={'x': self.pos['x'], 'y': self.pos['y'] - 1}):
                        self.pos['y'] = self.pos['y'] - 1
                elif (not self.gravity) and ((self.base - self.jump_from - self.max_jump) == self.pos['y']) and action != 'JUMP':
                    self.gravity = True

                if (not self.gravity) and ((self.base - self.jump_from - self.max_jump) != self.pos['y']) and action != 'JUMP' and (scene._grid[self.pos['y']-(1*self.height)][self.pos['x']] == GRID_CONFIG['CODE']['OBSTACLE']):
                    self.gravity = True
        except(IndexError, AttributeError):
            return
