import pandas as pd

class TestPandas:

    aaa = "Hello from the TestPandas package!"

    def __init__(self):
        self.df_train = pd.read_csv("staticfiles/train.csv")
        self.rows = self.df_train.shape[0]
