##
## This class implements Algo.
## This algo performs basic machine learning during its training.
## It looks at correlations between certain columns and bases items
## calculations on those correlations.
## Date: Sunday - Sep 29, 2019
##

from algo.BaseAlgo import BaseAlgo

class CorrAlgo(BaseAlgo):

    ## This method caluculates correlation coefficients and weights for every column in the training set
    def perform_training_analysis(self):
        ## Create a table that lists the correlation coeffients for each column
        print("**** Initiate CorrAlgo training..")

        series_survived = self.df_train['Survived']
        series_sex = self.df_train['Sex']
        sex = {'male': 0,'female': 1}
        self.df_train.Sex = [sex[item] for item in self.df_train.Sex]
        self.df_train.corr(method ='pearson')
        # corr_sex = # Still need to implement! 9/29/30

        return 1
