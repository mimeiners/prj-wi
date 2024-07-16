

# bibs
import os
import numpy as np
import time
import sys
import RPi.GPIO as GPIO 

# functions

def punkteausgabe(tore1, tore2, name1, name2):	# diese gibt NUR das Ergebniss in der Konsole aus
	print(name1,": ", tore1)
	print(name2,": ", tore2)
	return



def checkend(ToreS1, ToreS2):
	"""Überprüfen ob das aktuelle Spiel zu Ende ist. Dies ist der Fall wenn ein Spieler 6 Tore oder beide Spieler 5 Tore geschossen haben"""
	if ToreS1 == 6 or ToreS2 == 6:
		print("game over")
		return 1
	
	elif ToreS1 == 5 and ToreS2 == 5:
		print("game over")
		return 1
	
	else:
		return 0

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
				print("wait")
				time.sleep(1)
		else:
			print("no names")
			time.sleep(1)

def clear_names():
	open("/var/www/html/PlayerNames.txt", "w").close()
	return

