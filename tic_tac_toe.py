#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 18:42:15 2018

@author: yiqian
"""

import pygame
from pygame.locals import *
import random
import time


WIDTH = 3
HEIGHT = 3
RECsize = 100
WINDOWWIDTH = 700
WINDOWHEIGHT = 480

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 50, 255)
green = (0, 204, 0)
dark = (192, 192, 192)

BGcolor = dark
RECcolor = green
TEXTcolor = black
BORDERcolor = blue

BUTTERcolor = white
BUTTERTEXTcolor = black
MESSAGEcolor = white

BLANK = 0
PlayerX = 13
PlayerO = 11
choice = 0
CONTINUE = 0
DrawGame = 10

Xsize = int((WINDOWWIDTH - (RECsize * WIDTH + (WIDTH - 1)))/2)
Ysize = int((WINDOWHEIGHT - (RECsize * HEIGHT + (HEIGHT - 1)))/2)

def available_step(board):
    return [i for i in range(9) if board[i]==BLANK]

def update_board(board, position, player):
    board[position] = player
    return board

def change_player(player):
    if player == PlayerX:
        return PlayerO
    else:
        return PlayerX
    
    
def drawBoard(board, message):
    DISPLAYSURF.fill(BGcolor)
    if message:
        textSurf, textRect = makeText(message, MESSAGEcolor, BGcolor, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    
    for tilex in range(3):
        for tiley in range(3):
            if board[tilex*3+tiley] != BLANK:
                drawRec(tilex, tiley, board[tilex*3+tiley])
    
    left, top = getLeftTopOfTitle(0, 0)
    width = WIDTH * RECsize
    height = HEIGHT * RECsize
    pygame.draw.rect(DISPLAYSURF, BORDERcolor, ((left-5, top-5), (width+11, height+11)), 4)
    
    DISPLAYSURF.blit(NEW_SURF1, NEW_RECT1)
    DISPLAYSURF.blit(NEW_SURF2, NEW_RECT2)

# draw the rectange in board    
def drawRec(titX, titY, s, adjx=0, adjy=0):
    left, top = getLeftTopOfTitle(titX, titY)
    pygame.draw.rect(DISPLAYSURF, RECcolor, (left+adjx, top+adjy, RECsize, RECsize))
    textSurf = BASIC.render(number2str(s), True, TEXTcolor)
    textRect = textSurf.get_rect()
    textRect.center = left+int(RECsize/2)+adjx, top+int(RECsize/2)+adjy
    DISPLAYSURF.blit(textSurf, textRect)
    
# convert number index to string(X or O)
def number2str(s):
    if s==PlayerX:
        return 'X'
    else:
        return 'O'
    
def getLeftTopOfTitle(X, Y):
    left = Xsize + (X * RECsize) + (X-1)
    top = Ysize + (Y * RECsize) + (Y-1)
    return left, top

# define the surface and rect for text
def makeText(text, color, BGcolor, top, left):
    textSurf = BASIC.render(text, True, color, BGcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def check_win_game(board):
    def check_draw():
        return sum(board)==109
    
    def check_row(player):
        for i in [0, 3, 6]:
            if sum(board[i:i+3]) == 3 * player:
                return player
            
    def check_col(player):
          for i in range(3):
              if sum(board[i::3]) == 3 * player:
                  return player
    
    def check_dia(player):
        if (sum(board[0::4]) == 3*player) or (sum(board[2:7:2]) == 3*player):
            return player
    
    for player in [PlayerX, PlayerO]:
        if any([check_row(player), check_col(player), check_dia(player)]):
            return player
    
    return DrawGame if check_draw() else CONTINUE

# get click position
def getSpotClicked(x, y):
    for i in range(3):
        for j in range(3):
            left, top = getLeftTopOfTitle(i, j)
            tileRect = pygame.Rect(left, top, RECsize, RECsize)
            if tileRect.collidepoint(x, y):
                return (i, j)
    return None
            
        
# game strategy random 
def random_choice(board, depth):
    global choice
    
    steps = []
    
    for i in range(len(board)):
        if board[i] != PlayerX and board[i] != PlayerO:
            steps.append(i)
    ranIndex = random.randint(0, len(steps)-1)
    choice = steps[ranIndex]
    return None
        
                
def main():
    global BASIC
    global DISPLAYSURF, NEW_SURF1, NEW_RECT1, NEW_SURF2, NEW_RECT2
    
    pygame.init()
    GameOver = False
    TurnX = True
    ModeAI = False
    massage = "Tic Tac Toe"
    #Basic interface
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Yi Qian's Tic Toc Tac")
    BASIC = pygame.font.Font(None, 20)
    NEW_SURF1, NEW_RECT1 = makeText("AI vs AI", TEXTcolor, RECcolor, WINDOWWIDTH-120, WINDOWHEIGHT-60)
    NEW_SURF2, NEW_RECT2 = makeText("Human vs AI (unable)", TEXTcolor, RECcolor, WINDOWWIDTH-300, WINDOWHEIGHT-60)
    board = [BLANK] * 9
    drawBoard(board, massage)
    pygame.display.update()
    print(1)
    
    while True:
        c = None
        #click 
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                c = getSpotClicked(event.pos[0], event.pos[1])
                if not c and NEW_RECT1.collidepoint(event.pos):
                    print("init board")
                    board = [BLANK]*9
                    GameOver = False
                    message = "AI vs AI"
                    drawBoard(board, message)
                    pygame.display.update()
                    ModeAI = True     
                    
                if not c and NEW_RECT2.collidepoint(event.pos):
                    board = [BLANK]*9
                    GameOver = False
                    message = "Human vs AI"
                    drawBoard(board, massage)
                    pygame.display.update()
                    ModeAI = False
        
        if ModeAI:
            print("AI2AI")
            pro = ""
            count = 0
            player = PlayerX
            while count<9:
                random_choice(board, 0)
                print(board, choice)
                update_board(board, choice, player)
                drawBoard(board, massage)
                pygame.display.update()
                i = int(choice/3)
                j = int(choice%3)
                count+=1
                pro = pro+'R'+str(count)+number2str(player)+':('+ str(i)+','+str(j)+')|| '
                if player==PlayerX:
                    player=PlayerO
                else:
                    player=PlayerX
            c = None
            ModeAI = False
                
            """
                    if not ModeAI:
                        NextStep = board_step(*c)
                        update_board(board, NextStep, PlayerX)
                        drawBoard(board, message)
                        pygame.display.update()
                        # change strategy here random or minmax
                        random(board, 0)
                        update_board(board, choice, PlayerO)
            """
            
            result = check_win_game(board)
            GameOver = (result != CONTINUE)
            
            if result == PlayerX:
                massage = "Player X win!  " + pro
            elif result == PlayerO:
                massage = "Player O win!  " + pro
            elif result == DrawGame:
                massage = "Draw Game  " + pro
            
            drawBoard(board, massage)
            pygame.display.update()

if __name__== "__main__":
    main()
                
                
                
    
    