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

## Define constants
CHILD_AGE = 15

## Choose to generate submission from training or test set
# df = pd.read_csv("data/train.csv")
df = pd.read_csv("data/test.csv")

## Drop all columns but PassengerId, Survived, Pclass, Sex, Age
df = df[['PassengerId', 'Pclass', 'Sex', 'Age']]

## Assume women, children, and First Class passengers survived. How accurate is this in the training set?
def survival_critera(row):
    ## For passengers in steerage, predict only 1/3 of the children surivved
    if (row['Pclass']==3) & (row['Age']<=CHILD_AGE):
        steerage_child_survival_probability = random.randint(0, 2)
        if 1==steerage_child_survival_probability:
            return 1
        else:
            return 0
    ## For passengers in steerage, predict only half the adult female population survived
    elif (row['Pclass']==3) & (row['Sex']=="female") & (row['Age']>CHILD_AGE):
        return random.randint(0, 1)
    elif (row['Sex']=="female") | (row['Age']<=CHILD_AGE):
        return 1
    else:
        return 0

df["Survived"] = df.apply(lambda row: survival_critera(row), axis=1)
print(df.head())

## Drop all columns except for PassengerId, Survived
df = df[['PassengerId', 'Survived']]
print(df.head())

## Choose output destination
# df.to_csv(r'submission-train/train-sub04.csv', index = None, header=True)
df.to_csv(r'submission/titanic-sub05-child-age-15.csv', index = None, header=True)
