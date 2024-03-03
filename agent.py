from gameForAgent import Game
from model import Model
import pygame
import random
import numpy as np
import pandas as pd
from plot import plotdata

class ReplayMemory: 
    def __init__(self):
        self.capacity = replay_capacity
        self.memory = []

    def push(self, state, action, reward, next_state):
        if len(self.memory) >= self.capacity:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

class Agent:
    def __init__(self):
        if replay_capacity < batch_size:
            print('Error: Replay capacity is bigger than batch size')
        self.model = Model.buildModel(learning_rate, size)
        self.target_model = Model.cloneModel(self.model)
        self.replay_memory = ReplayMemory()
        self.epsilon = epsilon_initial
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_minimum

    def train(self):
        highscore = 0
        generation = 0
        target_model_update_counter = 0
        plot = {'generation':[],'score':[],'epsilon':[],'displayGraphics':displayGraphics,'learning_rate':learning_rate}

        while generation <= generations:
            generation += 1
            print('generation:', generation-1, '/', generations)
            game = Game(size=size, displayGraphics=displayGraphics)
            running = [True, True]
            score = 0

            while running[0]:
                state = game.grid
                if np.random.rand() < self.epsilon or generation < 2 or Model.checkForStutter(self.replay_memory.memory,stutter) == True:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(Model.predict(self.model,state,size))

                running = game.play(action)
                next_state = game.grid
                score_before = score
                score = game.score
                if game.step > 1:
                    reward = score - score_before
                else:
                    reward = score
                self.replay_memory.push(state, action, reward, next_state)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = [False, False]
                        generation = generations + 1
                        break
                
                if len(self.replay_memory.memory) >= batch_size:
                    self.model = Model.updateQValues(self.replay_memory.memory, batch_size, self.target_model, self.model, discount_factor)

            if score > highscore:
                highscore = score
            
            if len(self.replay_memory.memory) >= batch_size:
                for _ in range(epochs):
                    batch = self.replay_memory.sample(batch_size)

                    states, actions, reward, next_state = zip(*batch)

                    states = np.array(states)
                    actions = np.array(actions)

                    self.model = Model.trainModel(self.model, states, actions, epochs, batch_size)


            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            self.epsilon = round(self.epsilon*10e8)/10e8

            target_model_update_counter +=1
            if target_model_update_counter % target_model_update_frequency == 0:
                self.target_model.set_weights(self.model.get_weights())
                target_model_update_counter = 0
            
            plot['generation'].append(generation)
            plot['score'].append(score)
            plot['epsilon'].append(self.epsilon)
            df=pd.DataFrame(plot)
            df.to_csv('data/plot'+str(size)+'.csv', index=False)
            plotdata('data/plot'+str(size)+'.csv')
        Model.save_model(self.model,'models/model'+str(size))
        
if __name__ == '__main__':
    size = 3
    displayGraphics = True
    generations = 300
    
    learning_rate = 1e-3
    epochs = 8
    batch_size = 35

    epsilon_initial = 1.0
    epsilon_decay = 0.99
    epsilon_minimum = 0.01
    target_model_update_frequency = 100
    discount_factor = 0.99

    stutter = 3
    replay_capacity = 100
    
    agent = Agent()
    Agent.train(agent)
