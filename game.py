import random
from os.path import join
from os import getcwd
import pygame
import numpy as np
from glob import glob
from enum import Enum

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self, size = 5, width=1500, height=1000):
        self.size = size
        self.tileSize = 150
        self.score = 0
        self.step = 0
        
        self.width = max(width, self.size*self.tileSize)
        self.height = max(height, self.size*self.tileSize)
        self.screen = self.createScreen()
        self.drawnTiles = self.drawGrid(borderColor=(0,0,0))

        self.grid = np.zeros((size,size),dtype=int)
        self.numbersDir = self.getNumbers()

    def createScreen(self):
        screen = pygame.display.set_mode( (self.width, self.height) )
        pygame.display.set_caption('2048')
        screen.fill((160,160,160))
        pygame.display.flip()
        return screen
    
    def drawGrid(self,borderColor):
        startPoint=[(self.width/2)-(self.tileSize*self.size/2),
                    (self.height/2)-(self.tileSize*self.size/2)]
        borderWidth=round(self.tileSize*0.01)
        if borderWidth == 0:
            borderWidth = 1
        
        matrix = []
        for tileY in range(self.size):
            for tileX in range(self.size):
                matrix.append((startPoint[0]+self.tileSize*tileX,
                               startPoint[1]+self.tileSize*tileY))
        matrix = np.array(matrix)

        for position in matrix:
            inner_rect = pygame.Rect(position[0],position[1],self.tileSize,self.tileSize)
            outer_rect=pygame.Rect(position[0] + borderWidth, position[1] + borderWidth,
                                   self.tileSize - borderWidth*2, self.tileSize - borderWidth*2)
            pygame.draw.rect(self.screen,borderColor,inner_rect)
            pygame.draw.rect(self.screen,(160,160,160),outer_rect)
        pygame.display.flip()

        matrix = np.reshape(matrix,(self.size,self.size,2))

        return matrix
    
    def getNumbers(self):
        current_directory = getcwd()
        folder_path = join(current_directory, "numbers")

        pattern = join(folder_path, "*.png")
        numbers = glob(pattern)

        return numbers

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
        image2 = self.numbersDir[0]
        image2 = pygame.image.load(image2)
        image2 = pygame.transform.scale(image2, (self.tileSize,self.tileSize))
    
        if step == 0:
            spot = random.sample(range(len(emptySpots)), 2)
            spot = (emptySpots[spot][:2][:2])
        else:
            spot = random.sample(range(len(emptySpots)), 1)
            spot = emptySpots[spot][:2]

        for position in spot:
            self.screen.blit(image2,(position[0],position[1]))
            self.grid[position[2]][position[3]]=2
        pygame.display.flip()

    def updateScreen():
        return

    def moveNonZero(self,row):
        updatedRow=[]
        for element in row:
                if element != 0:
                    updatedRow.append(element)
        
        return updatedRow


    def merge(self,row):
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0

        while len(row) != self.size:
            row.append(0)
        
        return row
    
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
            updatedGrid.append(updatedRow)

        updatedGrid = np.array(updatedGrid)
        for i in range(timesRotated):
            updatedGrid = np.rot90(updatedGrid,-1)

        self.grid = updatedGrid

    def move(self,keys,emptySpots):
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

        self.putNumber(emptySpots,self.step)
            
            
        

    def play(self):
        keepRunning = True
        running = True

        emptySpots = game.getEmptySpots()
        game.putNumber(emptySpots,self.step)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepRunning = False
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.step+=1

                    emptySpots = game.getEmptySpots()
                    if game.isGameOver(emptySpots) != True:
                        keys = pygame.key.get_pressed()
                        game.move(keys,emptySpots)
                        print(self.grid)
                    else:
                        running=False

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