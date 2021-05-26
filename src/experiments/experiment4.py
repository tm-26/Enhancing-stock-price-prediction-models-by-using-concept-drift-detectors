"""

"""

import os
import pandas
import skmultiflow.drift_detection
import sys
from statistics import mean

if __name__ == "__main__":
    """""
        Parameters:
        args[0] --> Selects the dataset 
        possible inputs = "Stocknet" or "KDD17"
        args[1] = HDDM_A drift confidence (default value = 0.01)
    """""
    args = []

    if len(sys.argv) == 2:
        args.extend((sys.argv[1], 0.01))
    elif len(sys.argv) >= 3:
        args.extend((sys.argv[1], sys.argv[2]))
    else:
        args = input("Enter parameters: ").split(' ')
    if type(args[0]) is str:
        args[0] = args[0].lower()

    try:
        args[1] = float(args[1])
    except ValueError:
        print("Argument error: " + str(args[1]) + " not a valid drift confidence parameter")
        exit(-2)

    if args[0] == "stocknet" or args[0] == '0' or args[0] == 0:
        os.chdir("../../data/stocknet/raw")
    elif args[0] == "kdd17" or args[0] == '1' or args[0] == 1:
        os.chdir("../../data/kdd17/price_long_50")
    else:
        print("Argument error: " + str(args[1]) + " not a valid data-set")
        exit(-1)

    # Variable Declaration
    numberOfConcepts = [0]
    stocks = os.listdir('.')

    for stockName in stocks:
        data = pandas.read_csv(stockName, index_col="Date", parse_dates=["Date"])["Close"]

        # Detects drift for each stock
        hddmA = skmultiflow.drift_detection.hddm_a.HDDM_A(args[1])

        for i in range(len(data)):
            hddmA.add_element(data[i].item())

            if hddmA.detected_change():
                numberOfConcepts[-1] += 1
        print("Concept Drift occurred " + str(numberOfConcepts[-1]) + " times")
        numberOfConcepts.append(0)

    print("Average number of concept drifts: " + str(round(mean(numberOfConcepts))))
    print("Total number of drifts detected: " + str(sum(numberOfConcepts)))
    print("Stock " + stocks[numberOfConcepts.index(max(numberOfConcepts))][:-4] + " experienced the largest amount of concept drifts, with a total of " + str(max(numberOfConcepts)) + " concept drifts")


