###################################
##
##  Kaggle | Titanic Challenge
##  Title  | Explore Training Set
##  Author | Robert Lin
##  Date   | Sep 20, 2019
##
###################################

import pandas as pd

print('\nHello!\n')

## Functions
def find_survivors_by_class(df, pclass):
    ## Take a subset of only the n'th Class passengers
    df = df[df['Pclass']==pclass]

    ## How many of them survived?
    survivors = df[df['Survived']==1]

    ## How many were female?
    female_population = df[df['Sex']=="female"]

    ## How many female survived?
    female_survivors = survivors[survivors['Sex']=="female"]

    ## How many were children?
    child_population = df[df['Age']<19]

    ## How many  children survived?
    child_survivors = survivors[df['Age']<19]

    print(f"{pclass}'th Class Total Population: {df.shape[0]}")
    print(f"No of {pclass}'th Class Survivors: {survivors.shape[0]}")
    print(f"{pclass}'th Class Female Population: {female_population.shape[0]}")
    print(f"No of {pclass}'th Class Female Survivors: {female_survivors.shape[0]}")
    print(f"{pclass}'th Class Child Population: {child_population.shape[0]}")
    print(f"No of {pclass}'th Class Child Survivors: {child_survivors.shape[0]}")



df0 = pd.read_csv("data/train.csv")

## Drop all columns but PassengerId, Survived, Pclass, Sex, Age
df = df0[['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age']]

find_survivors_by_class(df, 1)
print()
find_survivors_by_class(df, 2)
print()
find_survivors_by_class(df, 3)

print('\n')
exit()

## Assume all people in First Class survived. How accurate is this in the training set?
def survival_critera(row):
    if(row['Pclass']==1):
        return 1
    else:
        return 0

df["SurvivedPrediction"] = df.apply(lambda row: survival_critera(row), axis=1)
print(df.head(20))

## How accurate are these predictions?
true_positives = 0
false_positives = 0

def check_accuracy():
    if (row['SurvivedPrediction']==1) & (row['Survived']==1):
        return 1
    else:
        return 0
