#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Header HTML Seite und Linkliste
"""	
__author__ = "Oliver Bleeker"
__version__ = "1.0.1"
__status__ = "Ready"


# Laden der Verwendeten Bibliotheken
import sys
import cgi

# Beginn HTML Ausgabe
print "<!DOCTYPE HTML PUBLIC>"
print "<html>"
print "<head>"
print "<title>TOP</title>"
print """<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">"""
print "</head>"
print """<link rel="stylesheet" type="text/css" href="style.css">"""
print """<div id="top">"""
# Anzeige Überschrift
print """<div id="topinfo">"""
print """<body>"""
print """<a href="/Kicker/cgi-bin/main_home.py" target="mainFrame">Hochschule Bremen Kicker Spieledatenbank</a>"""
print "</body>"
print """</div>"""
# Anzeige der Navigaltionsleiste für die Unterseiten
print """<div id="navi">"""
print """<a href="/Kicker/cgi-bin/main_settings.py" target="mainFrame">Einstellungen</a> | """
print """<a href="/Kicker/cgi-bin/main_games.py" target="mainFrame">Alle Spiele</a> | """
print """<a href="/Kicker/cgi-bin/main_compare.py" target="mainFrame">Spielervergleich</a> | """
print """<a href="/Kicker/cgi-bin/main_ever_table.py" target="mainFrame">Ewige Tabelle</a> | """
print """<a href="/Kicker/cgi-bin/main_gameday.py" target="mainFrame">Spieltag</a></font> """
print """</div>"""
print "</body>"
print "</div>"
print "</html>"""
# Ende HTML Ausgabe