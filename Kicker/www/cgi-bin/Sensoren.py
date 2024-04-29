#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Die Lichtschranken an den GPIO Ports werden in der Hauptschleife abgefragt. Ändert eine der beiden
seinen Zustand so wird je nach Seite der Lichtschranke ein Tor dem Jeweiligen Spieler
zugerechnet. Dies wird direkt in der Datenbank abgelegt. Anschließend wird überprüft ob der
Spielstand das Ende des laufenden Spiels ist. Ist dies der Fall werden die Spielernamen und
Tore weitergegeben um diese auszuwerten und in der Datenbank abzulegen.
"""	
__author__ = "Oliver Bleeker"
__credits__ = ["Christian Hannover"]
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import time 
import sys
import RPi.GPIO as GPIO 
import sqlite3 as sqlite 
import function_add_game

# Globale Variablen Definieren
con = sqlite.connect("Stats.db") 
cur=con.cursor()
rungame = 0

# Definieren der GPIO Ports
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Datenbank zu beginn erstellen wenn nicht vorhanden und mit Standard Werten beschreiben.
cur.execute("create table if not exists GamePlayers (Nummer INT,Spieler TEXT,Tore INT)")
cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=1")
cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=2")
cur.execute ("UPDATE GamePlayers Set Spieler='Spieler1' WHERE Nummer=1")
cur.execute ("UPDATE GamePlayers Set Spieler='Spieler2' WHERE Nummer=2")
con.commit()

# Funktionsblock Spielertore abfragen
def ask_goals(number):
	"""Abfrage der Tore des aktuellen Spiels eines Spielers"""	
	playernumber = number
	if playernumber == 1:
		cur.execute ("SELECT Tore FROM GamePlayers WHERE Nummer=1")
		ToreS1 = cur.fetchall()
		for row in ToreS1:
			goals_player = int(''.join(map(str,row)))
	elif playernumber == 2:
		cur.execute ("SELECT Tore FROM GamePlayers WHERE Nummer=2")
		ToreS2 = cur.fetchall()
		for row in ToreS2:
			goals_player = int(''.join(map(str,row)))
		
	print goals_player
	rungame = 1
	return goals_player

# Funktionsblock Spielernamen abfragen
def ask_player(number):
  """Abfrage der Spielernamen des aktuellen Spiels"""	
  playernumber = number
  if playernumber == 1:
    cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 1" )
    for playerdb in cur:
        name_player = ("%s") % playerdb
  elif playernumber == 2:
    cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 2" )
    for playerdb in cur:
        name_player = ("%s") % playerdb
  return name_player

# Funktionsblock abfragen und prüfen ob das Spiel zu Ende ist
def checkend():
	"""Überprüfen ob das aktuelle Spiel zu Ende ist. Dies ist der Fall wenn ein Spieler 6 Tore oder beide Spieler 5 Tore geschossen haben"""
	check = "Noend"
	ToreS1=ask_goals(1)
	ToreS2=ask_goals(2)
	NameS1=ask_player(1)
	NameS2=ask_player(2)
	if ToreS1 == 6 or ToreS2 == 6:
		if NameS1 != "Spieler1" and ToreS2 != "Spieler2":
			messagecode = function_add_game. addgame(NameS1,ToreS1,ToreS2,NameS2)
		time.sleep(3)
		cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=1")
		cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=2")
		cur.execute ("UPDATE GamePlayers Set Spieler='Spieler1' WHERE Nummer=1")
		cur.execute ("UPDATE GamePlayers Set Spieler='Spieler2' WHERE Nummer=2")
		con.commit()
		check = "End"
		rungame = 0
	if ToreS1 == 5 and ToreS2 == 5:
		if NameS1 != "Spieler1" and ToreS2 != "Spieler2":
			messagecode = function_add_game. addgame(NameS1,ToreS1,ToreS2,NameS2)
		time.sleep(3)
		cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=1")
		cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=2")
		cur.execute ("UPDATE GamePlayers Set Spieler='Spieler1' WHERE Nummer=1")
		cur.execute ("UPDATE GamePlayers Set Spieler='Spieler2' WHERE Nummer=2")
		con.commit()
		check = "End"
		rungame = 0
	return check
 
# Hauptschleife: Abrfage der GPIO Ports. Updaten des Spielstandes bei auslösen einer Lichtschranke
while True:
	if GPIO.input(13) == GPIO.LOW: #Tor Spieler 1
		ToreS1=ask_goals(1) # Abfragen Tore Spieler 1
		ToreS2=ask_goals(2) # Abfragen Tore Spieler 2
		if ToreS1 == 99 or ToreS2 == 99:
			cur.execute ("UPDATE GamePlayers Set Tore=0 WHERE Nummer=1")
			cur.execute ("UPDATE GamePlayers Set Tore=0 WHERE Nummer=2")
		cur.execute ("UPDATE GamePlayers Set Tore = Tore + 1 WHERE Nummer=1")
		con.commit()
		print "Tor Spieler 1 Gruen"
		checkend()
		time.sleep(1.0)
		
	if GPIO.input(15) == GPIO.LOW: #Tor Spieler 2
		ToreS1=ask_goals(1) # Abfragen Tore Spieler 1
		ToreS2=ask_goals(2) # Abfragen Tore Spieler 2
		if ToreS1 == 99 or ToreS2 == 99:
			cur.execute ("UPDATE GamePlayers Set Tore=0 WHERE Nummer=1")
			cur.execute ("UPDATE GamePlayers Set Tore=0 WHERE Nummer=2")
		cur.execute ("UPDATE GamePlayers Set Tore = Tore + 1 WHERE Nummer=2")
		con.commit()
		print "Tor Spieler 2 Weiss"
		checkend()
		time.sleep(1.0)
	time.sleep(0.01)