# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:40:27 2024

@author: Achraf Ben Mariem
"""

import subprocess

def display_website_fullscreen():
    # URL der Webseite
    url = "https://www.example.com"  # Ersetzen Sie dies durch die URL der Webseite, die Sie anzeigen möchten

    # Öffnen der URL im Webbrowser im Vollbildmodus
    try:
        browser_path = "/usr/bin/firefox"  # Pfad zu Ihrer Firefox-Exe-Datei
        subprocess.Popen([browser_path, "--kiosk", url])
    except Exception as e:
        print(f"Fehler beim Öffnen des Browsers: {e}")

# Aufrufen der Funktion
display_website_fullscreen()
