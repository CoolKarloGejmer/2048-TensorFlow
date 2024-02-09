import random
from os.path import join
from os import getcwd
import pygame
import numpy as np
import glob

class Game:
    def __init__(self, size = 5, width=1500, height=1000):
        self.size = size
        self.tileSize = 150
        self.score = 0
        self.step = 0
        
        self.width = max(width, self.size*self.tileSize)
        self.height = max(height, self.size*self.tileSize)
        self.screen = self.createScreen()
        self.drawnTiles = self.drawGrid()

        self.grid = np.zeros((size,size),dtype=int)
        self.numbersDir = self.getNumbers()

    def createScreen(self):
        screen = pygame.display.set_mode( (self.width, self.height) )
        pygame.display.set_caption('2048')
        screen.fill((160,160,160))
        pygame.display.flip()
        return screen
    
    def drawGrid(self):
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
            pygame.draw.rect(self.screen,(0,0,0),inner_rect)
            pygame.draw.rect(self.screen,(160,160,160),outer_rect)
        pygame.display.flip()

        matrix = np.reshape(matrix,(self.size,self.size,2))

        return matrix
    
    def getNumbers(self):
        current_directory = getcwd()
        folder_path = join(current_directory, "numbers")

        pattern = join(folder_path, "*.png")
        numbers = glob.glob(pattern)

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
        print(self.grid)

    def move(self,keys):
        if keys[pygame.K_LEFT]:
            return
        elif keys[pygame.K_UP]:
            return
        elif keys[pygame.K_RIGHT]:
            return
        elif keys[pygame.K_DOWN]:
            return
        

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
                        game.putNumber(emptySpots,self.step)
                    else:
                        running=False
                    
                    keys = pygame.key.get_pressed()
                    game.move(keys)

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