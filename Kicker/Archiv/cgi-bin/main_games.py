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

# Auslesen des Aktuellen Spieltages aus der Datenbank
cur.execute ("SELECT MAX(Spieltag) FROM Games")
maxSpieltag = cur.fetchall()
for row in maxSpieltag:
	maxSpieltag = (''.join(map(str,row)))
	if maxSpieltag == "None":
		maxSpieltag = 0
	else:
		maxSpieltag = int(''.join(map(str,row)))	
	
# Abfragen aller Spiele aus der Datenbank		
cur=con.cursor()
cur.execute("SELECT Datum FROM Games")
datumdb = cur.fetchall()
cur.execute("SELECT Spieltag FROM Games")
gamedaydb = cur.fetchall()
cur.execute("SELECT Spieler1 FROM Games")
player1namedb = cur.fetchall()
cur.execute("SELECT Spieler2 FROM Games")
player2namedb = cur.fetchall()
cur.execute("SELECT ToreSpieler1 FROM Games")
player1goalsdb = cur.fetchall()
cur.execute("SELECT ToreSpieler2 FROM Games")
player2goalsdb = cur.fetchall()
cur.execute("SELECT TrendSpieler1 FROM Games")
player1trend = cur.fetchall()
cur.execute("SELECT TrendSpieler2 FROM Games")
player2trend = cur.fetchall()

# Zählen aller Spiele um diese auf der seite anzuzeigen
cur.execute("SELECT Count(*) FROM `Games`")
countgamesdb = cur.fetchall()
for row in countgamesdb:
	countgames = (''.join(map(str,row)))
	if countgames == "None":
		countgames = 0
	else:
		countgames = int(''.join(map(str,row)))

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
print """<h1>Alle Spiele</h1>"""
print """Anzahl der Spiele: """,countgames,""""""
print "<br>"
print "<br>"
print """<table id="table">"""
print "  <tr>"
print """    <th ALIGN="CENTER" width="10%">Spieltag</th>"""
print """    <th ALIGN="CENTER" width="10%">Datum</th>"""
print """    <th ALIGN="CENTER" width="20%">Spieler 1</th>"""
print """    <th ALIGN="CENTER" width="5%">Trend</th>"""
print """    <th ALIGN="CENTER" width="5%">Tore</th>"""
print """    <th ALIGN="CENTER" width="5%">Tore</th>"""
print """    <th ALIGN="CENTER" width="5%">Trend</th>"""
print """    <th ALIGN="CENTER" width="20%">Spieler 2</th>"""
print "  </tr>"
print """  <tr align="center">"""
print "    <td>"
for row in gamedaydb:
    print (''.join(map(str,row))+"<br>")
print "</td>"

print "    <td>"
for row in datumdb:
    print (''.join(map(str,row))+"<br>")
print "    </td>"

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
print "</div>"
print "</div>"
print "<p>&nbsp;</p>"
print "</html>"

con.close()
# Ende der HTML Ausgabe