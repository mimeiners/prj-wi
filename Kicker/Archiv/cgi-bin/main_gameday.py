#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Eingeben der Spieldaten. Spielernamen und Ergebnis werden in die Datei function_add_game übergeben
und dort ausgewertet und in der Datenbank abgelegt. Zudem werden die Tagestabelle und die Spiele des
aktuellen Spieltages tabellarisch angezeigt.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
import sys
import time
import cgi
import function_add_game
from datetime import datetime

# Globale Variablen Definieren
con = sqlite.connect("Stats.db")
cur=con.cursor()
form = cgi.FieldStorage()
datum=time.strftime("%d.%m.%Y")	
tag=time.strftime("%d.%m.%Y")
messagecode = 100
Fehler = 0

# Abfrage der Eingabefelder HTML
if form.getvalue("player1_name"):
	player1_name=form.getvalue('player1_name')
	if player1_name == "Spieler 1":
		Fehler = 1
else:
	player1_name = "Spieler 1"

if form.getvalue("player2_name"):
	player2_name=form.getvalue('player2_name')
	if player2_name == "Spieler 2":
		Fehler = 1
else:
	player2_name = "Spieler 2"

if player1_name == player2_name:
	Fehler = 2

# Abfrage der Checkbox für das Löschen eines Spiels
if form.getvalue("checkbox1"):
	checkbox1= "delete"
else:
	checkbox1= "null"	

# Abfrage der Checkbox für das Abbrechen eines Spiels
if form.getvalue("checkbox2"):
	checkbox2= "delete"
else:
	checkbox2= "null"
	
# Debug
#player1_name = "Oliver B."
#player2_name = "Daniel N."
#player1_goals = 2
#player1_goals = 1
#checkbox1 = "delete"
#checkbox2 = "delete"

# Wenn keine Eingabefehler erkannt worden sind werden die Spielernamen in die Datenbank geschrieben
if Fehler == 0 and player1_name != "Spieler 1" and player2_name != "Spieler 2":
	cur.execute("UPDATE 'GamePlayers' SET Spieler = ? WHERE Nummer=1",(player1_name, ))
	cur.execute("UPDATE 'GamePlayers' SET Spieler = ? WHERE Nummer=2",(player2_name, ))
	cur.execute("UPDATE 'GamePlayers' SET Tore = 0 WHERE Nummer=1")
	cur.execute("UPDATE 'GamePlayers' SET Tore = 0 WHERE Nummer=2")
	con.commit()

# Abfrage Checkbox1 zum löschen des letzten Spiels
if checkbox1 == "delete":
	# Maximalen Zeilenwert aus den Spielen Laden
	cur.execute ("SELECT MAX (rowid) FROM Games")
	id = cur.fetchall()
	for row in id:
		id = (''.join(map(str,row)))
		if id == "None":
			id = 0
		else:
			id = int(''.join(map(str,row)))
	messagecode = function_add_game. deletegame(id)

# Abfrage Checkbox2 zum beenden des aktuellen spiels
if checkbox2 == "delete":
	cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=1")
	cur.execute ("UPDATE GamePlayers Set Tore=99 WHERE Nummer=2")
	cur.execute ("UPDATE GamePlayers Set Spieler='Spieler1' WHERE Nummer=1")
	cur.execute ("UPDATE GamePlayers Set Spieler='Spieler2' WHERE Nummer=2")
	con.commit()


# Alle Zeilen der Spalte Players auslesen
cur.execute("SELECT Name FROM Players")
players = cur.fetchall()
playerlist = [i for sub in players for i in sub]  # Convert to list from tuple

# Werte für die Tagestabelle aus der Datenbank laden. Hier nach Punkten Sortiert
cur.execute("SELECT Spieler FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC" )
player = cur.fetchall()
cur.execute("SELECT Siege FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
win = cur.fetchall()
cur.execute("SELECT Unentschieden FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
draw = cur.fetchall()
cur.execute("SELECT Niederlagen FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
loose = cur.fetchall()
cur.execute("SELECT Tore FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
goals = cur.fetchall()
cur.execute("SELECT Gegentore FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
goalsagainst = cur.fetchall()
cur.execute("SELECT Tordifferenz FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
goaldifference = cur.fetchall()
cur.execute("SELECT Punkte FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
points = cur.fetchall()
cur.execute("SELECT Spielanzahl FROM 'DayTable' ORDER BY Punkte DESC, Tore DESC, Tordifferenz DESC")
countgame = cur.fetchall()

# Laden der Tore des aktuellen Spiels
cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 1" )
for goalsdb in cur:
    player1_go = (''.join(map(str,goalsdb)))
cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 2" )
for goalsdb in cur:
    player2_go = (''.join(map(str,goalsdb)))

# Maximalen Spieltag aus der Datenbank lesen
cur.execute ("SELECT MAX(Spieltag) FROM Games")
maxSpieltag = cur.fetchall()
for row in maxSpieltag:
	maxSpieltag = (''.join(map(str,row)))
	if maxSpieltag == "None":
		maxSpieltag = 0
	else:
		maxSpieltag = int(''.join(map(str,row)))	

# Spieltag aus der Datenbank lesen
cur.execute("SELECT Spieltag FROM `Settings`")
gamedaydb = cur.fetchall()
for row in gamedaydb:
	gameday =(''.join(map(str,row)))
	if gameday == "None":
		gameday = maxSpieltag
	else:
		gameday = (''.join(map(str,row)))

# Ablegen ob ein Spiel gelöscht worden ist, da jeweils nur das letzte Spiel gelöscht werden kann		
cur.execute("SELECT Setgamedelete FROM `Settings`")
setdeletedb = cur.fetchall()
for row in setdeletedb:
	setdelete =(''.join(map(str,row)))
	if setdelete == "None":
		setdelete = "1"
	else:
		setdelete = (''.join(map(str,row)))
		

# Werte für die Tabelle aller Spiele des Spieltages aus der Datenbank laden
cur=con.cursor()
cur.execute("SELECT Datum FROM Games WHERE Spieltag=?", (maxSpieltag, ))
datumdb = cur.fetchall()
cur.execute("SELECT Spieler1 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player1namedb = cur.fetchall()
cur.execute("SELECT Spieler2 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player2namedb = cur.fetchall()
cur.execute("SELECT ToreSpieler1 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player1goalsdb = cur.fetchall()
cur.execute("SELECT ToreSpieler2 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player2goalsdb = cur.fetchall()
cur.execute("SELECT TrendSpieler1 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player1trend = cur.fetchall()
cur.execute("SELECT TrendSpieler2 FROM Games WHERE Spieltag=?", (maxSpieltag, ))
player2trend = cur.fetchall()
cur.execute("SELECT Count(*) FROM `Games`")
countgames = cur.fetchall()


#Datenbankverbindung schließen
con.close()

# Beginn der HTML Ausgabe
print "<!DOCTYPE HTML PUBLIC>"
print "<html>"
print "<head>"
print "<title>Aktuell</title>"
print """<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">"""
print "</head>"
print """<link rel="stylesheet" type="text/css" href="style.css">"""
print """<div id="main">"""
print """<div id="center">"""
print """<h1>Spieltag</h1>"""
print """Aktueller Spieltag: """,maxSpieltag,""" """
# Abrage von Eingabefehlern und darstellung auf der Webseite
if Fehler == 1:
	print "<br>"
	print """<div id="message-box-fail">"""
	print "Spieler Ausw&auml;hlen!"
	print "<br>"
	print "</div>"
elif Fehler == 2:
	print "<br>"
	print """<div id="message-box-fail">"""
	print "Unterschiedliche Spieler Ausw&auml;hlen!"
	print "<br>"
	print "</div>"
elif player1_go != "99" and player2_go != "99":
	print "<br>"
	print """<div id="message-box-done">"""
	print """Spiel Gestartet"""
	print "<br>"
	print "</div>"
elif messagecode == "71" and setdelete == "1":
	print """<div id="message-box-done">"""
	print "Spiel wurde erfolgreich gel&ouml;scht!"
	print "<br>"
	print "Es kann nur ein Spiel gel&ouml;scht werden!"
	print "</div>"
else:
	print "<br>"
	print "<br>"
# Wenn aktuell kein Spiel angefangen wurde, die Eingabe der Spielernamen ermöglichen um ein Spiel zu starten
if player1_go == "99" and player2_go == "99":
	print """<h2>Neues Spiel<h2>"""
	print "<br>"
	print """<form method="post" action="main_gameday.py" target="_self">""" 
	print "<p>" 
	print """  <select style="height: 50px; width: 160px;" name="player1_name">"""
	print """  <option selected value="Spieler 1">Spieler Gr&uuml;n</option>"""
	for i in playerlist:
		print '<option value="%s">%s</option>' % (i, i)
	print "  </select>"
	print """  <select style="height: 50px; width: 160px;" name="player2_name">"""
	print """  <option selected value="Spieler 2">Spieler Wei&szlig;</option>"""
	for i in playerlist:
		print '<option value="%s">%s</option>' % (i, i)
	print "  </select>"
	print "<br>"
	print "<br>"
	print """<form name="form2" method="post" action="">"""
	print """   <input style="height: 40px; width: 150px;" value="Spiel Starten"  type="submit" name="submit"/>"""
	print "  </p>"
	print "  <p>&nbsp;</p>"
	print "</form>"
if player1_go != "99" and player2_go != "99":
	print "<br>"
	print """<form method="post" action="main_gameday.py" target="_self">""" 
	print """   <input type="checkbox" name="checkbox2" value="checkbox2">"""
	print "Spiel Abbrechen"
	print "<br>"
	print "<br>"
	print """   <input style="height: 25px; width: 100px;" value="Best&auml;tigen"  type="submit" name="submit"/>"""
	print " </form>"
	print "<br>"
	print "<br>"
# Anzeige der Tagestabelle
print """<h2>Tagestabelle<h2>"""
print """<table id="table">"""
print "  <tr>"
print """    <th ALIGN="CENTER" width="10%">Spieler</th>"""
print """    <th ALIGN="CENTER" width="5%">Spielanzahl</th>"""
print """    <th ALIGN="CENTER" width="5%">Siege</th>"""
print """    <th ALIGN="CENTER" width="5%">Remis</th>"""
print """    <th ALIGN="CENTER" width="5%">Niederlagen</th>"""
print """    <th ALIGN="CENTER" width="5%">Tore</th>"""
print """    <th ALIGN="CENTER" width="5%">Gegentore</th>"""
print """    <th ALIGN="CENTER" width="5%">Tordifferenz</th>"""
print """    <th ALIGN="CENTER" width="5%">Punkte</th>"""
print "  </tr>"
print """  <tr align="center">"""
print "    <td>"
for row in player:
    print (''.join(map(str,row))+"<br>")
print "    </td>"

print "    <td>"
for row in countgame:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in win:
    print (''.join(map(str,row))+"<br>")
print "   </td>"

print "    <td>"
for row in draw:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in loose:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in goals:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in goalsagainst:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in goaldifference:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in points:
    print (''.join(map(str,row))+"<br>")
print "</td>"


print "  </tr>"
print "</table>"

# Anzeige der Tabelle aller Spiele

print "<br>"
print """<h2>Spiele des Tages</h2>"""
print """<table id="table"">"""
print "  <tr>"
print """    <th ALIGN="CENTER" width="20%">Spieler 1</th>"""
print """    <th ALIGN="CENTER" width="5%">Trend</th>"""
print """    <th ALIGN="CENTER" width="5%">Tore</th>"""
print """    <th ALIGN="CENTER" width="5%">Tore</th>"""
print """    <th ALIGN="CENTER" width="5%">Trend</th>"""
print """    <th ALIGN="CENTER" width="20%">Spieler 2</th>"""
print "  </tr>"
print """  <tr align="center">"""
print "    <td>"
for row in player1namedb:
    print (''.join(map(str,row))+"<br>")
print "   </td>"

print "    <td>"
for row in player1trend:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in player1goalsdb:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in player2goalsdb:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in player2trend:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in player2namedb:
    print (''.join(map(str,row))+"<br>")
print "</td>"
print "  </tr>"
print "</table>"
print "<br>"
print "<br>"


# Möglichkeit zum Löschen eines Spieles wenn dies noch nicht ausgeführt worden ist
if messagecode != "71" and setdelete == "0":
	print "<br>"
	print """<form method="post" action="main_gameday.py" target="_self">""" 
	print """   <input type="checkbox" name="checkbox1" value="checkbox1">"""
	print "Letztes Spiel L&ouml;schen"
	print "<br>"
	print "<br>"
	print """   <input style="height: 25px; width: 100px;" value="Best&auml;tigen"  type="submit" name="submit"/>"""
	print " </form>"
print "</div>"
print "<p>&nbsp;</p>"
print "</div>"
print "</html>"
# Ende HTML Ausgabe