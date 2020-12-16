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
        args[1] --> Is used to decide which concept drift detector is going to be used
        where:
            0 = EDDM
            1 = HDDMa
            2 = HDDMw
            3 = PH
    """""
    args = []

    if len(sys.argv) < 3:
        args = input("Enter parameters: ").split(" ")
        if len(args) < 2:
            print("Argument error: Not enough arguments passed")
            exit(-3)
    else:
        args.extend((sys.argv[1], sys.argv[2]))

    args = list(map(float, args))

    for arg in args:
        if not (type(arg) is int or type(arg) is float):
            print("Argument error: " + str(arg) + " is neither an int or a float")
            exit(-1)
        elif int(arg) < 0:
            print("Argument error: " + str(arg) + " is invalid")
            exit(-2)

    # Variable Declaration

    numberOfConcepts = [0]
    dataset = "data/kdd17"

    if args[0] == 0:
        dataset = "data/acl18"

    stocks = os.listdir(dataset)

    # Get Data
    for stockName in stocks:
        data = pandas.read_csv(dataset + '/' + stockName, index_col="Date", parse_dates=["Date"])["Close"]

        # Detect concepts for each stock
        detector = ''
        if args[1] == 0:
            detector = skmultiflow.drift_detection.eddm.EDDM()
        elif args[1] == 1:
            detector = skmultiflow.drift_detection.hddm_a.HDDM_A()
        elif args[1] == 2:
            detector = skmultiflow.drift_detection.hddm_w.HDDM_W()
        elif args[1] == 3:
            detector = skmultiflow.drift_detection.kswin.KSWIN()
        elif args[1] == 4:
            detector = skmultiflow.drift_detection.page_hinkley.PageHinkley()
        else:
            print("Argument error: " + str(args[1]) + " is not a valid concept drift detector")
            exit(-4)

        previous = 0
        for i in range(len(data)):
            if args[1] == 0:
                if previous < data[i]:
                    detector.add_element(1)
                else:
                    detector.add_element(0)
                previous = data[i]
            else:
                detector.add_element(data[i])

            if detector.detected_change():
                numberOfConcepts[-1] += 1
        print("Concept Drift occurred " + str(numberOfConcepts[-1]) + " times")
        numberOfConcepts.append(0)

    print("Average number of concept drifts: " + str(round(mean(numberOfConcepts))))
    print("Total number of drifts detected: " + str(sum(numberOfConcepts)))
    print("Stock " + stocks[numberOfConcepts.index(max(numberOfConcepts))][:-4] + " experienced the largest amount of concept drifts, with a total of " + str(max(numberOfConcepts)) + " concept drifts")
