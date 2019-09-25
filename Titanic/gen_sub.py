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
import time

class C:
    SEED = time.time()
    # SEED = 1569370095.0708084  # Yields 0.8092 accuracy against training set; 721 correct predictions
    CHILD_AGE = 15


## Assume women and children survived. How accurate is this in the training set?
def survival_critera(row):
    ## For passengers in steerage, predict only 1/3 of the children surivved
    random.seed(C.SEED)
    if (row['Pclass']==3) & (row['Age']<=C.CHILD_AGE):
        steerage_child_survival_probability = random.randint(0, 2)
        if 1==steerage_child_survival_probability:
            return 1
        else:
            return 0
    ## For passengers in steerage, predict only half the adult female population survived
    elif (row['Pclass']==3) & (row['Sex']=="female") & (row['Age']>C.CHILD_AGE):
        return random.randint(0, 1)
    elif (row['Sex']=="female") | (row['Age']<=C.CHILD_AGE):
        return 1
    else:
        return 0


def gen_predictions(df, mode):
    ## Drop all columns but PassengerId, Survived, Pclass, Sex, Age
    df = df[['PassengerId', 'Pclass', 'Sex', 'Age']]
    df["Survived"] = df.apply(lambda row: survival_critera(row), axis=1)
    print(df.head())

    ## Drop all columns except for PassengerId, Survived
    df = df[['PassengerId', 'Survived']]
    print(df.head())

    ## Output the predictions to a file
    if("train"==mode):
        df.to_csv(r'submission-train/train-sub05.csv', index = None, header=True)

        ## Compare the generated training predictions against training answers
        run_training_analysis(df)
    else:
        df.to_csv(r'submission/test-sub05.csv', index = None, header=True)


def check_accuracy(row):
    if (row['SubSurvived']==row['Survived']):
        return 1
    else:
        return 0


def run_training_analysis(df):
    ## Create a file of all of the incorrect predictions
    answers = pd.read_csv("data/train-answers.csv")
    answers["SubSurvived"] = df[['Survived']]

    ## Evaluate how many rows are correct
    answers["Correct"] = answers.apply(lambda row: check_accuracy(row), axis=1)
    no_correct = answers[answers['Correct']==1].shape[0]
    total = answers.shape[0]
    accuracy = no_correct/total

    ## Output a df of all incorrect predictions to a file
    df_incorrect = answers[answers['Correct']==0]
    print(df_incorrect.head())


    print("*************")
    print(f"Correct Predictions: {no_correct}")
    print(f"Total Rows: {total}")
    print(f"Training Accuracy: {accuracy}")
    print(f"Seed: {C.SEED}\n")

#####################################################################

print('\nGenerate Submission!')

def gen_training_predictions():
    print("generating training predictions..")
    df = pd.read_csv("data/train.csv")
    gen_predictions(df, "train")

def gen_test_predictions():
    print("generating test predictions..")
    df = pd.read_csv("data/test.csv")
    gen_predictions(df, "test")

def say_hello():
    print("hello there!")

def invoke_exit():
    print("Bye!")

options = {1 : gen_training_predictions,
           2 : gen_test_predictions,
           3 : say_hello,
           4 : invoke_exit
}

# Present an options menu to solicit the user's input
prompt = """
Please input your command:
1) Generate training predictions
2) Generate test predictions
3) Say Hello
4) Exit
"""
choice = input(prompt)
print(choice)
options[int(choice)]()
# print(sys.argv)

exit()
