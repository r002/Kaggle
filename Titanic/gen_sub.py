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

class Algo:

    def __init__(self):
        print("*************** Initializing Constructor! ***************")
        self.SEED = time.time()
        # SEED = 1569450935.079536     # 0.8114478114478114; 723 correct predictions
        # SEED = 1569370095.0708084  # Yields 0.8092 accuracy against training set; 721 correct predictions
        self.CHILD_AGE = 15

        ## Build a table of all of the surviving ticket numbers from the training set
        self.df_train = pd.read_csv("data/train.csv")
        # surviving_tickets = df_train[df_train['Survived']==1]
        self.df_train = self.df_train[['Ticket', 'Survived']]

    def check_if_surviving_ticket(self, ticketNo):
        df0 = self.df_train[self.df_train['Ticket'].str.contains(ticketNo)]
        if df0.shape[0]>0:
            return df0.iloc[0]['Survived']
        else:
            return -1


    ## Assume women and children survived. How accurate is this in the training set?
    def survival_critera(self, row):
        ## For passengers in steerage, predict only 1/3 of the children survived
        random.seed(self.SEED)

        if (row['Pclass']==3) & (row['Age']<=self.CHILD_AGE):
            steerage_child_survival_probability = random.randint(0, 2)
            if 1==steerage_child_survival_probability:
                return 1
            else:
                return 0
        ## For passengers in steerage, predict half the adult female population survived
        elif (row['Pclass']==3) & (row['Sex']=="female") & (row['Age']>self.CHILD_AGE):
            return random.randint(0, 1)
        ## Predict that women, children, and fare-classes over 499 survived
        elif (row['Sex']=="female") | (row['Age']<=self.CHILD_AGE) | (row['Fare']>499):
            return 1
        else:
            return 0


    def survival_critera2(self, row):
        ticketNo = row['Ticket']
        ## Check to see if this ticket number is shared by any survivors
        return self.check_if_surviving_ticket(ticketNo)


    def gen_predictions(self, df, mode):
        ## Drop all columns but PassengerId, Survived, Pclass, Sex, Age
        df = df[['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Ticket']]
        df["Survived"] = df.apply(lambda row: self.survival_critera(row), axis=1)
        print("## First Pass:")
        print(df.head())

        ## Second pass
        ## If the passenger shares the same ticket number as a survivor, assume their fate was shared
        df["Survived2"] = df.apply(lambda row: self.survival_critera2(row), axis=1)
        print("## Second Pass:")
        print(df.head(20))

        ## Drop all columns except for PassengerId, Survived
        df = df[['PassengerId', 'Survived']]
        print(df.head())

        ## Output the predictions to a file
        if("train"==mode):
            df.to_csv(r'submission-train/train-sub07.csv', index = None, header=True)

            ## Compare the generated training predictions against training answers
            self.run_training_analysis(df)
        else:
            df.to_csv(r'submission/test-sub07.csv', index = None, header=True)


    def check_accuracy(self, row):
        if (row['SubSurvived']==row['Survived']):
            return 1
        else:
            return 0


    def run_training_analysis(self, df):
        ## Read the training answers into a df
        answers = pd.read_csv("data/train.csv")
        answers["SubSurvived"] = df[['Survived']]

        ## Evaluate how many rows are correct
        answers["Correct"] = answers.apply(lambda row: self.check_accuracy(row), axis=1)
        no_correct = answers[answers['Correct']==1].shape[0]
        total = answers.shape[0]
        accuracy = no_correct/total

        ## Output df_incorrect predictions to a file
        df_incorrect = answers[answers['Correct']==0]
        print(df_incorrect.head())
        df_incorrect.to_csv(r'submission-train/incorrect-sub07.csv', index = None, header=True)

        print("*************")
        print(f"Correct Predictions: {no_correct}")
        print(f"Total Rows: {total}")
        print(f"Training Accuracy: {accuracy}")
        print(f"Seed: {self.SEED}\n")

    #####################################################################
