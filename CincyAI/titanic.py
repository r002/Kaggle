import pandas as pd

class Postmortem:

    Survived = -1
    Perished = -1
    SurvivalProbability = -1

    def __init__(self):
        df_train = pd.read_csv("staticfiles/titanic-data/train.csv")
        df_test = pd.read_csv("staticfiles/titanic-data/test.csv")
        df_sub = pd.read_csv("staticfiles/titanic-data/test-sub14.csv")

        # Add the SurvivedSub column to the test set
        df_test['SubSurvived'] = df_sub['Survived']

        df_survived = df_test[df_test['SubSurvived']==1]
        df_perished = df_test[df_test['SubSurvived']==0]

        self.Survived = df_survived.shape[0]
        self.Perished = df_perished.shape[0]
        a = self.Survived/(self.Survived+self.Perished) * 100
        self.SurvivalProbability = "{0:.2f}".format(a)
