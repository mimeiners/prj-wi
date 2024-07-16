#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Dieser Code basiert auf der alten main.py der Anzeigetafel und der Sensoren.py aus "./Kicker/www/cgi-bin".
Diese Version ersetzt die Datenbank durch einfache Variablen, welche mitzählen. 
Die Spielernamen werden über einen WebServer abgefragt.  
"""
__author__ = "Martin Schwarz"
__credits__ = ["Oliver Bleeker", "Christian Hannover"]
__version__ = "1.2.2"
__status__ = "WIP"

# bibs
import os
import numpy as np
import time
import sys
import RPi.GPIO as GPIO 		#https://pypi.org/project/RPi.GPIO/: 
								#"Note that the current release does not support SPI, I2C, hardware PWM or serial functionality on the RPi yet"
import Game_functions as game



# GPIO Setup, muss im main gemacht werden !!
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Variablen welche die Punkte zählen
ToreS1= 0
ToreS2= 0

ToreS1_alt = 0
ToreS2_alt = 0

Names = game.monitor_names()
PlayerName1 = Names[0]
PlayerName2 = Names[1]

game.clear_names()



while True:
#{loop begin		
# game
	if game.checkend(ToreS1, ToreS2) == 1:
		game.punkteausgabe(ToreS1, ToreS2, PlayerName1, PlayerName2)
		time.sleep(1)
		break
	else:
		if GPIO.input(13) == GPIO.LOW: #Tor Spieler 1
			if ToreS1 == 99 or ToreS2 == 99:
				ToreS1 = 0
				ToreS2 = 0
			ToreS1_alt = ToreS1
			ToreS1 = ToreS1 +1
			print ("Tor Spieler 1 ",PlayerName1,": ", ToreS1)
			game.checkend(ToreS1, ToreS2)
			time.sleep(1.0)

		
		if GPIO.input(15) == GPIO.LOW: #Tor Spieler 2
			if ToreS1 == 99 or ToreS2 == 99:
				ToreS1 = 0
				ToreS2 = 0
			ToreS2_alt = ToreS2
			ToreS2 = ToreS2 +1
			print ("Tor Spieler 2 ",PlayerName2,": ", ToreS2)
			game.checkend(ToreS1, ToreS2)
			time.sleep(1.0)
	time.sleep(0.01)	
		
	ToreS1_alt = ToreS1
	ToreS2_alt = ToreS2
	
	time.sleep(1)
	
	





