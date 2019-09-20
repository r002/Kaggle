###################################
##
##  Kaggle | Titanic Challenge
##  Title  | Generate Submission
##  Author | Robert Lin
##  Date   | Sep 20, 2019
##
###################################

import pandas as pd
import random

print('\nGenerate Submission!\n')

df = pd.read_csv("data/test.csv")

## Drop all columns but PassengerId, Survived, Pclass, Sex, Age
df = df[['PassengerId', 'Pclass', 'Sex', 'Age']]

## Assume women, children, and First Class passengers survived. How accurate is this in the training set?
def survival_critera(row):
    ## For people in steerage, predict only half the female population (including female children) survived
    if (row['Pclass']==3) & (row['Sex']=="female"):
        return random.randint(0, 1)
    elif (row['Sex']=="female") | (row['Age']<19):
        return 1
    else:
        return 0

df["Survived"] = df.apply(lambda row: survival_critera(row), axis=1)
print(df.head())

## Drop all columns except for PassengerId, Survived
df = df[['PassengerId', 'Survived']]
print(df.head())

df.to_csv(r'submission/titanic-sub03.csv', index = None, header=True)
