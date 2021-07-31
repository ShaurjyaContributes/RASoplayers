import sys
import termios
import tty
import os
import time
from config import FRAME_RATE
from colorama import Fore


def keyAction(key=None, player=None, scene=None):
    """Function that handles the behaviour of the player for different key presses."""
    if scene is None:
        return
    if player is None:
        return
    if key is None:
        # Print the player onto the game scene
        player.showMe(scene=scene)
    else:
        if key == 'q':
            print(Fore.RED + "QUIT")
            time.sleep(1/FRAME_RATE)
            return False
        elif key == 'a':
            player.showMe(action='LEFT', scene=scene)
            time.sleep(1/FRAME_RATE)
        elif key == 'd':
            player.showMe(action='RIGHT', scene=scene)
            time.sleep(1/FRAME_RATE)
        elif key == 'w':
            player.showMe(action='JUMP', scene=scene)
            time.sleep(1/FRAME_RATE)
        else:
            pass
            time.sleep(1/FRAME_RATE)
    return True
