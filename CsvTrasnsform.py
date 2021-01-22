import pandas as pd

# row_id, x,y: coordinates
# delete arrows: accuracy, time, place_id
df = pd.read_csv("train.csv")
df = df[:10000]
df = df.drop(labels=["row_id","accuracy", "time", "place_id"], axis="columns")

df.to_csv('train_x_y_10K.csv', index=False, sep=',')

print(df[0:3])

# Num of Rows:  29118021
print("Num of Rows: ", len(df.index))
