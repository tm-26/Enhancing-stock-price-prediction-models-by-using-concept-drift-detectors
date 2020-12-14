import matplotlib.pyplot
import os
import pandas
import skmultiflow.drift_detection
import sys

from statistics import mean

if __name__ == "__main__":
    """""
        Parameters:
        args[0] --> Controls which data-set is going to be used:
        where:
            0 = ACL18
            Bigger then 0 = KDD17
        args[1] --> Is used to decide if graphs are going to be plotted or not
        where:
            0 = Don't plot graphs
            Bigger then 0 = Plot graphs
        args[2] = HDDM_A Drift Confidence
        where:
            0 = default value (0.01)
        args[3] = HDDM_A Warning Confidence
        where:
            0 = default value (0.05)
    """""
    args = []

    if len(sys.argv) < 4:
        args = input("Enter parameters: ").split(" ")
        if len(args) < 4:
            print("Argument error: Not enough arguments passed")
            exit(-3)
    else:
        args = sys.argv

    args = list(map(float, args))

    for arg in args:
        if not (type(arg) is int or type(arg) is float):
            print("Argument error: " + arg + " is neither an int or a float")
            exit(-1)
        elif int(arg) < 0:
            print("Argument error: " + arg + " is invalid")
            exit(-2)

    # Variable Declaration

    numberOfConcepts = [0]
    dataset = ''

    if args[0] == 0:
        dataset = "data/acl18"
    else:
        dataset = "data/kdd17"

    if args[2] == 0:
        args[2] = 0.001
    if args[3] == 0:
        args[3] = 0.005

    stocks = os.listdir(dataset)

    # Get Data
    for stockName in stocks:
        data = pandas.read_csv(dataset + '/' + stockName, index_col="Date", parse_dates=["Date"])["Close"]

        if args[1] == 1:
            previous = 0
            currentColor = 'b'
            matplotlib.pyplot.figure(figsize=(16, 8))
            matplotlib.pyplot.title("Close Price History of " + stockName[:-4] + " Stocks")
            matplotlib.pyplot.xlabel("Date", fontsize=18)
            matplotlib.pyplot.ylabel("Close Price USD ($)", fontsize=18)

        # Detect concepts for each stock
        hddmA = skmultiflow.drift_detection.hddm_a.HDDM_A(args[2], args[3])

        for i in range(len(data)):
            hddmA.add_element(data[i])

            if hddmA.detected_change():
                if args[1] == 1:
                    matplotlib.pyplot.plot(data[previous:i], currentColor)
                    previous = i - 1
                    if currentColor == 'b':
                        currentColor = 'r'
                    else:
                        currentColor = 'b'
                numberOfConcepts[-1] += 1
        print("Concept Drift occurred " + str(numberOfConcepts[-1]) + " times")
        numberOfConcepts.append(0)

        if args[1] == 1:
            matplotlib.pyplot.show()
    print("Average number of concept drifts: " + str(round(mean(numberOfConcepts))))
    print("Total number of drifts detected: " + str(sum(numberOfConcepts)))
    print("Stock " + stocks[numberOfConcepts.index(max(numberOfConcepts))][:-4] + " experienced the largest amount of concept drifts, with a total of " + str(max(numberOfConcepts)) + " concept drifts")
