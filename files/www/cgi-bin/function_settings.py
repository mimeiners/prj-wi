#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Einstellungen können über die HTML Seite geändert werden. Diese Änderungen werden hier in der Datenbank abgelegt.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
import sys
import time
import cgi

# Definieren von Globelen Variablen 
con = sqlite.connect("Stats.db")
cur=con.cursor()

cur.execute('''create table if not exists "Players" (Datum TEXT,Name TEXT,Nummer INTEGER,Bewertung FLOAT,Bewertung_Alt FLOAT)''')

def addplayer(playername):	
	"""Funktion: Spieler hinzufügen wenn ein Name eingegeben worden ist und dieser noch nicht vorhanden ist"""
	playerpoints = "2000"
	playerpointsold = "2000"
	playerpointsgameday = "2000"	
	datum=time.strftime("%d.%m.%Y")	
	if playername != "Neuer Spieler":
		knownnumberdb = 0
		cur=con.cursor()
		cur.execute("SELECT Nummer FROM Players WHERE Name=?", (playername, ))
		for knownplayerdb in cur:
			knownnumberdb = ("%s") % knownplayerdb 
		knownplayernumber = int(knownnumberdb)
	else:
		knownplayernumber = 0
	if playername != "Neuer Spieler" and knownplayernumber == 0:
		cur.execute("SELECT Nummer FROM `Players`")
		for playerdb in cur:
			numberdb = ("%s") % playerdb 
		playernumber = int(numberdb)+1
		playernumberdb = ("%s") % playernumber
		cur=con.cursor()
		cur.execute("INSERT INTO Players VALUES (?,?,?,?,?,?);",(datum,playername,playernumberdb,playerpoints,playerpointsold,playerpointsgameday))
		con.commit()
		messagecode = "11"
	else:
		messagecode = "10"	
	return (messagecode)

def delplayer(delplayername):	
	"""Funktion: Spieler Löschen"""
	if delplayername != "Spieler Entfernen":
		cur.execute("DELETE FROM Players WHERE Name =?", (delplayername, ))
		con.commit()
		messagecode = "21"
	else:
		messagecode = "20"
	return (messagecode)

def gameplace(newgameplace):	
	"""Funktion: Spielort ändern"""
	# gameplace aus Settings holen
	cur=con.cursor()
	cur.execute ("SELECT Spielort FROM Settings")
	for gameplacedb in cur:
		gameplace = ("%s") % gameplacedb
	if newgameplace != gameplace:
		cur=con.cursor()
		cur.execute("UPDATE 'Settings' SET Spielort = ?",(newgameplace, ))
		con.commit()
		messagecode = "31"
	else:
		messagecode = "30"
	return (messagecode)
	
def gameday(newgameday):	
	"""Funktion: Spieltag ändern"""
	# gameplace aus Settings holen
	cur=con.cursor()
	cur.execute ("SELECT (Spieltag) FROM Settings")
	gameday = cur.fetchall()
	for row in gameday:
		gameday = (''.join(map(str,row)))
		if gameday == "None":
			gameday = 0
		else:
			gameday = int(''.join(map(str,row)))
	if newgameday != "unchanged" and newgameday != gameday:
		cur=con.cursor()
		cur.execute("UPDATE 'Settings' SET Spieltag = ?",(newgameday, ))
		con.commit()
		messagecode = "41"
	else:
		messagecode = "40"
	return (messagecode)

def goalcount(player1_goals,player2_goals):	
	cur=con.cursor()
	cur.execute ("UPDATE GamePlayers Set Tore = ? WHERE Nummer=1",(player1_goals, ))
	cur.execute ("UPDATE GamePlayers Set Tore = ? WHERE Nummer=2",(player2_goals, ))

	con.commit()
	messagecode = "61"
	return (messagecode)	
	
