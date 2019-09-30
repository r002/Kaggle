##
## This class implements Algo.
## It is a basic implement with no machine learning.
## Date: Sunday - Sep 29, 2019
##

from algo.BaseAlgo import BaseAlgo
import random

class BasicAlgo(BaseAlgo):

    # def hello_from_basic(self):
    #     return "Hello from basic algo!"

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

        return df
