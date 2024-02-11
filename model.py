import numpy as np
import tensorflow as tf

class Model:
    def buildModel(learning_rate, size):
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(size, size)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(4, activation='softmax')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        return model

    def trainModel(model,feature,label,score,epochs=10):

        model.fit(x=feature,
                y=label,
                epochs=epochs,
                sample_weight=score)
        
        return model
    
    def predict(model,state,size):
        state = np.array(state).reshape(-1, size, size)
        actions = model.predict(state)
        decided_action = np.argmax(actions)

        return int(decided_action)

    def save_model(model, path):
        model.save(path)
        print("Model saved successfully.")

    def checkForStutter(memory,stutter):
        stutter += 1
        if len(memory) <= stutter:
            return False
        latest_memory = memory[-stutter:]
        states = []

        for i in range(stutter):
            states.append(latest_memory[i][0])

        count=0
        for i in range(len(states)-1):
            if (states[i] == states[i+1] ).all():
                count+=1
        
        if count == stutter-1:
            return False
        else:
            return True

