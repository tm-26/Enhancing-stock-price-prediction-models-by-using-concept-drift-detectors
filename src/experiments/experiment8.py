# Experiment 8 evaluates method 4

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
        args[0] --> numberOfWaitDays parameter
        Controls how many days the model waits before comparing the current distribution to previous distributions.
    """

    # Handle arguments
    numberOfWaitDays = 5

    if len(sys.argv) >= 2:
        if sys.argv[1].lower() == "all":
            numberOfWaitDays = -1
        else:
            try:
                numberOfWaitDays = int(sys.argv[1])
                if not 4 <= numberOfWaitDays <= 40:
                    raise ValueError
                elif numberOfWaitDays == 0:
                    numberOfWaitDays = 5
            except ValueError:
                print("Argument error: " + str(sys.argv[1]) + " not a valid numberOfWaitDays parameter")
                print("numberOfWaitDays parameter needs to be an integer between 4 and 40")
                exit(-2)

    if numberOfWaitDays == -1:
        if not os.path.exists("../../results"):
            os.makedirs("../../results")

        if not os.path.exists("../../results/method4.csv"):
            file = open("../../results/method4.csv", "w+")
            writer = csv.writer(file)
            writer.writerow(["numberOfWaitDays", "ACC", "MCC"])
            file.close()

        results = pandas.read_csv("../../results/method4.csv")

        complete = []
        for i in results["numberOfWaitDays"]:
            complete.append(int(i))

        for i in range(4, 41):
            if i not in complete:
                print("+------------------------------+")
                print("Starting numberOfWaitDays parameter = " + str(i))
                print("+------------------------------+")
                acc, mcc = main(True, 5, i)
                results = results.append({"numberOfWaitDays": i, "ACC": acc, "MCC": mcc}, ignore_index=True)
                results.to_csv("../../results/method4.csv", index=False)

        numberOfWaitDays = []
        acc = []
        mcc = []

        for i in results.iterrows():
            numberOfWaitDays.append(int(i[1]["numberOfWaitDays"]))
            acc.append(float(i[1]["ACC"].split(' ')[0]))
            mcc.append(float(i[1]["MCC"].split(' ')[0]))

        matplotlib.pyplot.plot(numberOfWaitDays, acc)
        matplotlib.pyplot.xlabel("numberOfWaitDays parameter")
        matplotlib.pyplot.ylabel("ACC")
        matplotlib.pyplot.show()

        matplotlib.pyplot.plot(numberOfWaitDays, mcc)
        matplotlib.pyplot.xlabel("numberOfWaitDays parameter")
        matplotlib.pyplot.ylabel("MCC")
        matplotlib.pyplot.show()
    else:
        print("+------------------------------+")
        print("Starting numberOfWaitDays parameter = " + str(numberOfWaitDays))
        print("+------------------------------+")
        acc, mcc = main(True, 5, numberOfWaitDays)
