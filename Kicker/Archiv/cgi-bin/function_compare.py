#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Aus der Eingabeseite der WEB GUI Werden Zwei Spielernamen  übertragen.  Zu diesen Spielern
werden alle Spiele zwischen den beiden Spielen ermittelt und deren Ergebnissen verglichen.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite

# Definieren von Globelen Variablen 
con = sqlite.connect("Stats.db")
cur=con.cursor()

def askplayername(number):	
	"""Spielernummer einem Spielernamen zuordnen"""
	cur.execute ("SELECT Name FROM Players WHERE Nummer=?", (number, ))
	for playernumberdb in cur:
		playername1 = ("%s") % playernumberdb
	return (playername1)

def askplayerscore(name1,name2):	
	"""Spielernummer einem Spielernamen zuordnen"""
	cur.execute ("SELECT Bewertung FROM Players WHERE Name=?", (name1,  ))
	for askplayerscoredb in cur:
		askplayerscore = ("%s") % askplayerscoredb
	return (askplayerscore)
	
def askplayerpoints(name1,name2):
	"""Anzahl der Punkte beider Spieler im direkten Duell abfragen"""
	cur.execute ("SELECT SUM (PunkteSpieler1) FROM Games WHERE Spieler1=? AND Spieler2 =?", (name1, name2,  ))
	points1db = cur.fetchall()
	for row in points1db:
		points1 =(''.join(map(str,row)))
		if points1 == "None":
			points1 = 0
		else:
			points1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (PunkteSpieler2) FROM Games WHERE Spieler2=? AND Spieler1 =?", (name1, name2,  ))
	points2db = cur.fetchall()
	for row in points2db:
		points2 = (''.join(map(str,row)))
		if points2 == "None":
			points2 = 0
		else:
			points2 = float(''.join(map(str,row)))
		
	playerpoints = (points1 + points2)
	return (playerpoints)

def askplayergoals(name1,name2):
	"""Anzahl der Tore beider Spieler im direkten Duell abfragen"""
	cur.execute ("SELECT SUM (ToreSpieler1) FROM Games WHERE Spieler1=? AND Spieler2 =?", (name1, name2,  ))
	goals1db = cur.fetchall()
	for row in goals1db:
		goals1 = (''.join(map(str,row)))
		if goals1 == "None":
			goals1 = 0
		else:
			goals1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (ToreSpieler2) FROM Games WHERE Spieler2=? AND Spieler1 =?", (name1, name2,  ))
	goals2db = cur.fetchall()
	for row in goals2db:
		goals2 = (''.join(map(str,row)))
		if goals2 == "None":
			goals2 = 0
		else:
			goals2 = float(''.join(map(str,row)))
		
	playergoals = (goals1 + goals2)
	return (playergoals)

def askplayergoalsagainst(name1,name2):	
	"""Anzahl der Gegentore beider Spieler abfragen"""
	cur.execute ("SELECT SUM (ToreSpieler2) FROM Games WHERE Spieler1=? AND Spieler2 =?", (name1, name2,  ))
	goalsagainst1db = cur.fetchall()
	for row in goalsagainst1db:
		goalsagainst1 = (''.join(map(str,row)))
		if goalsagainst1 == "None":
			goalsagainst1 = 0
		else:
			goalsagainst1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (ToreSpieler1) FROM Games WHERE Spieler2=? AND Spieler1 =?", (name1, name2,  ))
	goalsagainst2db = cur.fetchall()
	for row in goalsagainst2db:
		goalsagainst2 = (''.join(map(str,row)))
		if goalsagainst2 == "None":
			goalsagainst2 = 0
		else:
			goalsagainst2 = float(''.join(map(str,row)))
		
	playergoalsagainst = (goalsagainst1 + goalsagainst2)
	return (playergoalsagainst)

def askplayercount(name1,name2):	
	"""Anzahl der Spiele beider Spieler im direkten Duell abfragen"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND Spieler2 =?", (name1, name2,  ))
	playercount1db = cur.fetchall()
	for row in playercount1db:
		playercount1 = (''.join(map(str,row)))
		if playercount1 == "None":
			playercount1 = 0
		else:
			playercount1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND Spieler1 =?", (name1, name2,  ))
	playercount2db = cur.fetchall()
	for row in playercount2db:
		playercount2 = (''.join(map(str,row)))
		if playercount2 == "None":
			playercount2 = 0
		else:
			playercount2 = int(''.join(map(str,row)))		
	playercount = playercount1 + playercount2
	return (playercount)

def askplayerwin(name1,name2):	
	"""Anzahl der Siege beider Spieler im direkten Duell abfragen"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=3 AND Spieler2 =?", (name1, name2,  ))
	playerwin1db = cur.fetchall()
	for row in playerwin1db:
		playerwin1 = (''.join(map(str,row)))
		if playerwin1 == "None":
			playerwin1 = 0
		else:
			playerwin1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=3 AND Spieler1 =?", (name1, name2,  ))
	playerwin2db = cur.fetchall()
	for row in playerwin2db:
		playerwin2 = (''.join(map(str,row)))
		if playerwin2 == "None":
			playerwin2 = 0
		else:
			playerwin2 = int(''.join(map(str,row)))		
	playerwin = playerwin1 + playerwin2
	return (playerwin)

def askplayerloose(name1,name2):	
	"""Anzahl der Niederlagen beider Spieler im direkten Duell abfragen"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=0 AND Spieler2 =?", (name1, name2,  ))
	playerloose1db = cur.fetchall()
	for row in playerloose1db:
		playerloose1 = (''.join(map(str,row)))
		if playerloose1 == "None":
			playerloose1 = 0
		else:
			playerloose1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=0 AND Spieler1 =?", (name1, name2,  ))
	playerloose2db = cur.fetchall()
	for row in playerloose2db:
		playerloose2 = (''.join(map(str,row)))
		if playerloose2 == "None":
			playerloose2 = 0
		else:
			playerloose2 = int(''.join(map(str,row)))		
	playerloose = playerloose1 + playerloose2
	return (playerloose)

def askplayerremi(name1,name2):	
	"""Anzahl der Unentschieden beider Spieler im direkten Duell abfragen"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=1 AND Spieler2 =?", (name1, name2,  ))
	playerremi1db = cur.fetchall()
	for row in playerremi1db:
		playerremi1 = (''.join(map(str,row)))
		if playerremi1 == "None":
			playerremi1 = 0
		else:
			playerremi1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=1 AND Spieler1 =?", (name1, name2,  ))
	playerremi2db = cur.fetchall()
	for row in playerremi2db:
		playerremi2 = (''.join(map(str,row)))
		if playerremi2 == "None":
			playerremi2 = 0
		else:
			playerremi2 = int(''.join(map(str,row)))		
	playerremi = playerremi1 + playerremi2
	return (playerremi)