# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:33:40 2024

@author: achraf Ben Mariem
"""
K = 40

def berechne_elo(R_Spieler1, R_Spieler2, Tore_Spieler1, Tore_Spieler2, K):
    # Überprüfung der Toranzahl
    #if Tore_Spieler1 > 6 or Tore_Spieler2 > 6:
       #raise ValueError("Die Toranzahl kann nicht größer als 6 sein.")
    # if Tore_Spieler1 == Tore_Spieler2 and Tore_Spieler1 == 6:
    #    raise ValueError("Die Toranzahl kann nicht mit 6:6 enden")
    if Tore_Spieler1 == Tore_Spieler2:
       S_Spieler1 = S_Spieler2 = 0.5
    elif Tore_Spieler1 > Tore_Spieler2:
       S_Spieler1 = 1
       S_Spieler2 = 0
    else:
       S_Spieler1 = 0
       S_Spieler2 = 1

    # Berechnung der erwarteten Punkte
    E_Spieler1 = 1 / (1 + 10 ** ((R_Spieler2 - R_Spieler1) / 400))
    E_Spieler2 = 1 / (1 + 10 ** ((R_Spieler1 - R_Spieler2) / 400))

    # Aktualisierung des K-Faktors
    K = K + abs(Tore_Spieler1 - Tore_Spieler2)

    # Berechnung der neuen ELO-Werte
    R_Spieler1 = R_Spieler1 + K * (S_Spieler1 - E_Spieler1)
    R_Spieler2 = R_Spieler2 + K * (S_Spieler2 - E_Spieler2)

    return R_Spieler1, R_Spieler2

# Test
R_Spieler1 = 1600  # Aktuelle Elo-Bewertung von Spieler 1
R_Spieler2 = 200  # Aktuelle Elo-Bewertung von Spieler 2
Tore_Spieler1 = 6
Tore_Spieler2 = 0 


#try:
R_Spieler1, R_Spieler2 = berechne_elo(R_Spieler1, R_Spieler2, Tore_Spieler1, Tore_Spieler2, K)
print("Neue Elo-Bewertung von Spieler 1:", round(R_Spieler1, 4))
print("Neue Elo-Bewertung von Spieler 2:", round(R_Spieler2, 4))
#except ValueError as e:
    #print(e)
