###################################
##
##  Kaggle | Titanic Challenge
##  Title  | Evaluate Submission
##           This script evaluates the inputted train-submission
##           against the training dataset to see accuracy.
##  Author | Robert Lin
##  Date   | Sep 20, 2019
##
###################################

import pandas as pd

submission = pd.read_csv("submission-train/train-sub04.csv")
answers = pd.read_csv("data/train-answers.csv")

## Evaluate the accuracy of the submission against the training dataset (the answers)
print("SUBMISSION")
print(submission.head())
print()
print("ANSWERS")
print(answers.head())
print()

answers["SubSurvived"] = submission[['Survived']]
print(answers.head())
print()

def check_accuracy(row):
    if (row['SubSurvived']==row['Survived']):
        return 1
    else:
        return 0

## Evaluate how many rows are correct
answers["Correct"] = answers.apply(lambda row: check_accuracy(row), axis=1)
no_correct = answers[answers['Correct']==1].shape[0]
total = answers.shape[0]
accuracy = no_correct/total

print(answers.head())
print()
print(f"Accuracy: {accuracy}")
print(f"Rows correct: {no_correct}")
print(f"Rows total: {total}")
