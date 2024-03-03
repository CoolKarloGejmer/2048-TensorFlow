import numpy as np
import tensorflow as tf
from random import sample

class Model:
    def buildModel(learning_rate, size):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', input_shape=(size, size, 1)),
            tf.keras.layers.Flatten(input_shape=(size, size)),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(4, activation='linear')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),
                      loss='mean_squared_error',
                      metrics=['accuracy'])
        
        return model
    
    def cloneModel(model):
        return tf.keras.models.clone_model(model)

    def trainModel(model,feature,label,epochs=10,batch_size=20,verbose = 0):
        
        model.fit(x=feature, #states
                y=label, #actions (qvalues)
                epochs=epochs,
                batch_size=batch_size,
                verbose=verbose)
        
        return model
    
    def predict(model,state,size):
        state = np.array(state).reshape(-1, size, size)
        actions = model.predict(state, verbose = 0)

        return actions

    def save_model(model, path):
        model.save(path)
        print("Model saved successfully.")

    def checkForStutter(memory,stutter):
        if len(memory) <= stutter:
            return True
        latest_memory = memory[-1*stutter:]
        states = []

        for i in range(stutter):
            states.append(latest_memory[i][0])

        count=0
        for i in range(len(states)-1):
            if (states[i] == states[i+1] ).all():
                count+=1
        
        if count == stutter:
            print('stuttering')
            return True
        else:
            return False
    
    def updateQValues(memory, batch_size, target_model, model, discount_factor):
        batch = sample(memory, batch_size)
        states, actions, rewards, next_states = zip(*batch)

        states = np.array(states)
        next_states = np.array(next_states)

        q_values = model.predict(states,verbose=0)
        next_q_values = target_model.predict(next_states,verbose=0)

        for i in range(batch_size):
            q_values[i][actions[i]] = rewards[i] + discount_factor * np.max(next_q_values[i])

        model.fit(states, q_values, epochs=1, batch_size=batch_size, verbose=0)

        return model
