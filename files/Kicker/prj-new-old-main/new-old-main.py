#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Versuch das alte Spiel aus den alten Daten (ohne die Datenbank) wieder lauffähig zu bekommen.
Dieser Code basiert auf der alten main.py der Anzeigetafel und der Sensoren.py aus "./Kicker/www/cgi-bin".
Diese Version ersetzt die Datenbank durch einfache Variablen, welche mitzählen. 
Die Spielernamen werden über die Konsole abgefragt und es gibt jetzt ein Game Over screen mit einem Temporären Bild zum Testen. 

Leider funktionieren relative Datei-Pfade nicht, weshalb der Pfad der Bilder angepasst werden muss, dieser sollte wie folgt aussehen:

		/home/[User]/Documents/prj-new-old-main/Bilder/[Bild-Name]

Der Einfachheit halber empfiehlt es sich den Ordner "new-old-main" ebenfalls im „Documents“-Verzeichnis des Pi abzulegen. 
"""
__author__ = "Martin Schwarz"
__credits__ = ["Oliver Bleeker", "Christian Hannover"]
__version__ = "1.0.0"
__status__ = "WIP"

# bibs
import tkinter as tk			#bib um GUI zu erstellen
#from tkinter import *			#auskommentiert um die Modulzuweisung zu behalten
import time
import sys
import RPi.GPIO as GPIO 		#https://pypi.org/project/RPi.GPIO/: 
								#"Note that the current release does not support SPI, I2C, hardware PWM or serial functionality on the RPi yet"


# bilder
root = tk.Tk()
screen = 0

background = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/schirm.gif")	# Pfad nach Bedarf ändern !
logo = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/hsb.gif")
goal1img = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/goal1img.gif")
goal2img = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/goal2img.gif")
player1img = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/player1img.gif")
player2img = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/player2img.gif")
tooor = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/tooor.gif")
gameFinish = tk.PhotoImage(file="/home/amogus/Documents/prj-new-old-main/Bilder/amogus_sus")

# Anpassung der Anzeige an das Display
#root.overrideredirect(True)
root.title('Anzeigetafel')
root.geometry('800x480')

# Definieren der GPIO Ports
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Variablen welche die Punkte zählen
ToreS1= 0
ToreS2= 0

ToreS1_alt = 0
ToreS2_alt = 0

# Funktionen
def punkteausgabe(tore1, tore2, name1, name2):	# diese gibt NUR das Ergebniss in der Konsole aus
	print(name1,": ", tore1)
	print(name2,": ", tore2)
	return



def checkend():
	"""Überprüfen ob das aktuelle Spiel zu Ende ist. Dies ist der Fall wenn ein Spieler 6 Tore oder beide Spieler 5 Tore geschossen haben"""
	if ToreS1 == 6 or ToreS2 == 6:
		print("game over")
		return 1
	
	elif ToreS1 == 5 and ToreS2 == 5:
		print("game over")
		return 1
	
	else:
		return 0



# Background defult
background_main = tk.Label(master=root, image=logo)
background_main.place(x=0, y=0, width=800, height=400)
screen = 0
	
# Abfrage der Spielernamen über die Konsole:
PlayerName1 = input("Enter Player 1: ")
PlayerName2 = input("Enter Player 2: ")	
	
# Hauptschleife: Abfrage der GPIO Ports. Updaten des Spielstandes bei auslösen einer Lichtschranke
while True:
#{loop begin		
# game
	if checkend() == 1:
		punkteausgabe(ToreS1, ToreS2, PlayerName1, PlayerName2)
		gameOver = tk.Label(
						root, 
						fg="black",
						font=('Arial', 60),
						text="Game Over", 
						compound = CENTER,					#Check for correct parameter				
						image=gameFinish)
		gameOver.place(x=0, y=0, width=800, height=600)
		root.update()
		time.sleep(5.0)
		break
	else:
		if GPIO.input(13) == GPIO.LOW: #Tor Spieler 1
			if ToreS1 == 99 or ToreS2 == 99:
				ToreS1 = 0
				ToreS2 = 0
			ToreS1_alt = ToreS1
			ToreS1 = ToreS1 +1
			print ("Tor Spieler 1 ",PlayerName1,": ", ToreS1)
			checkend()
			time.sleep(1.0)

		
		if GPIO.input(15) == GPIO.LOW: #Tor Spieler 2
			if ToreS1 == 99 or ToreS2 == 99:
				ToreS1 = 0
				ToreS2 = 0
			ToreS2_alt = ToreS2
			ToreS2 = ToreS2 +1
			print ("Tor Spieler 2 ",PlayerName2,": ", ToreS2)
			checkend()
			time.sleep(1.0)
	time.sleep(0.01)	
	
# bilder
	# Abrage der der Spielertore fuer die Bildauswahl
	if ToreS1 == "99" and ToreS2 == "99":
		if screen == 1:
			# Hintergrund
			background_main = tk.Label(master=root, image=logo)
			background_main.place(x=0, y=0, width=800, height=480)
			screen = 0
	else:
		if ToreS1 != ToreS1_alt or ToreS2 != ToreS2_alt:
			if ToreS1 != "0" or ToreS2 != "0":
				background_main = tk.Label(master=root, image=tooor)				
				background_main.place(x=0, y=0, width=800, height=480)
				root.update()
				time.sleep(1)
				screen = 0

		if screen == 0:
			# Hintergrund
			background_main = tk.Label(master=root, image=background)
			background_main.place(x=0, y=0, width=800, height=480)
			screen = 1
			
			# Spielernamen
			player1name = tk.Label(
							root, 
							fg="black",
							font=('Arial', 30),
							text=PlayerName1, 
							compound = CENTER,						
							image=player1img)
			player1name.place(x=102, y=343, width=200, height=50)
		
			player2name = tk.Label(
							root, 
							fg="black",
							font=('Arial', 30),
							text=PlayerName2, 
							compound = CENTER,						#Bild wird versetzt
							image=player2img)
			player2name.place(x=482, y=343, width=200, height=50)

		if ToreS1 != ToreS1_alt or ToreS2 != ToreS2_alt:
			# Anzahl der Tore
			player1goals = tk.Label(
								root, 
								fg="black",
								font=('Arial', 90),
								text=ToreS1, 
								compound = CENTER,						#Bild wird versetzt
								image=goal1img)
			player1goals.place(x=102, y=129, width=198, height=203)
			
			player2goals = tk.Label(
								root, 
								fg="black",
								font=('Arial', 90),
								text=ToreS2, 
								compound = CENTER,						#Bild wird versetzt
								image=goal2img)
			player2goals.place(x=486, y=129, width=198, height=203)
			
			ToreS1_alt = ToreS1
			ToreS2_alt = ToreS2
	
	root.update()
	time.sleep(1)
#loop end}
	
	





