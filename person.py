from config import GRID_CONFIG, PLAYER_CONFIG
import os


class Person:
    '''Characteristics of a person'''

    def __init__(self, name, height, width, speed):
        '''Contructor for person objects'''
        self.name = name
        self.height = height
        self.width = width
        self.speed = speed
        self.pos = {'x': 0, 'y': (GRID_CONFIG['HEIGHT'] - 1)}
        self.gravity = True
        self.surface = GRID_CONFIG['HEIGHT'] - 1
        self.base = GRID_CONFIG['ACTUAL_HEIGHT'] - 1
        self.max_jump = self.height * 2
        self.jump_from = self.base

    def move(self):
        '''Function to be over ridden by child classes'''
        pass

    def createMe(self, scene=None, code=None):
        '''Function to create the Player o the board'''
        if scene is None:
            return
        if code is None:
            return
        for i in range(self.pos['y'], self.pos['y'] - self.height, -1):
            for j in range(self.width):
                scene._grid[i][self.pos['x']+j] = code

    def clearMe(self, scene=None):
        '''Function to clear the Player o the board'''
        if scene is None:
            return
        for i in range(self.pos['y'], self.pos['y'] - self.height, -1):
            for j in range(self.width):
                scene._grid[i][self.pos['x']+j] = GRID_CONFIG['CODE']['BLANK']

    def showMe(self, action=None, scene=None):
        '''Function to show the player on the grid when scene map is rendered'''
        if scene is not None:
            self.clearMe(scene=scene)
            if action is not None:
                self.move(action=action, scene=scene)
            else:
                self.move(scene=scene)
            self.createMe(scene=scene)

    def check_surround(self, scene=None, pos=None):
        '''Check for ragging'''
        for i in range(pos['y'], pos['y'] - self.height, -1):
            for j in range(self.width):
                if (scene._grid[i][pos['x']+j] != GRID_CONFIG['CODE']['BLANK'] and scene._grid[i][pos['x']+j] != GRID_CONFIG['CODE']['CLOUD'] and scene._grid[i][pos['x']+j] != GRID_CONFIG['CODE']['EXIT'] and scene._grid[i][pos['x']+j] != GRID_CONFIG['CODE']['GRASS'] and scene._grid[i][pos['x']+j] != GRID_CONFIG['CODE']['COIN']) or scene._grid[i][pos['x']+j] == GRID_CONFIG['CODE']['PLAYER']:
                    self.check_clash(scene=scene, y=i, x=pos['x']+j, pos=pos)
                    return False
                if self.name == 'Mario' and scene._grid[i][pos['x']+j] == GRID_CONFIG['CODE']['COIN']:
                    for coin in scene.coins:
                        if coin.x == (pos['x'] + j) and coin.y == i:
                            coin.collected(scene=scene)
                            scene.coins.remove(coin)
                            os.system("aplay -q Sounds/coin.wav &")
                            # scene.numCoins -= 1
                            self.score += 1000

        return True

    def check_clash(self, scene=None, y=None, x=None, pos=None):
        '''Check for clashes between  player and other entities'''
        if self.pos['y'] == pos['y']:
            if self.name == 'Mario':
                if scene._grid[y][x] == GRID_CONFIG['CODE']['ENEMY']:
                    PLAYER_CONFIG['LIVES_LOST'] += 1

                    # Sound for losing a life
                    os.system("aplay -q Sounds/bump.wav &")

            elif self.name == 'Enemy':
                if scene._grid[y][x] == GRID_CONFIG['CODE']['PLAYER']:
                    PLAYER_CONFIG['LIVES_LOST'] += 1
                    os.system("aplay -q Sounds/bump.wav &")
        elif self.pos['y'] != pos['y']:
            if self.name == 'Mario':
                for i in range(scene.numEnemies):
                    for j in range(x, x + PLAYER_CONFIG['SIZE'], 1):
                        if scene.enemies[i].pos['x'] in range(x, x + PLAYER_CONFIG['SIZE'], 1) and (scene._grid[y+1][j] == GRID_CONFIG['CODE']['ENEMY']):
                            os.system("aplay -q Sounds/kill.wav &")
                            scene.enemies[i].lives -= 1
                            self.score += 1000
                            break
                    if scene.enemies[i].lives == 0:
                        break
