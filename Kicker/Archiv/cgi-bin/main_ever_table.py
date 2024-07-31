#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Eigenständige HTML Ausgabe der Ewigen Tabelle. Die Tabelle wird hierfür direkt aus der Datenbank
geladen und ausschließlich je nach Sortierungswunsch sortiert.
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

# Globale Variablen Definieren
con = sqlite.connect("Stats.db")
cur=con.cursor()
datum=time.strftime("%d.%m.%Y")	
tag=time.strftime("%d.%m.%Y")
form=cgi.FieldStorage()

# Abfrage der Einstellung Sortierung der Tabelle
cur.execute ("SELECT EwigeTabelleDarstellung FROM Settings")
for tabledisplaydb in cur:
    tabledisplay = ("%s") % tabledisplaydb

# Abfrage der Tabelle sortiert nach Punkten
if tabledisplay == "Punkte":	
	cur.execute("SELECT Spieler FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC" )
	player = cur.fetchall()
	cur.execute("SELECT Siege FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	win = cur.fetchall()
	cur.execute("SELECT Unentschieden FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	draw = cur.fetchall()
	cur.execute("SELECT Niederlagen FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	loose = cur.fetchall()
	cur.execute("SELECT Tore FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	goals = cur.fetchall()
	cur.execute("SELECT Gegentore FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	goalsagainst = cur.fetchall()
	cur.execute("SELECT Tordifferenz FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	goaldifference = cur.fetchall()
	cur.execute("SELECT Punkte FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	points = cur.fetchall()
	cur.execute("SELECT Spielanzahl FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	countgame = cur.fetchall()
	cur.execute("SELECT Bewertung FROM 'EverTable' ORDER BY Punkte DESC, Tordifferenz DESC, Tore DESC")
	rate = cur.fetchall()

# Abfrage der Tabelle sortiert nach Bewertung
if tabledisplay == "Bewertung":
	cur.execute("SELECT Spieler FROM 'EverTable' ORDER BY Bewertung DESC" )
	player = cur.fetchall()
	cur.execute("SELECT Siege FROM 'EverTable' ORDER BY Bewertung DESC")
	win = cur.fetchall()
	cur.execute("SELECT Unentschieden FROM 'EverTable' ORDER BY Bewertung DESC")
	draw = cur.fetchall()
	cur.execute("SELECT Niederlagen FROM 'EverTable' ORDER BY Bewertung DESC")
	loose = cur.fetchall()
	cur.execute("SELECT Tore FROM 'EverTable' ORDER BY Bewertung DESC")
	goals = cur.fetchall()
	cur.execute("SELECT Gegentore FROM 'EverTable' ORDER BY Bewertung DESC")
	goalsagainst = cur.fetchall()
	cur.execute("SELECT Tordifferenz FROM 'EverTable' ORDER BY Bewertung DESC")
	goaldifference = cur.fetchall()
	cur.execute("SELECT Punkte FROM 'EverTable' ORDER BY Bewertung DESC")
	points = cur.fetchall()
	cur.execute("SELECT Spielanzahl FROM 'EverTable' ORDER BY Bewertung DESC")
	countgame = cur.fetchall()
	cur.execute("SELECT Bewertung FROM 'EverTable' ORDER BY Bewertung DESC")
	rate = cur.fetchall()
	
#	cur.execute("SELECT Bewertung FROM 'Players' ORDER BY Bewertung DESC")
#	rate_new = cur.fetchall()
#	cur.execute("SELECT Bewertung_Alt FROM 'Players' ORDER BY Bewertung DESC")
#	rate_old = cur.fetchall()
#	
#	rate_diff = rate_new + rate_old

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
print """<h1>Ewige Tabelle</h1>"""
print """<table id="table">"""
print "  <tr>"
print """    <th ALIGN="CENTER" width="347">Spieler</th>"""
print """    <th ALIGN="CENTER" width="117">Spielanzahl</th>"""
print """    <th ALIGN="CENTER" width="177">Siege</th>"""
print """    <th ALIGN="CENTER" width="117">Remis</th>"""
print """    <th ALIGN="CENTER" width="117">Niederlagen</th>"""
print """    <th ALIGN="CENTER" width="117">Tore</th>"""
print """    <th ALIGN="CENTER" width="117">Gegentore</th>"""
print """    <th ALIGN="CENTER" width="117">Tordifferenz</th>"""
print """    <th ALIGN="CENTER" width="117">Bewertung</th>"""
print """    <th ALIGN="CENTER" width="117">Punkte</th>"""
print "  </tr>"
print """  <tr>"""
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
for row in rate:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in points:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "  </tr>"
print "</table>"

print "</div>"
print "</div>"
print "<p>&nbsp;</p>"
print "</html>"
# Ende der HTML Ausgabe