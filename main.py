import pandas as pd
import QuadTree


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    df = read_data()
    print(df[0:3])
    QuadTree.run(df[0:100000])  # it runs well with 10^5 items and it runs ok with 10^6 items
