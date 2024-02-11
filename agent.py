from gameForAgent import Game
from model import Model
import pygame
import random
import pandas as pd 
import numpy as np

def train(generations=10, size=5, stutter = 3, epochs=10):
    data = {'state': [], 'score': [], 'action': []}
    feature = 'state'
    label = 'action'
    learning_rate = 0.01
    myModel = Model.buildModel(learning_rate, size)
    highscore = 0
    generation = 0
    while generation <= generations:
        generation += 1
        print(generation)
        print(highscore)
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
                    Model.save_model(myModel,'models/model'+str(size))
                    running = [False,False]
                    generation = generations

        if highscore < score:
            highscore = score
        for state, score, action in memory:
            data['state'].append(state)
            data['score'].append(score)
            data['action'].append(action)

        if running[1] == False:
            break

        df = pd.DataFrame(data)
        feature = np.array(df['state'].tolist())
        label = np.array(df['action'].tolist())
        score = np.array(df['score'].tolist())

        myModel = Model.trainModel(myModel, feature, label, score, epochs)

    df = pd.DataFrame(data)
    feature = np.array(df['state'].tolist())
    label = np.array(df['action'].tolist())
    myModel = Model.trainModel(myModel, feature, label, score, epochs)

    df.to_csv('data/data'+str(size)+'.csv', index=False)
    Model.save_model(myModel,'models/model'+str(size))
    pygame.quit()
    print(highscore)
        
if __name__ == '__main__':
    size = 5
    learning_rate = 0.01
    epochs = 10
    myModel = Model.buildModel(learning_rate, size)
    train(generations=200, size=4, stutter=4 , epochs=10)
