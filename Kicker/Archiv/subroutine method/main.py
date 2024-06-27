"""
THIS FILE IS NOT ACTUALLY EXECUTABLE YET
Prototype for using a main file and a modules file so that main is a bit more easy to grasp
"import main_modules.py as a", more useful name can be chosen later (Ctrl+F replace); "import ... as ..." is needed for variables to actually be updated while running, "from ... import ..." doesnt do it

to be added:
- replace "while True" with bool for emergency shutdown
- use try/except/finally
- use threads library for polling

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.1"
__status__ = "heavy WIP"


import main_modules.py as a
import time

# POWERON
while a.poll_auvares == False:
    time.sleep(3)
    print("AuVAReS not found")
a.startup() # set up display, GPIO, global variables on auvares
a.set_status_ready()
a.display_screensaver()

# GAMING
while True:
    # check start button
    if a.poll_startbutton() is True:
        a.notify_auvares("gamestart")
        a.set_status_running()
        a.display_score()
    a.wait_after_loop()

    while a.game_running:
        # check for goals
        if a.poll_sensor1 == True:
            a.score_addgoal1()
            a.notify_auvares("goal")
            a.display_goal()
            a.wait_after_goal()
            a.display_score()
        if a.poll_sensor2 == True:
            a.score_addgoal2()
            a.notify_auvares("goal")
            a.display_goal()
            a.wait_after_goal()
            a.display_score()
        # check for Kurbelvergehen (maybe has to be called more often)
        if a.poll_foul == True:
            a.notify_auvares("foul")
        # check win condition
        if (a.goals1 == 6 or a.goals2 == 6) or (a.goals1 == 5 and a.goals2 == 5):
            a.set_status_ready()
            a.notify_auvares("gameover")
            a.display_gameover()
            a.database_savegame()
            a.wait_after_game()
            a.set_status_ready()
            a.display_screensaver()
            # we return to outside "while game_running"
        a.wait_after_loop()