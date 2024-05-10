"""

M A I N:
Level 0

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.0.0"
__status__ = "WIP"


from time import sleep
import threading
import LVL1_funcs as f



# Thread level one

'''
f.set_status("start")
print(f.game_paused)
f.set_status("pause")
print(f.game_paused)
'''

main_threadlist = [ threading.Thread( target = f.sensors,
                                      args = [],
                                      kwargs = {}),
                    
                    threading.Thread( target = f.interface,
                                      args = [],
                                      kwargs = {}) ]


#start threats
for thread in main_threadlist:
    thread.start()

#wait for threads to join once programm is finished | thread internal check
for thread in main_threadlist:
    thread.join()  
