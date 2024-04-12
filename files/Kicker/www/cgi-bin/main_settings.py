#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Es können Spieler hinzugefügt oder gelöscht werden. Zudem ist es möglich den Spieltag zu ändern wenn
aktuell kein Spiel läuft. Wird aktuell ein Spiel ausgeführt so kann der Punktestand hier korrigiert
werden. Alle eingebebnen Werte werden in dieser Datei abgefragt und an die Funktionsdatei weitergeben wo sie verarbeitet werden.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
import sys
import time
import cgi
import function_settings as function_settings
from datetime import datetime

# Globale Variablen Definieren
con = sqlite.connect("Stats.db")
cur=con.cursor()
tag=time.strftime("%d.%m.%Y")
datum=time.strftime("%d.%m.%Y")	
messagecode = 100


# Alle Zeilen der Spalte Players auslesen	
cur.execute("SELECT Name FROM Players")
players = cur.fetchall()
playerlist = [i for sub in players for i in sub]  # Convert to list from tuple

# gameplace aus Settings holen
cur.execute ("SELECT Spielort FROM Settings")
for gameplacedb in cur:
    gameplace = ("%s") % gameplacedb		

# Spieltag aus Settings holen
cur.execute ("SELECT (Spieltag) FROM Settings")
gameday = cur.fetchall()
for row in gameday:
	gameday = (''.join(map(str,row)))
	if gameday == "None":
		gameday = 0
	else:
		gameday = int(''.join(map(str,row)))

# Maximalen Spieltag aus Games holen
cur.execute ("SELECT MAX(Spieltag) FROM Games")
maxSpieltag = cur.fetchall()
for row in maxSpieltag:
	maxSpieltag = (''.join(map(str,row)))
	if maxSpieltag == "None":
		maxSpieltag = 0
	else:
		maxSpieltag = int(''.join(map(str,row)))		
neuSpieltag = maxSpieltag + 1

# Spielernamen aus aktuellem Spiel laden
cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 1" )
for playerdb in cur:
    NameS1 = ("%s") % playerdb
cur.execute("SELECT Spieler FROM 'GamePlayers' WHERE Nummer = 2" )
for playerdb in cur:
    NameS2 = ("%s") % playerdb
	
# Spielertore aus aktuellem Spiel laden
cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 1" )
for goalsdb in cur:
    ToreS1 = (''.join(map(str,goalsdb)))
cur.execute("SELECT Tore FROM 'GamePlayers' WHERE Nummer = 2" )
for goalsdb in cur:
    ToreS2 = (''.join(map(str,goalsdb)))

#Datenbankverbindung schließen
con.close()


# Eingabe von HTML Seite abfragen. In diesem Fall aus eigener Datei	
form = cgi.FieldStorage()
if form.getvalue("newplayer"):
	playername=form.getvalue('newplayer')
else:
	playername="Neuer Spieler"   # Wenn keine Eingabe dann "Neuer Spieler" um Fehler auszulösen

if form.getvalue("delplayer"):	
	delplayername=form.getvalue('delplayer')
else:
	delplayername = "Spieler Entfernen"

if form.getvalue("gameplaceinput"):
	newgameplace=form.getvalue('gameplaceinput')
else:
	newgameplace = "unchanged"

if form.getvalue("gamedayinput"):
	newgameday=form.getvalue('gamedayinput')
else:
	newgameday = "unchanged"

if form.getvalue("player1_goals_input"):
	player1_goals=form.getvalue('player1_goals_input')
else:
	player1_goals = "unchanged"

if form.getvalue("player2_goals_input"):
	player2_goals=form.getvalue('player2_goals_input')
else:
	player2_goals = "unchanged"
	
#player2_goals = 3

if playername != "Neuer Spieler":
	messagecode = function_settings. addplayer(playername)
if delplayername != "Spieler Entfernen":
	messagecode = function_settings. delplayer(delplayername)
if newgameplace != "unchanged":
	messagecode = function_settings. gameplace(newgameplace)
if newgameday != "unchanged":
	messagecode = function_settings. gameday(newgameday)
if player1_goals != "unchanged" or player2_goals != "unchanged":
	messagecode = function_settings. goalcount(player1_goals,player2_goals)	

	
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
print """<h1>Einstellungen</h1>"""
print "<br>"
print "<br>"
print """<h2>Spieler Bearbeiten</h2>"""
if messagecode == "10" and playername != "Neuer Spieler":
	print """<div id="message-box-fail">"""
	print "Spieler konnte nicht hinzugef&uuml;gt werden!"
	print "</div>"

if messagecode == "11":
	print """<div id="message-box-done">"""
	print "Spieler wurde erfolgreich hinzugef&uuml;gt"
	print "</div>"

if messagecode == "21":
	print """<div id="message-box-done">"""
	print "Spieler wurde erfolgreich gel&ouml;scht"
	print "</div>"

if messagecode != "10" and messagecode != "11" and messagecode != "21":
	print "<br>"
print """  <form method="post" action="main_settings.py" target="_self">"""
print """   <input type="text" name="newplayer" value="Neuer Spieler" style="height: 25px; width: 200px;">"""
print """  <select name="delplayer" style="height: 25px; width: 200px;">"""
print """  <option selected value="Spieler Entfernen">Spieler l&ouml;schen</option>"""
for i in playerlist:
	print '<option value="%s">%s</option>' % (i, i)
print "  </select>"
print "<br>"
print "<br>"
print """   <form name="form2" method="post" action="">"""
print """   <input style="height: 25px; width: 100px;" type="submit" name="submit" value="Speichern"/>"""
print "  </p>"
print "</form>"

print "<br>"
print "<br>"

if ToreS1 == "99" and ToreS2 == "99":
	print """<h2>Spieltag Bearbeiten</h2>"""
	if messagecode == "40":
		print """<div id="message-box-fail">"""
		print "Spieltag wurde nicht ge&auml;dert!"
		print "</div>"
	if messagecode == "41":
		print """<div id="message-box-done">"""
		print "Spieltag wurde erfolgreich ge&auml;dert!"
		print "</div>"
	if messagecode != "40" and messagecode != "41":
		print "<br>"
	print """  <form method="post" action="main_settings.py" target="_self">"""
	print "  <p>"
	print "  Spieltag: "
	print """   <input type="text" size="4" maxlength="3" name="gamedayinput" value=""",neuSpieltag,""">"""
	print "<br>"
	print "<br>"
	print """   <form name="form2" method="post" action="">"""
	print """   <input style="height: 25px; width: 100px;" type="submit" name="submit" value="Speichern"/>"""
	print "  </p>"
	print "</form>"
	print "<br>"
	print "<br>"

if messagecode == "40":
	print """<div id="message-box-fail">"""
	print "Spieltag wurde nicht ge&auml;dert!"
	print "</div>"

if messagecode == "61":
	print """<div id="message-box-done">"""
	print "Spielstand wurde erfolgreich ge&auml;dert!"
	print "</div>"
if messagecode != "61":
	print "<br>"

if ToreS1 != "99" and ToreS2 != "99":
	print """<h2>Spielstand Korregieren</h2>"""
	print "<br>"
	print """  <form method="post" action="main_settings.py" target="_self">"""
	print "  <p>"
	print "Spieler Gr&uuml;n:"
	print "  </select>"
	print """    <select style="height: 25px; width: 40px;" name="player1_goals_input">"""
	print """ 	 <option selected value=""",ToreS1,""">""",ToreS1,"""</option>"""
	print """      <option value="0">0</option>"""
	print """      <option value="1">1</option>"""
	print """      <option value="2">2</option>"""
	print """      <option value="3">3</option>"""
	print """      <option value="4">4</option>"""
	print """      <option value="5">5</option>"""
	print """      <option value="6">6</option>"""
	print "   </select>"
	print "<br>"
	print "Spieler Wei&szlig;:"
	print """   <select style="height: 25px; width: 40px;" name="player2_goals_input">"""
	print """ 	<option selected value=""",ToreS2,""">""",ToreS2,"""</option>"""
	print """      <option value="0">0</option>"""
	print """      <option value="1">1</option>"""
	print """      <option value="2">2</option>"""
	print """      <option value="3">3</option>"""
	print """      <option value="4">4</option>"""
	print """      <option value="5">5</option>"""
	print """      <option value="6">6</option>"""
	print "   </select>"
	print "<br>"
	print "<br>"
	print """   <form name="form2" method="post" action="">"""
	print """   <input style="height: 25px; width: 100px;" type="submit" name="submit" value="Speichern"/>"""
	print "  </p>"
	print "</form>"
print "</div>"
print "</div>"
print" </body>"
print" </html>"
# Ende HTML Ausgabe

