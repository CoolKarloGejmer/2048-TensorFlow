import pandas as pd
import matplotlib.pyplot as plt

def plotdata(data_file):
    df = pd.read_csv(data_file)

    # Plot the scores
    plt.plot(df['generation'], df['score'])
    plt.title('Scores During Training')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.xlim(1, max(df['generation']) * 1.1)
    plt.ylim(1, max(df['score']) * 1.1)
    plt.show(block=False)
    plt.pause(.1)

