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

class Algo:

    def __init__(self, trialNo):
        print("******** Welcome to Robert's Titanic Kaggle Predictor! ********")
        self.SEED = int(time.time())
        # SEED = 1569450935.079536     # 0.8114478114478114; 723 correct predictions
        # SEED = 1569370095.0708084  # Yields 0.8092 accuracy against training set; 721 correct predictions
        self.CHILD_AGE = 15
        self.TRIAL_NO = trialNo

        ## Build a table of all tickets with FOUR or more passengers. Predict these people all perished
        ## For the 'body of knowledge'-- combine all of the ticket numbers from the training set with the test set

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

    ## Predict that all females (adult & children) in groups four or larger with big families (>6) perished
    def check_if_group_is_4_or_larger(self, row):
        if (row['Sex']=="female") & (self.v.index[self.v.gt(4)].contains(row['Ticket']) & ((row['SibSp']+row['Parch'])>6)):
            return 1
        else:
            return -1

    def survival_critera2(self, row):
        ## Check to see if this ticket number is shared by any survivors
        # return self.check_if_surviving_ticket(ticketNo)
        return self.check_if_group_is_4_or_larger(row)


    def combine_predictions(self, row):
        if(row['Survived2']==1):
            return 0  # Assume women in groups sized four or larger perished
        else:
            return row['Survived1']


    def gen_predictions(self, df, mode, trialNo):
        ## Drop unneccessary columns
        if("train"==mode):
            df = df[['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Ticket', 'Survived']]
        else:
            df = df[['PassengerId', 'Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch', 'Ticket']]

        df["Survived1"] = df.apply(lambda row: self.survival_critera(row), axis=1)
        print("\n## First Pass:")
        print(df.head())

        ## Second pass
        ## If the passenger shares the same ticket number as a survivor, predict their fate was shared
        df["Survived2"] = df.apply(lambda row: self.survival_critera2(row), axis=1)
        print("\n## Second Pass:")
        print(df.head(20))

        ## Update the predictions based on the new analysis performed in the second pass
        df["SurvivedCombined"] = df.apply(lambda row: self.combine_predictions(row), axis=1)


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
