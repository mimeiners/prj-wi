"""
This is meant to be used as an imported modules file for the main file 
and is basically listing all the available functions (literally) the kicker posesses.
Current version is assuming AuVAReS is always available
"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.1"
__status__ = " heavy WIP"


import time
import RPi.GPIO as GPIO


# these functions need to communicate to auvares
def startup():
    # setting up local stuff like GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    # also set up display (tkinter) on auvares
    return
def display_score():
    # send score to auvares
    return
def display_goal():
    # tell auvares to put up the goal image for a few seconds
    return
def display_gameover():
    # tell auvares to put up the gamover image for a few seconds
    return
def display_screensaver():
    # tell auvares to put up the screensaver
    return


# inform auvares of game events, e.g. to trigger a replay/start drone
def notify_auvares():
    # goal, foul, gamestart, gameover, score
    return


# open website and stuff??
def database_savegame():
    # very big TBD
    return


# polling sensors and peripherals
def poll_sensor1(): # checking for goals
    if GPIO.input(13) == GPIO.LOW:
        return True
    return False
def poll_sensor2(): # checking for goals
    if GPIO.input(15) == GPIO.LOW:
        return True
    return False
def poll_auvares(): # checking if auvares is available/has started
    # return True if a certain pin is low (parallel) or message received (serial)
    return
def poll_foul(): # Kurbelerkenung
    # will probably run in another thread an spit out boolean
    return
def poll_startbutton(): # please press the start button
    if GPIO.input(?) == GPIO.LOW:
        return True
    return False    


# counting goals
global goals1; goals1 = 0
global goals2; goals2 = 0
def score_addgoal1():
    global goals1; goals1 += 1
    return
def score_addgoal2():
    global goals2; goals2 += 1
    return


# regulating the flow of the game and breaks
def wait_after_goal():
    time.sleep(0) #1.5 secs?
    return
def wait_after_loop():
    time.sleep(0) #0.01 secs?
    return
def wait_after_game():
    time.sleep(0) #10 secs?
    return


# game status, needed for while loops
global game_running; game_running = False
def set_status_running():
    global game_running; game_running = True
    return
def set_status_ready():
    global game_running; game_running = False
    return