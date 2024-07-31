#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Auslesen verschiedener Werte der Datenbank
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
con = sqlite.connect("Stats.db")
cur=con.cursor()

def askplayername(number):
	"""Auslesen der Spielernummer"""
	cur.execute ("SELECT Name FROM Players WHERE Nummer=?", (number, ))
	for playernumberdb in cur:
		playername1 = ("%s") % playernumberdb
	return (playername1)
	
def askplayerscore(name1):
	"""Abfrage der Bewertung eines Spielers"""
	cur.execute ("SELECT Bewertung FROM Players WHERE Name=?", (name1, ))
	for askplayerscoredb in cur:
		askplayerscore = ("%s") % askplayerscoredb
	return (askplayerscore)
	
def askplayerpoints(name1):	
	"""Abfrage der Punkte eines Spielers"""
	cur.execute ("SELECT SUM (PunkteSpieler1) FROM Games WHERE Spieler1=?", (name1, ))
	points1db = cur.fetchall()
	for row in points1db:
		points1 =(''.join(map(str,row)))
		if points1 == "None":
			points1 = 0
		else:
			points1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (PunkteSpieler2) FROM Games WHERE Spieler2=?", (name1, ))
	points2db = cur.fetchall()
	for row in points2db:
		points2 = (''.join(map(str,row)))
		if points2 == "None":
			points2 = 0
		else:
			points2 = float(''.join(map(str,row)))
		
	playerpoints = (points1 + points2)
	return (playerpoints)

def askplayergoals(name1):	
	"""Abfrage der Tore eines Spielers"""
	cur.execute ("SELECT SUM (ToreSpieler1) FROM Games WHERE Spieler1=?", (name1, ))
	goals1db = cur.fetchall()
	for row in goals1db:
		goals1 = (''.join(map(str,row)))
		if goals1 == "None":
			goals1 = 0
		else:
			goals1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (ToreSpieler2) FROM Games WHERE Spieler2=?", (name1, ))
	goals2db = cur.fetchall()
	for row in goals2db:
		goals2 = (''.join(map(str,row)))
		if goals2 == "None":
			goals2 = 0
		else:
			goals2 = float(''.join(map(str,row)))
		
	playergoals = (goals1 + goals2)
	return (playergoals)
	
def askplayergoalsagainst(name1):	
	"""Abfrage der Gegentore eines Spielers"""
	cur.execute ("SELECT SUM (ToreSpieler2) FROM Games WHERE Spieler1=?", (name1, ))
	goalsagainst1db = cur.fetchall()
	for row in goalsagainst1db:
		goalsagainst1 = (''.join(map(str,row)))
		if goalsagainst1 == "None":
			goalsagainst1 = 0
		else:
			goalsagainst1 = float(''.join(map(str,row)))
		
	cur.execute ("SELECT SUM (ToreSpieler1) FROM Games WHERE Spieler2=?", (name1, ))
	goalsagainst2db = cur.fetchall()
	for row in goalsagainst2db:
		goalsagainst2 = (''.join(map(str,row)))
		if goalsagainst2 == "None":
			goalsagainst2 = 0
		else:
			goalsagainst2 = float(''.join(map(str,row)))
		
	playergoalsagainst = (goalsagainst1 + goalsagainst2)
	return (playergoalsagainst)
	
def askplayercount(name1):	
	"""Abfrage der Anzahl der gespielten Spiele eines Spielers"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=?", (name1, ))
	playercount1db = cur.fetchall()
	for row in playercount1db:
		playercount1 = (''.join(map(str,row)))
		if playercount1 == "None":
			playercount1 = 0
		else:
			playercount1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=?", (name1, ))
	playercount2db = cur.fetchall()
	for row in playercount2db:
		playercount2 = (''.join(map(str,row)))
		if playercount2 == "None":
			playercount2 = 0
		else:
			playercount2 = int(''.join(map(str,row)))		
	playercount = playercount1 + playercount2
	return (playercount)

def askplayerwin(name1):	
	"""Abfrage der Siege eines Spielers"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=3", (name1, ))
	playerwin1db = cur.fetchall()
	for row in playerwin1db:
		playerwin1 = (''.join(map(str,row)))
		if playerwin1 == "None":
			playerwin1 = 0
		else:
			playerwin1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=3", (name1, ))
	playerwin2db = cur.fetchall()
	for row in playerwin2db:
		playerwin2 = (''.join(map(str,row)))
		if playerwin2 == "None":
			playerwin2 = 0
		else:
			playerwin2 = int(''.join(map(str,row)))		
	playerwin = playerwin1 + playerwin2
	return (playerwin)
	
def askplayerloose(name1):	
	"""Abfrage der Niederlagen eines Spielers"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=0", (name1, ))
	playerloose1db = cur.fetchall()
	for row in playerloose1db:
		playerloose1 = (''.join(map(str,row)))
		if playerloose1 == "None":
			playerloose1 = 0
		else:
			playerloose1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=0", (name1, ))
	playerloose2db = cur.fetchall()
	for row in playerloose2db:
		playerloose2 = (''.join(map(str,row)))
		if playerloose2 == "None":
			playerloose2 = 0
		else:
			playerloose2 = int(''.join(map(str,row)))		
	playerloose = playerloose1 + playerloose2
	return (playerloose)
	
def askplayerremi(name1):	
	"""Abfrage der Unentschieden eines Spielers"""
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler1=? AND PunkteSpieler1=1", (name1, ))
	playerremi1db = cur.fetchall()
	for row in playerremi1db:
		playerremi1 = (''.join(map(str,row)))
		if playerremi1 == "None":
			playerremi1 = 0
		else:
			playerremi1 = int(''.join(map(str,row)))
	
	cur.execute("SELECT Count(*) FROM `Games` WHERE Spieler2=? AND PunkteSpieler2=1", (name1, ))
	playerremi2db = cur.fetchall()
	for row in playerremi2db:
		playerremi2 = (''.join(map(str,row)))
		if playerremi2 == "None":
			playerremi2 = 0
		else:
			playerremi2 = int(''.join(map(str,row)))		
	playerremi = playerremi1 + playerremi2
	return (playerremi)


def maxdiffgameall():	
	"""Abfrage der Tordifferenz zweier Spieler"""	
	cur.execute ("SELECT MAX (ToreSpieler2 - ToreSpieler1) FROM Games")
	maxdiff1db = cur.fetchall()
	for row in maxdiff1db:
		maxdiff1db = (''.join(map(str,row)))
		if maxdiff1db == "None":
			maxdiff1 = 0
		else:
			maxdiff1 = int(''.join(map(str,row)))
			
	cur.execute ("SELECT MAX (ToreSpieler1 - ToreSpieler2) FROM Games")
	maxdiff2db = cur.fetchall()
	for row in maxdiff2db:
		maxdiff2db = (''.join(map(str,row)))
		if maxdiff2db == "None":
			maxdiff2 = 0
		else:
			maxdiff2 = int(''.join(map(str,row)))
	if maxdiff1 > maxdiff2:
		maxdiff = maxdiff1
	if maxdiff1 < maxdiff2:
		maxdiff = maxdiff2
	return (maxdiff)
	

def maxdiffgamedata(maxdiff):
	"""Abfrage der maximalen Tordifferenz zweier Spieler"""			
	cur.execute ("SELECT Spieler1 FROM Games WHERE (ToreSpieler2 - ToreSpieler1) =?",(maxdiff,  ))
	for row in cur:
			player1 =  (''.join(map(str,row)))
	cur.execute ("SELECT Spieler2 FROM Games WHERE (ToreSpieler2 - ToreSpieler1) =?",(maxdiff,  ))
	for row in cur:
			player2 =  (''.join(map(str,row)))
	cur.execute ("SELECT Spieler1 FROM Games WHERE (ToreSpieler1 - ToreSpieler2) =?",(maxdiff,  ))
	for row in cur:
			player1 =  (''.join(map(str,row)))
	cur.execute ("SELECT Spieler2 FROM Games WHERE (ToreSpieler1 - ToreSpieler2) =?",(maxdiff,  ))
	for row in cur:
			player2 =  (''.join(map(str,row)))
			
	cur.execute ("SELECT ToreSpieler1 FROM Games WHERE (ToreSpieler2 - ToreSpieler1) =?",(maxdiff,  ))
	for row in cur:
			playergoals1 =  (''.join(map(str,row)))
	cur.execute ("SELECT ToreSpieler2 FROM Games WHERE (ToreSpieler2 - ToreSpieler1) =?",(maxdiff,  ))
	for row in cur:
			playergoals2 =  (''.join(map(str,row)))
	cur.execute ("SELECT ToreSpieler1 FROM Games WHERE (ToreSpieler1 - ToreSpieler2) =?",(maxdiff,  ))
	for row in cur:
			playergoals1 =  (''.join(map(str,row)))
	cur.execute ("SELECT ToreSpieler2 FROM Games WHERE (ToreSpieler1 - ToreSpieler2) =?",(maxdiff,  ))
	for row in cur:
			playergoals2 =  (''.join(map(str,row)))	
	return (player1,player2,playergoals1,playergoals2)
	