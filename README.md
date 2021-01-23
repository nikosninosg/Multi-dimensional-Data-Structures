# Multi-dimensional-Data-Structures

**K-D trees, Quad Trees και 2D Range Trees: 2D kNN Queries Implementation.**

Data:
The train and test dataset are split based on time, and the public/private leaderboard in the test data are split randomly. There is no concept of a person in this dataset. All the row_id's are events, not people. 

Note: Some of the columns, such as time and accuracy, are intentionally left vague in their definitions. Please consider them as part of the challenge. 

File descriptions:
1. train.csv, test.csv (https://www.kaggle.com/c/facebook-v-predicting-check-ins/data)
    - row_id: id of the check-in event
    - x y: coordinates
    - accuracy: location accuracy 
    - time: timestamp
    - place_id: id of the business, this is the target you are predicting

2. train_x_y.csv
    - x y: coordinates (https://drive.google.com/file/d/151xoFDNtabYaFT6Dxy5D1nXp_-8L1ttq/view?usp=sharing)
