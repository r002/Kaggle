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
import datetime

class BaseAlgo:

    def __init__(self, trialNo):
        print("******** Welcome to Robert's Titanic Kaggle Predictor! ********")
        self.SEED = int(time.time())
        # SEED = 1569450935.079536     # 0.8114478114478114; 723 correct predictions
        # SEED = 1569370095.0708084  # Yields 0.8092 accuracy against training set; 721 correct predictions
        self.CHILD_AGE = 15
        self.TRIAL_NO = trialNo

        ## Build a table of all tickets with FOUR or more passengers. Predict these people all perished
        ## For the 'body of knowledge'-- combine all of the ticket numbers from the training set with the test set

        self.df_train = pd.read_csv("data/train.csv")

        df_train_tickets = pd.read_csv("data/train.csv")
        df_train_tickets = df_train_tickets[['Ticket']]
        df_test_tickets = pd.read_csv("data/test.csv")
        df_test_tickets = df_test_tickets[['Ticket']]
        df_all_tickets = pd.concat([df_train_tickets, df_test_tickets])
        self.v = df_all_tickets.Ticket.value_counts()

        # group4 = df_all_tickets[df_all_tickets.Ticket.isin(v.index[v.gt(4)])]
        # self.df_train = self.df_train[self.df_train['Survived']==1]
        # self.df_train = self.df_train[['Ticket', 'Survived']]


    # def check_if_surviving_ticket(self, ticketNo):
    #     df0 = self.df_train[self.df_train['Ticket'].str.contains(ticketNo)]
    #     if df0.shape[0]>0:
    #         return df0.iloc[0]['Survived']
    #     else:
    #         return -1


    def gen_predictions(self, df, mode, trialNo):

        # df = BasicAlgo.gen_predictions(df, mode, trialNo)

        ## Drop all columns except for PassengerId, Survived
        df = df[['PassengerId', 'SurvivedCombined']]
        df.rename(columns={'SurvivedCombined':'Survived'}, inplace=True)
        print("\n## Combined Final Predictions:")
        print(df.head(20))

        ## Sanity check - Output aggregate totals for survived and died
        survived = df[df['Survived']==1].shape[0]
        perished = df[df['Survived']==0].shape[0]
        print("\n## Sanity Check:")
        print(f"Survived prediction: {survived}")
        print(f"Perished prediction: {perished}")

        ## Print this sanity check out to a log file
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d__%I.%M %p")
        d_log = {'Survival Prediction' : survived,
                 'Perished Prediction' : perished,
                 'Datetime Run' : now,
                 'Seed' : self.SEED}

        ## Output the predictions to a file
        if("train"==mode):
            df.to_csv(fr'submission-train/train-sub{self.TRIAL_NO}.csv', index = None, header=True)
            d_train_log = self.run_training_analysis(df)
            d_log = {**d_log, **d_train_log}  # Concat the logging dictionaries
        else:
            df.to_csv(fr'submission/test-sub{self.TRIAL_NO}.csv', index = None, header=True)

        df_log = pd.DataFrame(list(d_log.items()))
        df_log.to_csv(fr'logs/log__{self.TRIAL_NO}__{now}.csv', index = None, header=True)


    ## This method caluculates correlation coefficients and weights for every column in the training set
    def perform_training_analysis(self):
        ## Create a table that lists the correlation coeffients for each column
        series_survived = self.df_train['Survived']
        series_sex = self.df_train['Sex']
        sex = {'male': 1,'female': 0}
        self.df_train.Sex = [sex[item] for item in self.df_train.Sex]
        self.df_train.corr(method ='pearson')
        # corr_sex = # Still need to implement! 9/29/30

        return 1


    def check_accuracy(self, row):
        if (row['SubSurvived']==row['Survived']):
            return 1
        else:
            return 0


    ## Compare the generated training predictions against training answers
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
        print("\n## Training Analysis:")
        print(df_incorrect.head())
        df_incorrect.to_csv(fr'submission-train/incorrect-sub{self.TRIAL_NO}.csv', index = None, header=True)

        d_log = {'Correct Predictions' : no_correct,
                 'Total Rows' : total,
                 'Training Accuracy' : accuracy}

        print("*************")
        print(f"Correct Predictions: {no_correct}")
        print(f"Total Rows: {total}")
        print(f"Training Accuracy: {accuracy}")
        print(f"Seed: {self.SEED}\n")

        return d_log

    #####################################################################
