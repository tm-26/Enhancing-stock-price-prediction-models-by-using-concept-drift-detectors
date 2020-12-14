This code is for the paper "Enhancing stock price prediction models by using concept drift detectors"

The detector.py file found in the Concept Drift Detector folder tests the HDDMa concept drift detector.
To make use of this file python 3.6.12 (or a more recent version) needs to be installed with the following libraries:
numpy = 1.14.5
pandas = 0.25.3
scikit-learn = 0.20.1
scipy = 1.1.0
tensorflow = 1.9.0


It takes in the following 4 arguments:
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

The models.py file found in the models folder tests three diffrent NN models.
To make use of this file python 3.7.7 (or a more recent version) needs to be installed with the following libraries:
mathplotlib >= 3.3.1
pandas >= 1.1.0
scikit-multiflow >= 0.5.3


It takes in the following 2 arguments:
 args[0] --> Selects the model
 possible inputs = "LSTM" or "ALSTM" or "Adv-Alstm"
 args[1] --> Selects the data-set 
 possible inputs = "ACL18" or "KDD17"

