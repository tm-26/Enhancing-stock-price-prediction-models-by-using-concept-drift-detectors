# Experiment 7 evaluates method 3

import csv
import matplotlib.pyplot
import os
import pandas
import sys

sys.path.append("..")
from main import main


if __name__ == "__main__":

    """
        Parameters:
        args[0] --> splitDays parameter
        Controls how many days the model waits before starting to train on the current distribution.
    """

    # Handle arguments
    splitDays = 5

    if len(sys.argv) >= 2:
        if sys.argv[1].lower() == "all":
            splitDays = -1
        else:
            try:
                splitDays = int(sys.argv[1])
                if not 3 <= splitDays <= 30:
                    raise ValueError
                elif splitDays == 0:
                    splitDays = 5
            except ValueError:
                print("Argument error: " + str(sys.argv[1]) + " not a valid splitDays parameter")
                print("splitDays parameter needs to be an integer between 3 and 30")
                exit(-2)

    if splitDays == -1:
        if not os.path.exists("../../results"):
            os.makedirs("../../results")

        if not os.path.exists("../../results/method3.csv"):
            file = open("../../results/method3.csv", "w+")
            writer = csv.writer(file)
            writer.writerow(["splitDays", "ACC", "MCC"])
            file.close()

        results = pandas.read_csv("../../results/method3.csv")

        complete = []
        for i in results["splitDays"]:
            complete.append(int(i))

        for i in range(3, 31):
            if i not in complete:
                print("+------------------------------+")
                print("Starting splitDays parameter = " + str(i))
                print("+------------------------------+")
                acc, mcc = main(True, 3, i)
                results = results.append({"splitDays": i, "ACC": acc, "MCC": mcc}, ignore_index=True)
                results.to_csv("../../results/method3.csv", index=False)

        splitDays = []
        acc = []
        mcc = []

        for i in results.iterrows():
            splitDays.append(int(i[1]["splitDays"]))
            acc.append(float(i[1]["ACC"].split(' ')[0]))
            mcc.append(float(i[1]["MCC"].split(' ')[0]))

        matplotlib.pyplot.plot(splitDays, acc)
        matplotlib.pyplot.xlabel("splitDays parameter")
        matplotlib.pyplot.ylabel("ACC")
        matplotlib.pyplot.show()

        matplotlib.pyplot.plot(splitDays, mcc)
        matplotlib.pyplot.xlabel("splitDays parameter")
        matplotlib.pyplot.ylabel("MCC")
        matplotlib.pyplot.show()
    else:
        print("+------------------------------+")
        print("Starting splitDays parameter = " + str(splitDays))
        print("+------------------------------+")
        acc, mcc = main(True, 3, splitDays)
