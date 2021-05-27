# Experiment 5 evaluates method 1


import os
import sys

sys.path.append("..")
from main import main

if __name__ == "__main__":

    results = main(True, 1)

    if not os.path.exists("../../results"):
        os.makedirs("../../results")

    file = open("../../results/method1.txt", "w+")
    file.write("ACC = " + str(results[0]) + '\n')
    file.write("MCC = " + str(results[1]))
    file.close()