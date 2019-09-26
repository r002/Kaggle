from gen_sub import Algo
import pandas as pd

print('\nGenerate Submission!')

algo = Algo()

def gen_training_predictions():
    print("generating training predictions..\n")
    df = pd.read_csv("data/train.csv")
    algo.gen_predictions(df, "train")

def gen_test_predictions():
    print("generating test predictions..\n")
    df = pd.read_csv("data/test.csv")
    algo.gen_predictions(df, "test")

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
