#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Wenn ein Spiel, durch eingeben zweier Spieler Namen oder durch durchqueren eines Balles einer
Lichtschranke, gestartet wird, wird der aktuelle Spielstand auf der Anzeige dargestellt. Ändert
sich der Spielstand so wird der Treffer mit durch Anzeige eines weiteren Bildes kenntlich gemacht.
Ist ein spiel beendet wird zu dem HSB Logo gewechselt
"""
__author__ = ["Oliver Bleeker", "Christian Hannover"]
__version__ = "1.0.1"
__status__ = "Ready"	

# Laden der Verwendeten Bibliotheken
import tkinter as tk
from tkinter import *
import sqlite3 as sqlite
import time

root = tk.Tk()
screen = 0
player1_go_alt = 100
player2_go_alt = 100

# Verschiedene Datenbankpfade, da Debug aud Windows PC
try:
    con = sqlite.connect("/var/www/Kicker/cgi-bin/Stats.db")
except:
    con = sqlite.connect("Stats.db")

cur=con.cursor()

# Laden der Bilder
background = PhotoImage(file="/home/kicker/Anzeigetafel/images/schirm.gif")
logo = PhotoImage(file="/home/kicker/Anzeigetafel/images/hsb.gif")
goal1img = PhotoImage(file="/home/kicker/Anzeigetafel/images/goal1img.gif")
goal2img = PhotoImage(file="/home/kicker/Anzeigetafel/images/goal2img.gif")
player1img = PhotoImage(file="/home/kicker/Anzeigetafel/images/player1img.gif")
player2img = PhotoImage(file="/home/kicker/Anzeigetafel/images/player2img.gif")
tooor = PhotoImage(file="/home/kicker/Anzeigetafel/images/tooor.gif")

# Anpassung der Anzeige an das Display
root.overrideredirect(True)
root.title('Anzeigetafel')
root.geometry('800x480')


def ask_player(number):
  """Abfrage der Spielernamen fuer die Anzeige"""
  playernumber = number
  if playernumber == 1:
    cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 1" )
    for playerdb in cur:
        name_player = ("%s") % playerdb
#    player1name.config(text=str(name_player))
  elif playernumber == 2:
    cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 2" )
    for playerdb in cur:
        name_player = ("%s") % playerdb
    #player2name.config(text=str(name_player))
  return name_player

def ask_goals(number):
  """Abfrage der Spielertore fuer die Anzeige"""
  playernumber = number
  if playernumber == 1:
    cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 1" )
    for goalsdb in cur:
        goals_player = (''.join(map(str,goalsdb)))
    #player1goals.config(text=int(goals_player))
  elif playernumber == 2:
    cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 2" )
    for goalsdb in cur:
        goals_player = (''.join(map(str,goalsdb)))
    #player2goals.config(text=int(goals_player))
  return goals_player


# Hintergund HSB Logo vorweg ausgewaehlt um schnellere Anzeige zu gewaehrleisten  
background_main = Label(master=root, image=logo)				#hab hier das von logo auf background geaendert
background_main.place(x=0, y=0, width=800, height=480)

# Beginn der Hauptschleife
while True:
	# Abrage der der Spielertore fuer die Bildauswahl
	player1_go= ask_goals(1)
	player2_go= ask_goals(2)

	if player1_go == "99" and player2_go == "99":
		if screen == 1:
			# Hintergrund
			background_main = Label(master=root, image=logo)
			background_main.place(x=0, y=0, width=800, height=480)
			screen = 0
	else:
		if player1_go != player1_go_alt or player2_go != player2_go_alt:
			if player1_go != "0" or player2_go != "0":
				background_main = Label(master=root, image=tooor)				#hab hier das von logo auf background geaendert
				background_main.place(x=0, y=0, width=800, height=480)
				root.update()
				time.sleep(2)
				screen = 0
		if screen == 0:
			# Hintergrund
			background_main = Label(master=root, image=background)
			background_main.place(x=0, y=0, width=800, height=480)
			screen = 1
			
			# Spielernamen
			player1name = Label(
							root, 
							fg="white",
							font=('Arial', 30),
							text=ask_player(1), 
							compound = CENTER,						#Bild wird versetzt
							image=player1img)
			player1name.place(x=102, y=343, width=200, height=50)
		
			player2name = Label(
							root, 
							fg="white",
							font=('Arial', 30),
							text=ask_player(2), 
							compound = CENTER,						#Bild wird versetzt
							image=player2img)
			player2name.place(x=482, y=343, width=200, height=50)

		
		if player1_go != player1_go_alt or player2_go != player2_go_alt:
			# Anzahl der Tore
			player1goals = Label(
								root, 
								fg="white",
								font=('Arial', 90),
								text=ask_goals(1), 
								compound = CENTER,						#Bild wird versetzt
								image=goal1img)
			player1goals.place(x=102, y=129, width=198, height=203)
			
			player2goals = Label(
								root, 
								fg="white",
								font=('Arial', 90),
								text=ask_goals(2), 
								compound = CENTER,						#Bild wird versetzt
								image=goal2img)
			player2goals.place(x=486, y=129, width=198, height=203)
			
			player1_go_alt = player1_go
			player2_go_alt = player2_go
	
	root.update()
	time.sleep(1)
			
root.mainloop()
