from config import GRID_CONFIG, PLAYER_CONFIG
from colorama import Fore, Back, Style, init
from random import randint
from enemy import Enemy


class MovingPlatforms:
    '''Characteristics of a moving platform/bridge'''

    def __init__(self, left=None, right=None, pos=None, height=None):
        self.left = left
        self.right = right
        self.pos = pos
        self.height = height
        self.direction = 0

    def move(self):
        '''Function to oscillate the platform/bridge'''
        if self.direction == 0 and self.pos == self.left:
            self.direction = (self.direction + 1) % 2
            return
        elif self.direction == 1 and self.pos == self.right:
            self.direction = (self.direction + 1) % 2
            return
        elif self.direction == 0:
            self.pos = self.pos - 1
            return
        elif self.direction == 1:
            self.pos = self.pos + 1
            return

    def createMe(self, scene=None):
        '''Function to display what is in the park'''
        for i in range(12):
            scene._grid[self.height][self.pos +
                                     i] = GRID_CONFIG['CODE']['OBSTACLE']

    def clearMe(self, scene=None):
        '''Function to clear what is in the grid'''
        for i in range(12):
            scene._grid[self.height][self.pos +
                                     i] = GRID_CONFIG['CODE']['BLANK']

    def refresh(self, scene=None):
        '''Function to refresh what is in the grid'''
        try:
            if scene is None:
                raise AttributeError
            else:
                self.clearMe(scene=scene)
                self.move()
                self.createMe(scene=scene)
        except(AttributeError):
            return


class Coin:
    '''Characteristics of a coin'''

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def collected(self, scene=None):
        '''Function to remove coin from scene when collected'''
        if scene is not None:
            scene._grid[self.y][self.x] = GRID_CONFIG['CODE']['OBSTACLE']

    def show(self, scene=None):
        '''Function to show the coin'''
        if scene is not None:
            scene._grid[self.y][self.x] = GRID_CONFIG['CODE']['COIN']


class Scene:
    '''Characteristics of game screen'''

    def __init__(self, level=1):
        '''Contructor for game screen'''
        self.height = GRID_CONFIG['HEIGHT']
        self.width = GRID_CONFIG['WIDTH']
        self.actual_width = GRID_CONFIG['ACTUAL_WIDTH']
        self.actual_height = GRID_CONFIG['ACTUAL_HEIGHT']
        self.window_left = 0
        self.window_right = GRID_CONFIG['WIDTH'] - 1
        self._grid = [[GRID_CONFIG['CODE']['BLANK']]
                      * self.actual_width for n in range(self.height+2)]
        self.level = level

        self.enemies = []
        self.numEnemies = 4
        self.grass_pos = []
        self.numGrass = 12
        self.pit_pos = []
        self.numPits = 4
        self.cloud_pos = []
        self.cloud_height = []
        self.numClouds = 4
        self.obs_height = []
        self.obs_pos = []
        self.numObs = 4
        self.platform_pos = []
        self.platform_height = []
        self.numPlatforms = 4
        self.movingPlatforms = []
        self.num_moving_platforms = 4
        self.numCoins = 25
        self.coins = []

    def refresh(self, player=None):
        '''Function to refresh the positions of some entities before
        updating player'''
        if player is None:
            return
        count = 0

        # Print the constant objects that cover or hide behind Mario
        self.applyGrass()
        self.applyExitPipe()

        # Generate enemeies
        while count < self.numEnemies:
            if self.enemies[count].lives <= 0:
                self.enemies[count].clearMe(scene=self)
                self.enemies.pop(count)
                self.numEnemies -= 1
            else:
                self.enemies[count].showMe(scene=self)
                count += 1
        if self.level == 3:
            for i in range(self.num_moving_platforms):
                self.movingPlatforms[i].refresh(scene=self)

    def render(self, player=None, enemies=None):
        '''Render game scenery with player, enemies and other obstacles'''
        if player is None:
            return
        else:
            self.applyExitPipe()
            for row in range(self.actual_height):
                for col in range(self.window_left, self.width+self.window_left, 1):
                    if self._grid[row][col] == GRID_CONFIG['CODE']['BLANK']:
                        if self.level == 1:
                            print(Back.LIGHTCYAN_EX + " ", end='')
                        elif self.level == 2:
                            print(Back.LIGHTYELLOW_EX + " ", end='')
                        elif self.level == 3:
                            print(Back.LIGHTCYAN_EX + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['PLAYER']:
                        print(Back.RED + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['CLOUD']:
                        print(Back.WHITE + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['ENEMY']:
                        print(Back.MAGENTA + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['OBSTACLE']:
                        print(Back.LIGHTBLACK_EX + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['EXIT']:
                        print(Back.LIGHTBLUE_EX + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['GRASS']:
                        print(Back.GREEN + " ", end='')
                    elif self._grid[row][col] == GRID_CONFIG['CODE']['COIN']:
                        print(Back.YELLOW + " ", end='')
                    else:
                        self._grid[row][col] = 0
                        print(Back.GREEN + " ", end='')
                print(Back.RESET + '')

    def createMe(self):
        '''Function to generate the mostly randomly generated map'''
        self.createSurface()
        self.createClouds()
        self.createPits()
        self.createGrass()
        self.createObstacles()
        self.createEnemies()
        if self.level < 3:
            self.createPlatforms()
        elif self.level == 3:
            self.createMovingPlatforms()
        self.applyExitPipe()
        self.createCoins()

    def createSurface(self):
        '''Function to create bottom surface'''
        for i in range(self.height, self.actual_height, 1):
            for j in range(self.actual_width):
                self._grid[i][j] = GRID_CONFIG['CODE']['OBSTACLE']

    def createPits(self):
        '''Function to create pits to fall off the surface'''
        max_x = PLAYER_CONFIG['SIZE']
        x_pos = max_x

        for i in range(self.numPits):
            if i == 0:
                x_pos = randint(max_x + 1, max_x + 101)
            else:
                x_pos = randint(max_x + 10, max_x + 110)
            max_x = x_pos
            self.pit_pos.append(x_pos)
        self.applyPits()

    def applyPits(self):
        '''Function to translate the pits to the game by putting its code
        in the file'''
        for i in range(self.numPits):
            for j in range(self.height, self.actual_height, 1):
                for k in range(0, 10 - 1, 1):
                    self._grid[j][k + self.pit_pos[i]
                                  ] = GRID_CONFIG['CODE']['BLANK']

    def createObstacles(self):
        '''Function to create obstacles'''
        max_x = PLAYER_CONFIG['SIZE']
        x_pos = max_x
        count = 0
        flag = True

        while count < self.numObs:
            flag = True
            if count == 0:
                x_pos = randint(max_x + 3, max_x + 101)
            else:
                x_pos = randint(max_x + 25, max_x + 125)
            for i in range(0, 10, 1):
                if self._grid[self.actual_height - 1][x_pos + i] == GRID_CONFIG['CODE']['BLANK']:
                    flag = False
                    break
            if flag is True:
                count += 1
                max_x = x_pos
                self.obs_pos.append(x_pos)
            else:
                continue

            obs_h = randint(4, 6)
            self.obs_height.append(obs_h)
        self.applyObs()

    def applyObs(self):
        '''Function to put the obstacles in the scene'''
        for count in range(self.numObs):
            for j in range(self.height - self.obs_height[count-1], self.height, 1):
                for k in range(0, 7, 1):
                    self._grid[j][k + self.obs_pos[count-1]
                                  ] = GRID_CONFIG['CODE']['OBSTACLE']

    def applyExitPipe(self):
        '''Function to add exit pipe at the end'''
        for i in range(self.height - 5, self.height - 1, 1):
            for j in range(self.actual_width - 8, self.actual_width, 1):
                self._grid[i][j] = GRID_CONFIG['CODE']['EXIT']
        for i in range(4, 9, 1):
            self._grid[self.height - 6][self.actual_width -
                                        i] = GRID_CONFIG['CODE']['EXIT']
            self._grid[self.height - 1][self.actual_width -
                                        i] = GRID_CONFIG['CODE']['EXIT']

    def createClouds(self):
        '''Function to create clouds in the scene'''
        max_x = PLAYER_CONFIG['SIZE']
        x_pos = max_x

        for i in range(self.numClouds):

            if i == 0:
                x_pos = randint(max_x + 1, max_x + 101)
            else:
                x_pos = randint(max_x + 10, max_x + 110)
            if x_pos > max_x:
                max_x = x_pos
            self.cloud_pos.append(x_pos)

            self.cloud_height.append(randint(2, 6))
        self.applyClouds()

    def applyClouds(self):
        '''Function to put the clouds in the scene'''
        for i in range(self.numClouds):
            for j in range(0, 3, 1):
                for k in range(0, 10 - 1, 1):
                    self._grid[j + self.cloud_height[i]][k +
                                                         self.cloud_pos[i]] = GRID_CONFIG['CODE']['CLOUD']

    def createGrass(self):
        '''Function to create grass in the scene'''
        max_x = PLAYER_CONFIG['SIZE']
        x_pos = max_x
        count = 0
        flag = True

        while count < self.numGrass:
            flag = True
            if count == 0:
                x_pos = randint(max_x + 3, max_x + 30)
            else:
                x_pos = randint(max_x + 10, max_x + 40)
            for i in range(0, 10, 1):
                if self._grid[self.actual_height - 1][x_pos + i] == GRID_CONFIG['CODE']['BLANK']:
                    flag = False
                    break
            if flag is True:
                count += 1
                max_x = x_pos
                self.grass_pos.append(x_pos)
            else:
                continue
        self.applyGrass()

    def applyGrass(self):
        '''Function to put the grass in the scene'''
        for count in range(self.numGrass):
            for j in range(self.height - 1, self.height - 3, -1):
                for k in range(0, 3, 1):
                    if self._grid[j][k + self.grass_pos[count]] == GRID_CONFIG['CODE']['BLANK']:
                        self._grid[j][k + self.grass_pos[count]
                                      ] = GRID_CONFIG['CODE']['GRASS']

    def createEnemies(self):
        '''Function to create enemies in the scene'''
        max_x = PLAYER_CONFIG['SIZE']
        x_pos = max_x
        count = 0
        flag = True

        while count < self.numEnemies:
            flag = True
            if count == 0:
                x_pos = randint(max_x + 3, self.pit_pos[count])
            elif count == (self.numEnemies - 1):
                x_pos = randint(
                    self.pit_pos[count - 1], self.actual_width - 15)
            else:
                x_pos = randint(self.pit_pos[count - 1], self.pit_pos[count])
            for i in range(0, 7, 1):
                if self._grid[self.actual_height - 1][x_pos + i] == GRID_CONFIG['CODE']['BLANK'] or self._grid[self.height - 1][x_pos + i] == GRID_CONFIG['CODE']['OBSTACLE']:
                    flag = False
                    break
            if flag is True:
                count += 1
                max_x = x_pos
                if self.level == 1:
                    self.enemies.append(Enemy(
                        name="Enemy", height=None, width=None, speed=1, x=x_pos, y=self.height-1))
                elif self.level > 1:
                    self.enemies.append(Enemy(
                        name="Enemy", height=None, width=None, speed=2, x=x_pos, y=self.height-1))
            else:
                continue
        self.applyEnemies()

    def applyEnemies(self):
        '''Function to put enemies in the scene'''
        for i in range(self.numEnemies):
            self.enemies[i].createMe(
                scene=self, code=GRID_CONFIG['CODE']['ENEMY'])

    def createPlatforms(self):
        '''Function to create platforms in the scene'''
        self.numPlatforms = self.numPits
        for i in range(self.numPits):
            self.platform_pos.append(self.pit_pos[i] - 4)
            self.platform_height.append(
                randint(self.height - 6, self.height - 5))
        self.applyPlatforms()

    def createMovingPlatforms(self):
        '''Function to put the moving platforms in the scene'''
        self.num_moving_platforms = self.numPits
        for i in range(self.num_moving_platforms):
            self.movingPlatforms.append(MovingPlatforms(left=(self.pit_pos[i] - 4), right=(
                self.pit_pos[i] + 5), pos=(self.pit_pos[i] - 4), height=randint(self.height - 6, self.height - 5)))
            self.movingPlatforms[i].createMe(scene=self)

    def applyPlatforms(self):
        '''Function to put the platforms in the scene'''
        for i in range(self.num_moving_platforms):
            for j in range(12):
                self._grid[self.platform_height[i]][self.platform_pos[i] +
                                                    j] = GRID_CONFIG['CODE']['OBSTACLE']

    def createCoins(self):
        '''Function to put coins in the scene'''
        count = 0
        x = 0
        y = 0
        while count < self.numCoins:
            x = randint(1, self.actual_width - 15)
            y = randint(self.height - 9, self.height - 7)
            if self._grid[y][x] == GRID_CONFIG['CODE']['BLANK']:
                self.coins.append(Coin(x=x, y=y))
                self.coins[count].show(scene=self)
                count += 1

    def shift_window(self, player=None):
        '''Function to shift visible window of the scene'''
        if (self.width + self.window_left + (1 * player.speed)) < self.actual_width:
            self.window_left += (1 * player.speed)
            self.window_right += (1 * player.speed)
