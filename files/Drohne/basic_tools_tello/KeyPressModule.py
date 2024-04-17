# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:04:36 2023

@author: lenna
"""

import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400,400))
    
def getKey(KeyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey=getattr(pygame, "K_{}".format(KeyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans
    
def main():
    # print(getKey())
    if getKey("LEFT"):
        print("Links")
    if getKey("RIGHT"):
        print("Rechts")
    if getKey("ESCAPE"):
        print("ECSAPE")

        
        
if __name__ == "__main__":
    init()
    while True:
        main()
