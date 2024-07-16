#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Der erste der beiden Funktionsblöcke dient dem Auswerten und ablegen der Spielergebnisse.
Es wird anhand der Tore ermittelt welcher Spieler gewonnen hat und anhand dessen werden die Punkte
für die Tagestabelle ermittelt. Für die Ewige Tabelle wird mit Hilfe der ELO Formel und anhand
der Auswertung der vergangenen Spieler, eine Gewinnwahrscheinlichkeit errechnet. Hin Hilfe
dieser Wahrscheinlichkeit wird eine Bewertung des jeweiligen Spielers errechnet und abgelegt. Zudem
dient der Zweite Funktionsblock dem Löschen des Letzten Spiels falls ein Fehler in der Eingabe erfolgte.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
import sys
import time
import cgi
from datetime import datetime


def addgame(player1_name,player1_goals,player2_goals,player2_name):	
	"""Spieldaten entgegennehmen, auswerten und neu in der Datenbank ablegen"""
	# Definieren von Globelen Variablen 
	con = sqlite.connect("Stats.db")
	cur=con.cursor()
	datum=time.strftime("%d.%m.%Y")
	null = 0
	zweitausend = 2000
	Fehler = 0
	
	# Nur für Testzwecke
	#player1_goals = int(4)
	#player2_goals = int(3)
	#player1_name = "Marius"
	#player2_name = "Oliver"
	#gameplace = "Oliver"
	#gameday = int(9)        #später variabel
	
	# Erstellen der Tabellen in der Datenbank falls diese nicht Vorhanden sein Sollten 
	cur.execute('''create table if not exists Games (Datum TEXT,Spieler1 TEXT,Spieler2 TEXT,ToreSpieler1 INT,ToreSpieler2 INT,PunkteSpieler1 INT,PunkteSpieler2 INT,BewertungSpieler1 INT, BewertungSpieler2 INT, TrendSpieler1 INT, TrendSpieler2 INT,Spieltag INT,Spielort TEXT)''')
	cur.execute('''create table if not exists EverTable (Spieler TEXT,Siege INT,Unentschieden INT,Niederlagen INT,Tore INT,Gegentore INT,Tordifferenz INT,Punkte INT,Spielanzahl INT,Bewertung FLOAT, BewertungTrend INT)''')
	cur.execute('''create table if not exists DayTable (Spieler TEXT,Siege INT,Unentschieden INT,Niederlagen INT,Tore INT,Gegentore INT,Tordifferenz INT,Punkte INT,Spielanzahl INT, BewertungTrend INT)''')

	
	# gameday aus Settings holen
	cur.execute ("SELECT (Spieltag) FROM Settings")
	gameday = cur.fetchall()
	for row in gameday:
		gameday = (''.join(map(str,row)))
		if gameday == "None":
			Fehler = 3                # Fehlercode 3 = gameday muss unter Settings definiert werden
		else:
			gameday = int(''.join(map(str,row)))
	# gameplace aus Settings holen
	cur.execute ("SELECT Spielort FROM Settings")
	for gameplacedb in cur:
		gameplace = ("%s") % gameplacedb
	# Maximalen Spieltag aus Games holen
	cur.execute ("SELECT MAX(Spieltag) FROM Games")
	maxSpieltag = cur.fetchall()
	for row in maxSpieltag:
		maxSpieltag = (''.join(map(str,row)))
		if maxSpieltag == "None":
			maxSpieltag = 0
		else:
			maxSpieltag = int(''.join(map(str,row)))
	
	# Prüfen ob eingegebener gameday größer oder gleich maxSpieltag ist - sonst Fehler...
	if maxSpieltag < gameday:
		cur.execute("DROP Table IF EXISTS `DayTable`")
		cur.execute('''create table if not exists DayTable (Spieler TEXT,Siege INT,Unentschieden INT,Niederlagen INT,Tore INT,Gegentore INT,Tordifferenz INT,Punkte INT,Spielanzahl INT, BewertungTrend INT)''')
	else:
		if maxSpieltag > gameday:
			Fehler = 2                          #Fehlercode 2 = maxSpieltag größer gameday
	
	#Zuweisung der Punkte für die Siegerauswertung
	if player1_goals > player2_goals:
		player1_points = 3
		player2_points = 0
		win = player1_name
		SS1 = 1
		SS2 = 0
	
	if player1_goals < player2_goals:
		player1_points = 0
		player2_points = 3
		win = player2_name
		SS1 = 0
		SS2 = 1
	
	if player1_goals == player2_goals:
		player1_points = 1
		player2_points = 1
		win = 0
		SS1 = 0.5
		SS2 = 0.5
	
	# Fehler in der Spielernameneingabe erkennen
	if player1_name == "Spieler 1" or player2_name == "Spieler 2":
		Fehler = 4
		
	if player1_name == player2_name:
		Fehler = 5
	
	# Wenn keine Eingabefehler erkannt werden started das eintragen in die Datenbank 		
	if Fehler == 0:
		# Spielernamen suchen ob in EverTable bereichts vorhanden - sonst erstellen
		cur.execute ("SELECT SUM (Spielanzahl) FROM EverTable WHERE Spieler=?", (player1_name, ))
		countplayS1 = cur.fetchall()
		for row in countplayS1:
			countplayS1 =(''.join(map(str,row)))
			if countplayS1 == "None":
				countplayS1 = 0
				cur=con.cursor()
				cur.execute("INSERT INTO EverTable VALUES (?,?,?,?,?,?,?,?,?,?,?);",(player1_name,null,null,null,null,null,null,null,null,zweitausend,null))
				con.commit()
			else:
				countplayS1 = int(''.join(map(str,row)))
		
		cur.execute ("SELECT SUM (Spielanzahl) FROM EverTable WHERE Spieler=?", (player2_name, ))
		countplayS2 = cur.fetchall()
		for row in countplayS2:
			countplayS2 =(''.join(map(str,row)))
			if countplayS2 == "None":
				countplayS2 = 0
				cur=con.cursor()
				cur.execute("INSERT INTO EverTable VALUES (?,?,?,?,?,?,?,?,?,?,?);",(player2_name,null,null,null,null,null,null,null,null,zweitausend,null))
				con.commit()
			else:
				countplayS2 = int(''.join(map(str,row)))
		
		# Spielernamen suchen ob in DayTable bereichts vorhanden - sonst erstellen
		cur.execute ("SELECT SUM (Spielanzahl) FROM DayTable WHERE Spieler=?", (player1_name, ))
		countplayS1 = cur.fetchall()
		for row in countplayS1:
			countplayS1 =(''.join(map(str,row)))
			if countplayS1 == "None":
				countplayS1 = 0
				cur=con.cursor()
				cur.execute("INSERT INTO DayTable VALUES (?,?,?,?,?,?,?,?,?,?);",(player1_name,null,null,null,null,null,null,null,null,null))
				con.commit()
			else:
				countplayS1 = int(''.join(map(str,row)))
		
		cur.execute ("SELECT SUM (Spielanzahl) FROM DayTable WHERE Spieler=?", (player2_name, ))
		countplayS2 = cur.fetchall()
		for row in countplayS2:
			countplayS2 =(''.join(map(str,row)))
			if countplayS2 == "None":
				countplayS2 = 0
				cur=con.cursor()
				cur.execute("INSERT INTO DayTable VALUES (?,?,?,?,?,?,?,?,?,?);",(player2_name,null,null,null,null,null,null,null,null,null))
				con.commit()
			else:
				countplayS2 = int(''.join(map(str,row)))
				
		# Abfrage und berechnung Bewertung der Spieler Anfang
		cur.execute ("SELECT (Bewertung) FROM Players WHERE Name=?", (player1_name, ))
		RS1db = cur.fetchall()
		for row in RS1db:
			RS1db = float(''.join(map(str,row)))
		
		cur.execute ("SELECT (Bewertung) FROM Players WHERE Name=?", (player2_name, ))
		RS2db = cur.fetchall()
		for row in RS2db:
			RS2db = float(''.join(map(str,row)))
		
		#cur.execute ("SELECT (Bewertung) FROM Players WHERE Name=?", (player1_name, ))
		#for RS1db1 in cur:
		#	RS1db = float(''.join(map(str,RS1db1)))
		#
		#cur.execute ("SELECT (Bewertung) FROM Players WHERE Name=?", (player2_name, ))
		#for RS2db1 in cur:
		#	RS2db = float(''.join(map(str,RS2db1)))
		
		#    cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 1" )
		#	for playerdb in cur:
		#		name_player = ("%s") % playerdb
		
		cur.execute ("SELECT KFaktor FROM Settings")
		K = cur.fetchall()
		for row in K:
			K = int(''.join(map(str,row)))
		
		#Berechnug der Spielerbewertung mit Hilfe der ELO Formel
		K = K + abs(player1_goals - player2_goals)
		ES1 = float(1/(1 + 10**((RS2db - RS1db)/400)))
		ES2 = float(1/(1 + 10**((RS1db - RS2db)/400)))
				
		RS1 = RS1db + K * (SS1 - ES1)
		RS2 = RS2db + K * (SS2 - ES2)
		
		
		cur.execute ("UPDATE Players Set Bewertung=? WHERE Name=?", (RS1,player1_name, ))
		cur.execute ("UPDATE Players Set Bewertung=? WHERE Name=?", (RS2,player2_name, ))
		
		cur.execute ("UPDATE Players Set Bewertung_Spiel=? WHERE Name=?", (RS1db,player1_name, ))
		cur.execute ("UPDATE Players Set Bewertung_Spiel=? WHERE Name=?", (RS2db,player2_name, ))
		
		player1_trend = RS1 - RS1db
		player2_trend = RS2 - RS2db

		RS1 = round(RS1 , 2)
		RS2 = round(RS2 , 2)
		
		# Werte in Games speichern:
		cur=con.cursor()
		con.commit()
		cur=con.cursor()
		cur.execute("INSERT INTO Games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);",(datum,player1_name,player2_name,player1_goals,player2_goals,player1_points,player2_points,RS1,RS2,player1_trend,player2_trend,gameday,gameplace))
	
		# Start Update der EverTable:
		if win == player1_name:
			cur.execute ("UPDATE EverTable Set Siege = Siege + 1 WHERE Spieler=?", (player1_name, ))                  # Update "EverTable" Siege SP1
			cur.execute ("UPDATE EverTable Set Niederlagen = Niederlagen + 1 WHERE Spieler=?", (player2_name, ))      # Update "EverTable" Niederlagen SP2
		if win == player2_name:
			cur.execute ("UPDATE EverTable Set Niederlagen = Niederlagen + 1 WHERE Spieler=?", (player1_name, ))      # Update "EverTable" Niederlagen SP1
			cur.execute ("UPDATE EverTable Set Siege = Siege + 1 WHERE Spieler=?", (player2_name, ))                  # Update "EverTable" Siege SP2
		if win == 0:
			cur.execute ("UPDATE EverTable Set Unentschieden = Unentschieden + 1 WHERE Spieler=?", (player1_name, ))  # Update "EverTable" Unentschieden SP1
			cur.execute ("UPDATE EverTable Set Unentschieden = Unentschieden + 1 WHERE Spieler=?", (player2_name, ))  # Update "EverTable" Unentschieden SP2
	
		cur.execute ("UPDATE EverTable Set Tore = Tore + ? WHERE Spieler=?", (player1_goals, player1_name, ))          # Update "EverTable" Tore SP1
		cur.execute ("UPDATE EverTable Set Tore = Tore + ? WHERE Spieler=?", (player2_goals, player2_name, ))          # Update "EverTable" Tore SP2
		cur.execute ("UPDATE EverTable Set Gegentore = Gegentore + ? WHERE Spieler=?", (player2_goals, player1_name, ))    # Update "EverTable" Gegentore SP1
		cur.execute ("UPDATE EverTable Set Gegentore = Gegentore + ? WHERE Spieler=?", (player1_goals, player2_name, ))    # Update "EverTable" Gegentore SP2
	
		cur.execute ("UPDATE EverTable Set Tordifferenz = Tordifferenz + ? - ? WHERE Spieler=?", (player1_goals, player2_goals, player1_name, ))   # Update "EverTable" Tordifferenz SP1
		cur.execute ("UPDATE EverTable Set Tordifferenz = Tordifferenz + ? - ? WHERE Spieler=?", (player2_goals, player1_goals, player2_name, ))   # Update "EverTable" Tordifferenz SP2
	
		cur.execute ("UPDATE EverTable Set Spielanzahl = Spielanzahl + 1 WHERE Spieler=?", (player1_name, ))           # Update "EverTable" Spielanzahl SP1
		cur.execute ("UPDATE EverTable Set Spielanzahl = Spielanzahl + 1 WHERE Spieler=?", (player2_name, ))           # Update "EverTable" Spielanzahl SP2
	
		cur.execute ("UPDATE EverTable Set Punkte = (Punkte + ?) WHERE Spieler=?", (player1_points, player1_name, ))   # Update "EverTable" Punkte SP1
		cur.execute ("UPDATE EverTable Set Punkte = (Punkte + ?) WHERE Spieler=?", (player2_points, player2_name, ))   # Update "EverTable" Punkte SP2
	
		cur.execute ("UPDATE EverTable Set Bewertung=? WHERE Spieler=?", (RS1,player1_name, ))     # Update "EverTable" Bewertung SP1
		cur.execute ("UPDATE EverTable Set Bewertung=? WHERE Spieler=?", (RS2,player2_name, ))     # Update "EverTable" Bewertung SP2
		
		cur.execute ("SELECT SUM (Spielanzahl) FROM EverTable WHERE Spieler=?", (player1_name, ))

		# Start Update der DayTable:
		if win == player1_name:
			cur.execute ("UPDATE DayTable Set Siege = Siege + 1 WHERE Spieler=?", (player1_name, ))                  # Update "EverTable" Siege SP1
			cur.execute ("UPDATE DayTable Set Niederlagen = Niederlagen + 1 WHERE Spieler=?", (player2_name, ))      # Update "EverTable" Niederlagen SP2
		if win == player2_name:
			cur.execute ("UPDATE DayTable Set Niederlagen = Niederlagen + 1 WHERE Spieler=?", (player1_name, ))      # Update "EverTable" Niederlagen SP1
			cur.execute ("UPDATE DayTable Set Siege = Siege + 1 WHERE Spieler=?", (player2_name, ))                  # Update "EverTable" Siege SP2
		if win == 0:
			cur.execute ("UPDATE DayTable Set Unentschieden = Unentschieden + 1 WHERE Spieler=?", (player1_name, ))  # Update "EverTable" Unentschieden SP1
			cur.execute ("UPDATE DayTable Set Unentschieden = Unentschieden + 1 WHERE Spieler=?", (player2_name, ))  # Update "EverTable" Unentschieden SP2
	
		cur.execute ("UPDATE DayTable Set Tore = Tore + ? WHERE Spieler=?", (player1_goals, player1_name, ))          # Update "EverTable" Tore SP1
		cur.execute ("UPDATE DayTable Set Tore = Tore + ? WHERE Spieler=?", (player2_goals, player2_name, ))          # Update "EverTable" Tore SP2
		cur.execute ("UPDATE DayTable Set Gegentore = Gegentore + ? WHERE Spieler=?", (player2_goals, player1_name, ))    # Update "EverTable" Gegentore SP1
		cur.execute ("UPDATE DayTable Set Gegentore = Gegentore + ? WHERE Spieler=?", (player1_goals, player2_name, ))    # Update "EverTable" Gegentore SP2
	
		cur.execute ("UPDATE DayTable Set Tordifferenz = Tordifferenz + ? - ? WHERE Spieler=?", (player1_goals, player2_goals, player1_name, ))   # Update "EverTable" Tordifferenz SP1
		cur.execute ("UPDATE DayTable Set Tordifferenz = Tordifferenz + ? - ? WHERE Spieler=?", (player2_goals, player1_goals, player2_name, ))   # Update "EverTable" Tordifferenz SP2
	
		cur.execute ("UPDATE DayTable Set Spielanzahl = Spielanzahl + 1 WHERE Spieler=?", (player1_name, ))           # Update "EverTable" Spielanzahl SP1
		cur.execute ("UPDATE DayTable Set Spielanzahl = Spielanzahl + 1 WHERE Spieler=?", (player2_name, ))           # Update "EverTable" Spielanzahl SP2
	
		cur.execute ("UPDATE DayTable Set Punkte = (Punkte + ?) WHERE Spieler=?", (player1_points, player1_name, ))   # Update "EverTable" Punkte SP1
		cur.execute ("UPDATE DayTable Set Punkte = (Punkte + ?) WHERE Spieler=?", (player2_points, player2_name, ))   # Update "EverTable" Punkte SP2
	
	#	cur.execute ("SELECT SUM (Spielanzahl) FROM EverTable WHERE Spieler=?", (player1_name, ))
	
		setdelete = "0"
		cur.execute("UPDATE 'Settings' SET Setgamedelete = ?",(setdelete, ))
	
		con.commit()
		con.close()
		
	# Auswertung Eingabefehler
	if Fehler == 0:
		#text = "Spieldaten werden gespeichert"
		#color = "ADFF2F"   #grün - erfolgreich gespeichert
		messagecode = "50"
	if Fehler == 1:
		#text = "Bitte alle Spieldaten Eingeben!"
		#color = "FF0000"   #rot - Fehler!
		messagecode = "51"
	if Fehler == 2:
		#text = "Spieltag ist zu klein - muss groesser oder gleich %s sein" % (maxSpieltag)
		#color = "FF0000"   #rot - Fehler!
		messagecode = "51"
	if Fehler == 3:
		#text = "Spieltag muss in den Einstellungen definiert sein!"
		#color = "FF0000"   #rot - Fehler!
		messagecode = "51"
	if Fehler == 4:
		#text = "Spieler w&auml;hlen!"
		#color = "FF0000"   #rot - Fehler!
		messagecode = "51"
	if Fehler == 5:
		#text = "Zwei gleiche Spieler eingegeben!"
		#color = "FF0000"   #rot - Fehler!
		messagecode = "51"
		
	return (messagecode)

def deletegame(rowid):	
	"""Das zuletzt eingetragende Spiel aud der Wertung und der Tabelle löschen"""
	con = sqlite.connect("Stats.db")
	cur=con.cursor()
	
	cur.execute ("SELECT Spieler1 FROM Games WHERE rowid=?", (rowid, ))
	player1_name = cur.fetchall()
	for row in player1_name:
		player1_name = (''.join(map(str,row)))
		
	cur.execute ("SELECT Spieler2 FROM Games WHERE rowid=?", (rowid, ))
	player2_name = cur.fetchall()
	for row in player2_name:
		player2_name = (''.join(map(str,row)))
		
	cur.execute ("SELECT ToreSpieler1 FROM Games WHERE rowid=?", (rowid, ))
	player1_goals = cur.fetchall()
	for row in player1_goals:
		player1_goals = int(''.join(map(str,row))
		)
	cur.execute ("SELECT ToreSpieler2 FROM Games WHERE rowid=?", (rowid, ))
	player2_goals = cur.fetchall()
	for row in player2_goals:
		player2_goals = int(''.join(map(str,row)))
	
	cur.execute ("SELECT (Bewertung_Spiel) FROM Players WHERE Name=?", (player1_name, ))
	RS1db = cur.fetchall()
	for row in RS1db:
		RS1db = float(''.join(map(str,row)))
	
	cur.execute ("SELECT (Bewertung_Spiel) FROM Players WHERE Name=?", (player2_name, ))
	RS2db = cur.fetchall()
	for row in RS2db:
		RS2db = float(''.join(map(str,row)))
	
	if player1_goals > player2_goals:
		player1_points = 3
		player2_points = 0
		win = player1_name

	if player1_goals < player2_goals:
		player1_points = 0
		player2_points = 3
		win = player2_name

	if player1_goals == player2_goals:
		player1_points = 1
		player2_points = 1
		win = 0
	
	
	cur.execute ("UPDATE Players Set Bewertung=? WHERE Name=?", (RS1db,player1_name, ))
	cur.execute ("UPDATE Players Set Bewertung=? WHERE Name=?", (RS2db,player2_name, ))
	
	# Start Update der EverTable:
	if win == player1_name:
		cur.execute ("UPDATE EverTable Set Siege = Siege - 1 WHERE Spieler=?", (player1_name, ))                  # Update "EverTable" Siege SP1
		cur.execute ("UPDATE EverTable Set Niederlagen = Niederlagen - 1 WHERE Spieler=?", (player2_name, ))      # Update "EverTable" Niederlagen SP2
	if win == player2_name:
		cur.execute ("UPDATE EverTable Set Niederlagen = Niederlagen - 1 WHERE Spieler=?", (player1_name, ))      # Update "EverTable" Niederlagen SP1
		cur.execute ("UPDATE EverTable Set Siege = Siege - 1 WHERE Spieler=?", (player2_name, ))                  # Update "EverTable" Siege SP2
	if win == 0:
		cur.execute ("UPDATE EverTable Set Unentschieden = Unentschieden - 1 WHERE Spieler=?", (player1_name, ))  # Update "EverTable" Unentschieden SP1
		cur.execute ("UPDATE EverTable Set Unentschieden = Unentschieden - 1 WHERE Spieler=?", (player2_name, ))  # Update "EverTable" Unentschieden SP2
	
	cur.execute ("UPDATE EverTable Set Tore = Tore - ? WHERE Spieler=?", (player1_goals, player1_name, ))          # Update "EverTable" Tore SP1
	cur.execute ("UPDATE EverTable Set Tore = Tore - ? WHERE Spieler=?", (player2_goals, player2_name, ))          # Update "EverTable" Tore SP2
	cur.execute ("UPDATE EverTable Set Gegentore = Gegentore - ? WHERE Spieler=?", (player2_goals, player1_name, ))    # Update "EverTable" Gegentore SP1
	cur.execute ("UPDATE EverTable Set Gegentore = Gegentore - ? WHERE Spieler=?", (player1_goals, player2_name, ))    # Update "EverTable" Gegentore SP2
	
	cur.execute ("UPDATE EverTable Set Tordifferenz = Tordifferenz - ? + ? WHERE Spieler=?", (player1_goals, player2_goals, player1_name, ))   # Update "EverTable" Tordifferenz SP1
	cur.execute ("UPDATE EverTable Set Tordifferenz = Tordifferenz - ? + ? WHERE Spieler=?", (player2_goals, player1_goals, player2_name, ))   # Update "EverTable" Tordifferenz SP2
	
	cur.execute ("UPDATE EverTable Set Spielanzahl = Spielanzahl - 1 WHERE Spieler=?", (player1_name, ))           # Update "EverTable" Spielanzahl SP1
	cur.execute ("UPDATE EverTable Set Spielanzahl = Spielanzahl - 1 WHERE Spieler=?", (player2_name, ))           # Update "EverTable" Spielanzahl SP2
	
	cur.execute ("UPDATE EverTable Set Punkte = (Punkte - ?) WHERE Spieler=?", (player1_points, player1_name, ))   # Update "EverTable" Punkte SP1
	cur.execute ("UPDATE EverTable Set Punkte = (Punkte - ?) WHERE Spieler=?", (player2_points, player2_name, ))   # Update "EverTable" Punkte SP2
	
	RS1db = round(RS1db , 2)
	RS2db = round(RS2db , 2)
		
	cur.execute ("UPDATE EverTable Set Bewertung=? WHERE Spieler=?", (RS1db,player1_name, ))     # Update "EverTable" Bewertung SP1
	cur.execute ("UPDATE EverTable Set Bewertung=? WHERE Spieler=?", (RS2db,player2_name, ))     # Update "EverTable" Bewertung SP2
	

	# Start Update der DayTable:
	if win == player1_name:
		cur.execute ("UPDATE DayTable Set Siege = Siege - 1 WHERE Spieler=?", (player1_name, ))                  # Update "EverTable" Siege SP1
		cur.execute ("UPDATE DayTable Set Niederlagen = Niederlagen - 1 WHERE Spieler=?", (player2_name, ))      # Update "EverTable" Niederlagen SP2
	if win == player2_name:
		cur.execute ("UPDATE DayTable Set Niederlagen = Niederlagen - 1 WHERE Spieler=?", (player1_name, ))      # Update "EverTable" Niederlagen SP1
		cur.execute ("UPDATE DayTable Set Siege = Siege - 1 WHERE Spieler=?", (player2_name, ))                  # Update "EverTable" Siege SP2
	if win == 0:
		cur.execute ("UPDATE DayTable Set Unentschieden = Unentschieden - 1 WHERE Spieler=?", (player1_name, ))  # Update "EverTable" Unentschieden SP1
		cur.execute ("UPDATE DayTable Set Unentschieden = Unentschieden - 1 WHERE Spieler=?", (player2_name, ))  # Update "EverTable" Unentschieden SP2
	
	cur.execute ("UPDATE DayTable Set Tore = Tore - ? WHERE Spieler=?", (player1_goals, player1_name, ))          # Update "EverTable" Tore SP1
	cur.execute ("UPDATE DayTable Set Tore = Tore - ? WHERE Spieler=?", (player2_goals, player2_name, ))          # Update "EverTable" Tore SP2
	cur.execute ("UPDATE DayTable Set Gegentore = Gegentore - ? WHERE Spieler=?", (player2_goals, player1_name, ))    # Update "EverTable" Gegentore SP1
	cur.execute ("UPDATE DayTable Set Gegentore = Gegentore - ? WHERE Spieler=?", (player1_goals, player2_name, ))    # Update "EverTable" Gegentore SP2
	
	cur.execute ("UPDATE DayTable Set Tordifferenz = Tordifferenz - ? + ? WHERE Spieler=?", (player1_goals, player2_goals, player1_name, ))   # Update "EverTable" Tordifferenz SP1
	cur.execute ("UPDATE DayTable Set Tordifferenz = Tordifferenz - ? + ? WHERE Spieler=?", (player2_goals, player1_goals, player2_name, ))   # Update "EverTable" Tordifferenz SP2
	
	cur.execute ("UPDATE DayTable Set Spielanzahl = Spielanzahl - 1 WHERE Spieler=?", (player1_name, ))           # Update "EverTable" Spielanzahl SP1
	cur.execute ("UPDATE DayTable Set Spielanzahl = Spielanzahl - 1 WHERE Spieler=?", (player2_name, ))           # Update "EverTable" Spielanzahl SP2
	
	cur.execute ("UPDATE DayTable Set Punkte = (Punkte - ?) WHERE Spieler=?", (player1_points, player1_name, ))   # Update "EverTable" Punkte SP1
	cur.execute ("UPDATE DayTable Set Punkte = (Punkte - ?) WHERE Spieler=?", (player2_points, player2_name, ))   # Update "EverTable" Punkte SP2
	
	cur.execute ("DELETE FROM `Games` WHERE `rowid` = ?", (rowid, ))
	
	setdelete = 1
	cur.execute("UPDATE 'Settings' SET Setgamedelete = ?",(setdelete, ))

	con.commit()
	con.close()
		
	messagecode = "71"
	return (messagecode)
