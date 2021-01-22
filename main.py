import pandas as pd
from matplotlib import pyplot as plt
import QuadTree


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    df = read_data()
    print('Dataframe Created')
    print('Calculating k nearest neighbors...')
    # print(df[0:3])
    QuadTree.run(df[0:1000000])   # runs well with 10^5 elements, runs ok with 10^6 elements
    print("Process ended")
