#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Um einen direkten Vergleich zwischen zwei Spielern zu erstellen, wird nach Eingabe zweier Spielernamen,
nach allen Spielen gesucht in denen ein direktes Duell stattgefunden hat. Diese werden dann auf einer HTML Seite 
tabellarisch dargestellt. Das Suchen und zusammenstellen der Daten wird in der Datei function_compace.py ausgeführt.
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"

# Laden der Verwendeten Bibliotheken
import sqlite3 as sqlite
import sys
import time
import cgi
import function_compare as function
from datetime import datetime

# Globale Variablen Definieren
con = sqlite.connect("Stats.db")
cur=con.cursor()
datum=time.strftime("%d.%m.%Y")	
tag=time.strftime("%d.%m.%Y")
Fehler = 0
text = " "

# Alle Zeilen der Spalte Players auslesen	
cur.execute("SELECT Name FROM Players")
players = cur.fetchall()
playerlist = [i for sub in players for i in sub]  # Convert to list from tuple

#Datenbankverbindung schließen
con.close()

# Eingabe von HTML Seite abfragen. In diesem Fall aus eigener Datei	
form = cgi.FieldStorage()
if form.getvalue("player1_name"):
    playername1db=form.getvalue('player1_name')
else:
	playername1db = "Spieler 1"
	Fehler = 1

if form.getvalue("player2_name"):
    playername2db=form.getvalue('player2_name')
else:
	playername2db = "Spieler 2"
	Fehler = 1

if playername1db == "Spieler 1" or playername2db == "Spieler 2":
	Fehler = 4
if playername1db == "Spieler 1" and playername2db == "Spieler 2":
	Fehler = 1	
if playername1db == playername2db:
	Fehler = 5	

# Wenn keine falschen eingaben getätigt worden sind, werden die Namen in die Funktion function_compare übergeben. Diese vergleicht alle Spiele der angefragten Namen miteinander
if playername1db != "Spieler 1" and playername2db != "Spieler 2":	
	playerpoints1db = function. askplayerpoints(playername1db,playername2db)
	playergoals1db = function. askplayergoals(playername1db,playername2db)
	playergoalsagainst1db = function. askplayergoalsagainst(playername1db,playername2db)
	playercount1db = function. askplayercount(playername1db,playername2db)
	playerwin1db = function. askplayerwin(playername1db,playername2db)
	playerloose1db = function. askplayerloose(playername1db,playername2db)
	playerremi1db = function. askplayerremi(playername1db,playername2db)
	playerscore1db = function. askplayerscore(playername1db,playername2db)
	goaldifferent1 = playergoals1db - playergoalsagainst1db
	
	playerpoints2db = function. askplayerpoints(playername2db,playername1db)
	playergoals2db = function. askplayergoals(playername2db,playername1db)
	playergoalsagainst2db = function. askplayergoalsagainst(playername2db,playername1db)
	playercount2db = function. askplayercount(playername2db,playername1db)
	playerwin2db = function. askplayerwin(playername2db,playername1db)
	playerloose2db = function. askplayerloose(playername2db,playername1db)
	playerremi2db = function. askplayerremi(playername2db,playername1db)
	playerscore2db = function. askplayerscore(playername2db,playername1db)
	goaldifferent2 = playergoals2db - playergoalsagainst2db
else:
	playerpoints1db = 0
	playergoals1db = 0
	playergoalsagainst1db = 0
	playercount1db = 0
	playerwin1db = 0
	playerloose1db = 0
	playerremi1db = 0
	playerscore1db = 0
	goaldifferent1 = 0

	playerpoints2db = 0
	playergoals2db = 0
	playergoalsagainst2db = 0
	playercount2db = 0
	playerwin2db = 0
	playerloose2db = 0
	playerremi2db = 0
	playerscore2db = 0
	goaldifferent2 = 0

# Debug: Direkte Anzeige der Auswertung im Terminal 
#print "Spielername:	" + str(playername1db)
#print "Punkte:		" + str(playerpoints1db)
#print "Tore:		" + str(playergoals1db)
#print "Gegentore:	" + str(playergoalsagainst1db)
#print "Tordifferenz:	" + str(goaldifferent1)
#print "Spielanzahl:	" + str(playercount1db)
#print "Siege:		" + str(playerwin1db)
#print "Niederlagen:	" + str(playerloose1db)
#print "Remis:		" + str(playerremi1db)
#print "Bewertung:	" + str(playerscore1db)
#	
#
#print "Spielername:	" + str(playername2db)
#print "Punkte:		" + str(playerpoints2db)
#print "Tore:		" + str(playergoals2db)
#print "Gegentore:	" + str(playergoalsagainst2db)
#print "Tordifferenz:	" + str(goaldifferent2)
#print "Spielanzahl:	" + str(playercount2db)
#print "Siege:		" + str(playerwin2db)
#print "Niederlagen:	" + str(playerloose2db)
#print "Remis:		" + str(playerremi2db)
#print "Bewertung:	" + str(playerscore2db)

# Fehlercode für Fehleranzeige festlegen
if Fehler == 4:
    text = "Nur ein Spieler ausgew&auml;hlt! "
if Fehler == 1:
    text = "Bitte Spieler w&auml;hlen!"
if Fehler == 5:
    text = "Zwei gleiche Spieler ausgew&auml;hlt!"

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
print """<h1>Direkter Spielervergleich</h1>"""
if Fehler == 5 or Fehler == 4:
	print """<div id="message-box-fail">"""
	print text
	print "</div>"
else:
	print """<div id="message-box">"""
	print text
	print "<br>"
	print "</div>"

print "<br>"	
print """<form method="post" action="main_compare.py" target="mainFrame">""" 
print "<p>" 
print """  <select style="height: 25px; width: 100px;" name="player1_name">"""
print """  <option selected value="Spieler 1">Spieler 1</option>"""
for i in playerlist:
	print '<option value="%s">%s</option>' % (i, i)
	
print "  </select>"
print """  <select style="height: 25px; width: 100px;" name="player2_name">"""
print """  <option selected value="Spieler 2">Spieler 2</option>"""
for i in playerlist:
	print '<option value="%s">%s</option>' % (i, i)

print "  </select>"

print """<form  name="form2" method="post" action="">"""
print """   <input style="height: 25px; width: 100px;" value="Vergleichen"  type="submit" name="submit"/>"""
print "  </p>"
print "  <p>&nbsp;</p>"
print "</form>"

	
print "<br>"
print "<br>"
print """<table id="table_compare">"""
print "  <tr>"
print"""     <th width="33%"></th>"""
print"""     <th width="33%">""",playername1db,"""</th>"""
print"""     <th width="33%">""",playername2db,"""</th>"""
print"   </tr>"

print "  <tr>"
print "    <td>"
print "Spiele"
print "    </td>"
print "    <td colspan= 2>"
print playercount1db
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Siege"
print "    </td>"
print "    <td>"
print playerwin1db
print "    </td>"
print "    <td>"
print playerwin2db
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Remis"
print "    </td>"
print "    <td colspan= 2>"
print playerremi1db
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Niederlagen"
print "    </td>"
print "    <td>"
print playerloose1db
print "    </td>"
print "    <td>"
print playerloose2db
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Tore"
print "    </td>"
print "    <td>"
print playergoals1db
print "    </td>"
print "    <td>"
print playergoals2db
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Tordifferenz"
print "    </td>"
print "    <td>"
print goaldifferent1
print "    </td>"
print "    <td>"
print goaldifferent2
print "	   </td>"
print "    </tr>"

print "  <tr>"
print "    <td>"
print "Punkte"
print "    </td>"
print "    <td>"
print playerpoints1db
print "    </td>"
print "    <td>"
print playerpoints2db
print "	   </td>"
print "    </tr>"

print "</table>"
print "</div>"
print "</div>"
print" </body>"
print" </html>"
# Ende der HTML Ausgabe

