from os.path import join
from os import getcwd
from glob import glob
from enum import Enum
from re import findall
import math
import pygame
import numpy as np
import random
import time

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self, size = 4, width=1000, height=800, displayGraphics = True):
        pygame.init()
        self.size = size
        self.displayGraphics = displayGraphics
        self.tileSize = 150
        self.score = 0
        self.step = -1
        
        self.width = max(width, self.size*self.tileSize)
        self.height = max(height, self.size*self.tileSize)
        if self.displayGraphics == True:
            self.backgroundColor = (160,160,160)
            self.screen = self.createScreen()
            self.borderWidth, self.startPoint = self.getBorderAndStartPoint()
            self.font = pygame.font.Font(None, int(self.tileSize*0.5))
            self.drawnTiles = self.drawGrid(borderColor=(0,0,0))
        else:
            print('display graphics: ',self.displayGraphics)

        self.grid = np.zeros((size,size),dtype=int)
        self.numbersDir = self.getNumbers()

        emptySpots = self.getEmptySpots()
        if self.displayGraphics == True:
            self.putNumber(emptySpots,self.step)

    def createScreen(self):
        screen = pygame.display.set_mode( (self.width, self.height) )
        pygame.display.set_caption('2048')
        screen.fill(self.backgroundColor)
        pygame.display.flip()
        return screen
    
    def getBorderAndStartPoint(self):
        startPoint=[(self.width/2)-(self.tileSize*self.size/2),
                    (self.height/2)-(self.tileSize*self.size/2)]
        borderWidth=round(self.tileSize*0.01)
        if borderWidth == 0:
            borderWidth = 1
        
        return borderWidth,startPoint
    
    def drawGrid(self,borderColor):        
        matrix = []
        for tileY in range(self.size):
            for tileX in range(self.size):
                matrix.append((self.startPoint[0]+self.tileSize*tileX,
                               self.startPoint[1]+self.tileSize*tileY))
        matrix = np.array(matrix,dtype=int)

        for position in matrix:
            inner_rect = pygame.Rect(position[0],position[1],self.tileSize,self.tileSize)
            outer_rect = pygame.Rect(position[0] + self.borderWidth, position[1] + self.borderWidth,
                                   self.tileSize - self.borderWidth*2, self.tileSize - self.borderWidth*2)
            pygame.draw.rect(self.screen,borderColor,inner_rect)
            pygame.draw.rect(self.screen,(160,160,160),outer_rect)

        score = self.font.render("Score: "+str(self.score),True,(0,0,0))
        self.screen.blit(score,(self.startPoint[0], self.startPoint[1]-int(self.tileSize*0.35)))
        pygame.display.flip()
        matrix = np.reshape(matrix,(self.size,self.size,2))

        return matrix
    
    def getNumbers(self):
        current_directory = getcwd()
        folder_path = join(current_directory, "numbers")

        pattern = join(folder_path, "*.png")
        numbers = glob(pattern)

        numbersAndDirs = []
        for dir in numbers:
            integer = int(findall(r'\d+', dir)[-1])
            numbersAndDirs.append(dir)
            numbersAndDirs.append(integer)
            
        return numbersAndDirs

    def getEmptySpots(self):
        grid = self.grid
        emptySpots = []

        if self.displayGraphics == True:
            drawnTiles = self.drawnTiles
            for row in range(self.size):
                for element in range(self.size):
                    if grid[row][element] == 0:
                        temp = [drawnTiles[row][element][0],drawnTiles[row][element][1],row,element]
                        emptySpots.append(temp)
        else:
            for row in range(self.size):
                for element in range(self.size):
                    if grid[row][element] == 0:
                        emptySpots.append([0,0,row,element])

        return np.array(emptySpots,dtype=int)
    
    def putNumber(self,emptySpots,step):
        if emptySpots.size != 0:
            choice = random.randint(1,10)
            if choice == 1:
                imageLoad = self.numbersDir[2]
                imageValue = self.numbersDir[3]
            else:
                imageLoad = self.numbersDir[0]
                imageValue = self.numbersDir[1]
            
            if self.displayGraphics == True:
                imageLoad = pygame.image.load(imageLoad)
                imageLoad = pygame.transform.scale(imageLoad, (self.tileSize,self.tileSize))
        
            if step == -1:
                spot = random.sample(range(len(emptySpots)), 2)
                spot = (emptySpots[spot][:2][:2])
            else:
                spot = random.sample(range(len(emptySpots)), 1)
                spot = emptySpots[spot][:2]
            
            if self.displayGraphics == True:
                for position in spot:
                    self.screen.blit(imageLoad,(position[0],position[1]))
                pygame.display.flip()

            for position in spot:
                self.grid[position[2]][position[3]]=imageValue
        self.step+=1

    def updateScreen(self):
        if self.displayGraphics == True:
            for row in range(len(self.grid)):
                for element in range(len(self.grid[row])):
                    outer_rect = pygame.Rect(self.drawnTiles[row][element][0] + self.borderWidth, self.drawnTiles[row][element][1] + self.borderWidth,
                                    self.tileSize - self.borderWidth*2, self.tileSize - self.borderWidth*2)
                    pygame.draw.rect(self.screen,(160,160,160),outer_rect)
                    if self.grid[row][element] in self.numbersDir:
                        index = self.numbersDir.index(self.grid[row][element])
                        imageLoad = self.numbersDir[index-1]
                        imageLoad = pygame.image.load(imageLoad)
                        imageLoad = pygame.transform.scale(imageLoad, (self.tileSize,self.tileSize))
                        self.screen.blit(imageLoad,(self.drawnTiles[row][element][0],self.drawnTiles[row][element][1]))
                        
            pygame.display.flip()

    def moveNonZero(self,row):
        updatedRow=[]
        for element in row:
            if element != 0:
                updatedRow.append(element)
        
        return updatedRow


    def merge(self,updatedRow,getBestAction):
        try:
            for i in range(len(updatedRow) - 1):
                updatedRow = self.moveNonZero(updatedRow)
                if updatedRow[i] == updatedRow[i + 1]:
                    self.score += updatedRow[i]
                    score = self.font.render("Score: "+str(self.score),True,(0,0,0))
                    if getBestAction == False and self.displayGraphics == True:
                        pygame.draw.rect(self.screen,self.backgroundColor,(self.startPoint[0], self.startPoint[1]-int(self.tileSize*0.35),self.width,int(self.tileSize*0.35)))
                        self.screen.blit(score,(self.startPoint[0], self.startPoint[1]-int(self.tileSize*0.35)))
                    updatedRow[i] *= 2
                    updatedRow[i + 1] = 0
        except:
            return updatedRow
        return updatedRow
    
    def slide(self,direction):
        if direction == Direction.LEFT:
            grid = self.grid
            timesRotated = 0
        elif direction == Direction.UP:
            grid = np.rot90(self.grid)
            timesRotated = 1
        elif direction == Direction.RIGHT:
            grid = np.rot90(self.grid,2)
            timesRotated = 2
        elif direction == Direction.DOWN:
            grid = np.rot90(self.grid,3)
            timesRotated = 3

        updatedGrid = []
        for row in grid:
            updatedRow = self.moveNonZero(row)
            updatedRow = self.merge(updatedRow,False)
            while len(updatedRow) != self.size:
                updatedRow.append(0)
            updatedGrid.append(updatedRow)

        updatedGrid = np.array(updatedGrid)
        for i in range(timesRotated):
            updatedGrid = np.rot90(updatedGrid,-1)

        self.grid = updatedGrid

    def move(self,action):
        grid = self.grid
        if action == Direction.LEFT.value:
            self.slide(Direction.LEFT)

        elif action == Direction.UP.value:
            self.slide(Direction.UP)

        elif action == Direction.RIGHT.value:
            self.slide(Direction.RIGHT)

        elif action == Direction.DOWN.value:
            self.slide(Direction.DOWN)

        if (grid == self.grid).all():
            return False
        else:
            if self.displayGraphics == True:
                self.putNumber(self.getEmptySpots(),self.step)
            return True
        
    def checkForMoves(self):
        for row in self.grid:
            if len(set(row)) != len(row):
                for i in range(len(row)):
                    try:
                        if row[i] == row[i+1]:
                            return True
                    except:
                        continue
        for column in np.rot90(self.grid):
            if len(set(column)) != len(column):
                for i in range(len(column)):
                    try:
                        if column[i] == column[i+1]:
                            return True
                    except:
                        continue
        return False

    def play(self,action):
        keepRunning = True

        changed = True

        emptySpots = self.getEmptySpots()

        if self.isGameOver(emptySpots) == False:
            changed = self.move(action)
        else:
            return [False,keepRunning]
        
        if changed and self.displayGraphics == True:
            self.updateScreen()

        return [True,keepRunning]

    def isGameOver(self,emptySpots):
        if emptySpots.size == 0:
            if self.checkForMoves() == True:
                return False
            return True
        else:
            return False


                