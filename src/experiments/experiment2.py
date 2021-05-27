"""
Experiment 2 was conducted in order to check how many concept drifts each concept drift detector detects in the KDD17
and the Stocknet dataset.
"""

import os
import pandas
import skmultiflow.drift_detection
import sys

from statistics import mean

if __name__ == "__main__":
    """""
    Parameters:
    args[0] --> Selects the concept drift detector
    possible inputs = "EDDM" or "HDDMa" or "HDDMw" or or "KSWIN" "PH"
    args[1] --> Selects the dataset 
    possible inputs = "Stocknet" or "KDD17"
    """""

    # Handle arguments
    args = []

    if len(sys.argv) >= 3:
        args.extend((sys.argv[1], sys.argv[2]))
    else:
        args = input("Enter parameters: ").split(' ')

    for i in range(len(args)):
        if type(args[i]) is str:
            args[i] = args[i].lower()

    if args[1] == "stocknet" or args[1] == '0' or args[1] == 0:
        os.chdir("../../data/stocknet/raw")
    elif args[1] == "kdd17" or args[1] == '1' or args[1] == 1:
        os.chdir("../../data/kdd17/price_long_50")
    else:
        print("Argument error: " + str(args[1]) + " not a valid data-set")
        exit(-1)

    # Variable Declaration
    numberOfConcepts = [0]
    stocks = os.listdir('.')

    for stockName in stocks:
        # Get data on each stock
        data = pandas.read_csv(stockName, index_col="Date", parse_dates=["Date"])["Close"]

        # Detect concepts for each stock
        if args[0] == "eddm" or args[0] == '0' or args[0] == 0:
            detector = skmultiflow.drift_detection.eddm.EDDM()
        elif args[0] == "hddma" or args[0] == '1' or args[0] == 1:
            detector = skmultiflow.drift_detection.hddm_a.HDDM_A()
        elif args[0] == "hddmw" or args[0] == '2' or args[0] == 2:
            detector = skmultiflow.drift_detection.hddm_w.HDDM_W()
        elif args[0] == "kswin" or args[0] == '3' or args[0] == 3:
            detector = skmultiflow.drift_detection.kswin.KSWIN()
        elif args[0] == "ph" or args[0] == '4' or args[0] == 4:
            detector = skmultiflow.drift_detection.page_hinkley.PageHinkley()
        else:
            print("Argument error: " + str(args[0]) + " is not a valid concept drift detector")
            exit(-4)

        previous = 0
        for i in range(len(data)):
            if args[0] == "eddm" or args[0] == '0' or args[0] == 0:
                if previous < data[i]:
                    detector.add_element(1)
                else:
                    detector.add_element(0)
                previous = data[i]
            else:
                detector.add_element(data[i])

            if detector.detected_change():
                numberOfConcepts[-1] += 1
        print("Concept Drift detected " + str(numberOfConcepts[-1]) + " times")
        numberOfConcepts.append(0)

    print("Average number of concept drifts detected: " + str(round(mean(numberOfConcepts))))
    print("Total number of drifts detected: " + str(sum(numberOfConcepts)))
    print("Stock " + stocks[numberOfConcepts.index(max(numberOfConcepts))][:-4] + " experienced the largest amount of concept drifts, with a total of " + str(max(numberOfConcepts)) + " detected concept drifts")
