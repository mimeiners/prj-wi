# bibs
import os
import numpy as np
import time
import sys

#functions
def monitor_names():
	print("Start name wait")
	while True:
		if os.path.exists("/var/www/html/PlayerNames.txt"):
			with open("/var/www/html/PlayerNames.txt", "r") as names_file:
				names = names_file.read().strip()
			if names:
				name1, name2 = names.split(",")
				print("game start")
				return name1, name2
			else:
				print("wait for names")
				time.sleep(1)
		else:
			print("no names")
			time.sleep(1)

	
def monitor_drone():
	print("Start drone wait")
	while True:
		if os.path.exists("/var/www/html/DroneCheck.txt"):
			with open("/var/www/html/DroneCheck.txt", "r") as Dcheck_file:
				check = Dcheck_file.read().strip()
			if check:
				check == "success"
				print("drone start")
				return check
			else:
				print("wait for drone")
				time.sleep(1)
		else:
			print("no drone")
			time.sleep(1)

def clear_names():					# redundant function, clear now on reset
	open("/var/www/html/PlayerNames.txt", "w").close()
	return
	
def clear_drone_check():			# redundant function, clear now on reset
	open("/var/www/html/DroneCheck.txt", "w").close()
	return


def reset_check():
	if os.path.exists("/var/www/html/PlayerNames.txt"):
			with open("/var/www/html/PlayerNames.txt", "r") as names_file:
				names = names_file.read().strip()
				
	if os.path.exists("/var/www/html/DroneCheck.txt"):
			with open("/var/www/html/DroneCheck.txt", "r") as Dcheck_file:
				check = Dcheck_file.read().strip()
				
	if names == "":
		return "reset"
#main
Names = monitor_names()
PlayerName1 = Names[0]
PlayerName2 = Names[1]

print(PlayerName1, PlayerName2)

Drone = monitor_drone()
print(Drone)

#clear_names()
#clear_drone_check()

while True: # loop for testing purposes
	
	print("game running")
	time.sleep(1)
	reset = reset_check()
	if reset == "reset":
		print("game was reset")
		break
		
