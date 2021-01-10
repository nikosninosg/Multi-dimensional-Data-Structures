import pandas as pd


def read_data():
    ret_df = pd.read_csv("data/data.csv")
    ret_df.drop(labels=["accuracy", "time", "place_id"], axis="columns", inplace=True)
    return ret_df


if __name__ == '__main__':
    df = read_data()
    print(df[0:3])
