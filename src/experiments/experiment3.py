"""
Experiment 3 tests for type II errors by testing the concept drift detectors on ten different periods in time where
concept drift occurred beyond any unreasonable doubt.
"""


import os
import pandas
import skmultiflow.drift_detection
import sys

if __name__ == "__main__":
    """""
    Parameters:
    args[0] --> Selects the concept drift detector
    possible inputs = "EDDM" or "HDDMa" or "HDDMw" or or "KSWIN" "PH"
    """""

    # Get arguments
    detectorType = None

    if len(sys.argv) >= 2:
        detectorType = sys.argv[1]
    else:
        detectorType = input("Enter parameter: ").split(' ')[0]

    if type(detectorType) is str:
        detectorType = detectorType.lower()

    # Variable Declaration
    beforeEvents = []
    duringEvents = []
    afterEvents = []
    stocks = os.listdir("../../data/historicalEvents")
    detector = None

    for counter, stockName in enumerate(stocks):
        # Get data on each stock
        data = pandas.read_csv("../../data/historicalEvents/" + stockName, index_col="Date", parse_dates=["Date"])["Close"]

        # Detect concepts for each stock
        if detectorType == "eddm" or detectorType == '0' or detectorType == 0:
            detector = skmultiflow.drift_detection.eddm.EDDM()
        elif detectorType == "hddma" or detectorType == '1' or detectorType == 1:
            detector = skmultiflow.drift_detection.hddm_a.HDDM_A()
        elif detectorType == "hddmw" or detectorType == '2' or detectorType == 2:
            detector = skmultiflow.drift_detection.hddm_w.HDDM_W()
        elif detectorType == "kswin" or detectorType == '3' or detectorType == 3:
            detector = skmultiflow.drift_detection.kswin.KSWIN()
        elif detectorType == "ph" or detectorType == '4' or detectorType == 4:
            detector = skmultiflow.drift_detection.page_hinkley.PageHinkley()
        else:
            print("Argument error: " + str(detectorType) + " is not a valid concept drift detector")
            exit(-4)

        status = 0
        previous = 0
        previousMonth = data.index[0].month
        beforeEvent = 0
        duringEvent = 0
        afterEvent = 0
        for i in range(len(data)):

            if previousMonth != data.index[0].month:
                status += 1

            previousMonth = data.index[i].month

            if detectorType == "eddm" or detectorType == '0' or detectorType == 0:
                if previous < data[i]:
                    detector.add_element(1)
                else:
                    detector.add_element(0)
                previous = data[i]
            else:
                detector.add_element(data[i])
            if detector.detected_change():
                if status == 0:
                    beforeEvent += 1
                elif status == 1:
                    duringEvent += 1
                else:
                    afterEvent += 1
        print("-------------------------------Event #" + str(counter) + "---------------------------------")
        print("Concept Drifts detected before event " + str(beforeEvent) + " times")
        print("Concept Drifts detected during event " + str(duringEvent) + " times")
        print("Concept Drifts detected after event " + str(afterEvent) + " times")
        print("------------------------------------------------------------------------")

        beforeEvents.append(beforeEvent)
        duringEvents.append(duringEvent)
        afterEvents.append(afterEvent)

    print("-------------------------------Total---------------------------------")
    print("Concept Drifts detected before events " + str(sum(beforeEvents)) + " times")
    print("Concept Drifts detected during events " + str(sum(duringEvents)) + " times")
    print("Concept Drifts detected after events " + str(sum(afterEvents)) + " times")
    print("------------------------------------------------------------------------")
