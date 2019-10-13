from algo.SimpleAlgo import SimpleAlgo
from algo.CorrAlgo import CorrAlgo
import pandas as pd

print('\nGenerate Submission!')

def gen_training_predictions():
    print("performing analysis of training data..\n")
    algo.perform_training_analysis()

    print("generating training predictions..\n")
    df = pd.read_csv("data/train.csv")
    df = algo.gen_predictions(df, "train", trialNo)
    algo.finalize_predictions(df, "train", trialNo)

def gen_test_predictions():
    print("generating test predictions..\n")
    df = pd.read_csv("data/test.csv")
    df = algo.gen_predictions(df, "test", trialNo)
    algo.finalize_predictions(df, "test", trialNo)

def say_hello():
    print(f"hello there! {algo.TRIAL_NO}")

def invoke_exit():
    print("Bye!")

#####################################################################

options = {1 : gen_training_predictions,
           2 : gen_test_predictions,
           3 : say_hello,
           4 : invoke_exit
}

# Ask user to input the TrialNo-- this will be used as the suffix
# for the output files that are generated
trialNoPrompt = """
Please enter the trial number:
"""
trialNo = input(trialNoPrompt)
print(f"Trial No: {trialNo}")


## Ask user to select the algo they desire to use
algoPrompt = """
Please select the algo desired:
1) Simple Algo
2) Correlation Algo
"""
algoSel = input(algoPrompt)

if "1"==algoSel:
    algo = SimpleAlgo(trialNo)
elif "2"==algoSel:
    algo = CorrAlgo(trialNo)

# Present an options menu to solicit the user's input
prompt = """
Please input your command:
1) Generate training predictions
2) Generate test predictions
3) Say Hello
4) Exit
"""
choice = input(prompt)
print(f"Selection: {choice}\n")
options[int(choice)]()
# print(sys.argv)

exit()
