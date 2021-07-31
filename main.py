import config
import time
import os
import helpers
from colorama import Back, Fore, Style
from player import Player
from enemy import Enemy
from scene import Scene
from input import Get, input_to

# Wile loop control variable
GAME_PLAY = True

score_level = []
scenes = [Scene(level=1), Scene(level=2), Scene(level=3)]
player = Player(name="Mario", height=None, width=None, speed=1)
# Input object
getch = Get()

# Result of Game
result = False

# Play the start music
os.system("aplay -q Sounds/start.wav &")

# Iterate over the 3 levels implemented
for i in range(0, config.NUM_LEVELS):
    result = False

    # Choose scene according to level
    scene = scenes[i]

    scene.createMe()
    player.reset_pos()
    player.createMe(scene=scene)

    # Score from previous level
    score_level.append(player.score)

    while GAME_PLAY:
        # Clear screen before re-render
        os.system('cls' if os.name == 'nt' else 'clear')

        # Calculate score as a function of x coordinate
        new_score = (
            int(player.pos['x'] / (player.width * 2)) * 200) + score_level[i]
        if new_score > player.score:
            player.score = new_score

        # Print the score
        print(Fore.CYAN +
              "\n\t\t\tScore: {0}\t\tLives: {1}\n".format(player.score, player.lives))

        # Render the grid
        scene.render(player=player)

        # Decrease the number of lives of the player
        player.lives = config.PLAYER_CONFIG['START_LIVES'] - \
            config.PLAYER_CONFIG['LIVES_LOST']

        # If player lives become 0, end game
        if player.lives <= 0:
            result = False
            break

        # If player enters pipe at the end of the level, he goes to next level, or completes game
        if player.pos['x'] > (scene.actual_width - config.PLAYER_CONFIG['SIZE'] - 5):
            result = True
            player.score += player.lives * 1000
            break

        if player.pos['y'] == player.base:
            result = False
            break

        # Refresh screen
        scene.refresh(player=player)

        # Accept key input
        key_pressed = input_to(getch, timeout=5000/config.FRAME_RATE)
        if key_pressed is not None:
            GAME_PLAY = helpers.keyAction(
                key=key_pressed.lower(), player=player, scene=scene)
        else:
            GAME_PLAY = helpers.keyAction(key=None, player=player, scene=scene)
    # If the game was quit, or lost, don't go to next level
    if result == False:
        break

# Play GAME OVER song
os.system("aplay -q Sounds/gameover.wav &")

if result is False:
    os.system('cls' if os.name == 'nt' else 'clear')

    new_score = int(player.pos['x'] / (player.width * 2)) * 200
    if new_score > player.score:
        player.score = new_score

    print(Fore.CYAN +
          "\n\t\t\tScore: {0}\t\tLives: {1}\n".format(player.score, player.lives))

    scene.render(player=player)

    print(Fore.RED + '\n\t\t\t\t  GAME OVER')
    print(Fore.BLUE + '\n\t\t\t\t Score: {0}\n'.format(player.score))
else:
    os.system('cls' if os.name == 'nt' else 'clear')

    new_score = int(player.pos['x'] / (player.width * 2)) * 200
    if new_score > player.score:
        player.score = new_score

    print(Fore.WHITE +
          "\n\t\t\tScore: {0}\t\tLives: {1}\n".format(player.score, player.lives))

    scene.render(player=player)

    print(Fore.RED + '\n\t\t\t\t  GAME OVER')
    print(Fore.GREEN + '\n\t\t\t\t   YOU WON')
    print(Fore.BLUE + '\n\t\t\t\t Score: {0}'.format(player.score))
