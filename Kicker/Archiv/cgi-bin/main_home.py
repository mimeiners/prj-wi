#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Datei: 			Main Home
Autor:			Oliver Bleeker
Funktion:		Anzeige des Posters als PDF Datei
Abhängigkeit:
Beschreibung:	Anzeige einer PDF Datei mit dem Projektposter
"""	

# Laden der Verwendeten Bibliotheken
import sys
import time
import cgi

# Beginn HTML Ausgabe
print "<!DOCTYPE HTML PUBLIC>"
print "<html>"
print "<head>"
print "<title>Aktuell</title>"
print """<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">"""
print "</head>"
print """<link rel="stylesheet" type="text/css" href="style.css">"""
print "<body>"
print """<div id="main">"""
print """<img src="images/Poster JPG.png" alt="Poster">"""
#print """<iframe frameborder="0" src="images/Poster_Projekttisch.pdf" width="100%" height="700"></iframe>"""
print "</div>"
print "<p>&nbsp;</p>"
print "</front>"
print "</font> "
print "</body>"
print "</html>"
# Ende HTML Ausgabe