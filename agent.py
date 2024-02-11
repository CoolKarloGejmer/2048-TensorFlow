from gameForAgent import Game
from model import Model
import pygame
import random
import pandas as pd 
import numpy as np

def train(generations=10, size=5, stutter = 3):
    data = {'state': [], 'score': [], 'action': []}
    feature = 'state'
    label = 'action'
    learning_rate = 0.01
    myModel = Model.buildModel(learning_rate, size)

    for generation in range(generations):
        print(generation)
        game = Game(size)
        running = [True,True]
        memory = []

        while running[0]:
            state = game.grid
            if generation != 0 and game.step != 0 and Model.checkForStutter(memory,stutter):
                action = Model.predict(myModel, state,size)
            else:
                action = random.randint(0,3)
            running = game.play(action)
            score = game.score
            memory.append((state,score,action))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = [False,False]

        for state, score, action in memory:
            data['state'].append(state)
            data['score'].append(score)
            data['action'].append(action)

        if running[1] == False:
            break

        df = pd.DataFrame(data)
        feature = np.array(df['state'].tolist())
        label = np.array(df['action'].tolist())

        myModel = Model.trainModel(myModel, feature, label)

    df = pd.DataFrame(data)
    feature = np.array(df['state'].tolist())
    label = np.array(df['action'].tolist())
    myModel = Model.trainModel(myModel, feature, label)

    df.to_csv('data/data'+str(size)+'.csv', index=False)
    Model.save_model(myModel,'models/model'+str(size))
    pygame.quit()
        
if __name__ == '__main__':
    size = 5
    learning_rate = 0.01
    myModel = Model.buildModel(learning_rate, size)
    train(generations=30,size=5,stutter=5)
