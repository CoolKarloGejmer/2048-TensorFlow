from os.path import join
from os import getcwd
from glob import glob
from enum import Enum
from re import findall
import pygame
import numpy as np
import random
import sys

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self, size = 5, width=1500, height=1000):
        pygame.init()
        self.size = size
        self.tileSize = 150
        self.score = 0
        self.step = -1
        
        self.width = max(width, self.size*self.tileSize)
        self.height = max(height, self.size*self.tileSize)
        self.backgroundColor = (160,160,160)
        self.screen = self.createScreen()
        self.borderWidth, self.startPoint = self.getBorderAndStartPoint()
        self.font = pygame.font.Font(None, int(self.tileSize*0.5))
        self.drawnTiles = self.drawGrid(borderColor=(0,0,0))

        self.grid = np.zeros((size,size),dtype=int)
        self.numbersDir = self.getNumbers()

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
        drawnTiles = self.drawnTiles
        emptySpots = []

        for row in range(self.size):
            for element in range(self.size):
                if grid[row][element] == 0:
                    temp = [drawnTiles[row][element][0],drawnTiles[row][element][1],row,element]
                    emptySpots.append(temp)

        return np.array(emptySpots,dtype=int)
    
    def putNumber(self,emptySpots,step):
        choice = random.randint(1,10)
        if choice == 1:
            imageLoad = self.numbersDir[2]
            imageValue = self.numbersDir[3]
        else:
            imageLoad = self.numbersDir[0]
            imageValue = self.numbersDir[1]
        imageLoad = pygame.image.load(imageLoad)
        imageLoad = pygame.transform.scale(imageLoad, (self.tileSize,self.tileSize))
    
        if step == -1:
            spot = random.sample(range(len(emptySpots)), 2)
            spot = (emptySpots[spot][:2][:2])
        else:
            spot = random.sample(range(len(emptySpots)), 1)
            spot = emptySpots[spot][:2]

        for position in spot:
            self.screen.blit(imageLoad,(position[0],position[1]))
            self.grid[position[2]][position[3]]=imageValue
        pygame.display.flip()
        self.step+=1

    def updateScreen(self):
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
        return

    def moveNonZero(self,row):
        updatedRow=[]
        for element in row:
                if element != 0:
                    updatedRow.append(element)
        
        return updatedRow


    def merge(self,updatedRow):
        try:
            for i in range(len(updatedRow) - 1):
                updatedRow = self.moveNonZero(updatedRow)
                if updatedRow[i] == updatedRow[i + 1]:
                    self.score += updatedRow[i]
                    score = self.font.render("Score: "+str(self.score),True,(0,0,0))
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
            updatedRow = self.merge(updatedRow)
            while len(updatedRow) != self.size:
                updatedRow.append(0)
            updatedGrid.append(updatedRow)

        updatedGrid = np.array(updatedGrid)
        for i in range(timesRotated):
            updatedGrid = np.rot90(updatedGrid,-1)

        self.grid = updatedGrid

    def move(self,keys,emptySpots):
        grid = self.grid
        if keys[pygame.K_LEFT]:
            direction = Direction.LEFT
            self.slide(direction)

        elif keys[pygame.K_UP]:
            direction = Direction.UP
            self.slide(direction)

        elif keys[pygame.K_RIGHT]:
            direction = Direction.RIGHT
            self.slide(direction)

        elif keys[pygame.K_DOWN]:
            direction = Direction.DOWN
            self.slide(direction)

        if (grid == self.grid).all():
            return False
        else:
            self.putNumber(emptySpots,self.step)
            return True

    def play(self):
        keepRunning = True
        running = True

        changed = True
        emptySpots = self.getEmptySpots()
        self.putNumber(emptySpots,self.step)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepRunning = False
                    running = False

                elif event.type == pygame.KEYDOWN:
                    emptySpots = self.getEmptySpots()
                    if self.isGameOver(emptySpots) != True:
                        keys = pygame.key.get_pressed()
                        changed = self.move(keys,emptySpots)
                        
                        print('score: ',self.score,'step: ',self.step,'\ngrid: \n',self.grid)
                    else:
                        running=False
                    
                    if changed:
                        self.updateScreen()

        if keepRunning == False:
            return False
        else:
            return True



    def isGameOver(self,emptySpots):
        if emptySpots.size == 0:
            print('game over')
            print(self.score)
            return True
        else:
            return False
                    
            
if __name__ == '__main__':
    while True:
        game = Game()
        keepRunning = game.play()

        if keepRunning == False:
            break
    
    pygame.quit()