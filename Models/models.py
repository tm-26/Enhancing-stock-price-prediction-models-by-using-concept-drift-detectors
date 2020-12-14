# This code makes uses of these three NN models: https://github.com/fulifeng/Adv-ALSTM

import os
import sys

if __name__ == "__main__":
    """""
        Parameters:
        args[0] --> Selects the model
        possible inputs = "LSTM" or "ALSTM" or "Adv-Alstm"
        args[1] --> Selects the data-set 
        possible inputs = "ACL18" or "KDD17"
    """""

    os.chdir("Adv-ALSTM")

    # Get arguments
    args = []

    if len(sys.argv) >= 3:
        args.extend((sys.argv[1], sys.argv[2]))
    else:
        args = input("Enter parameters: ").split(" ")

    for i in range(len(args)):
        if type(args[i]) is str:
            args[i] = args[i].lower()

    if args[1] == "acl18" or args[1] == '0' or args[1] == 0:
        if args[0] == "lstm" or args[0] == '0' or args[0] == 0:
            os.system("python pred_lstm.py -a 0 -l 10 -u 32 -l2 10 -f 1")
        elif args[0] == "alstm" or args[0] == '1' or args[1] == 0:
            os.system("python pred_lstm.py -l 5 -u 4 -l2 1 -f 1")
        elif args[0] == "adv-alstm" or args[0] == "advalstm" or args[0] == '2' or args[0] == 2:
            os.system("python pred_lstm.py -l 5 -u 4 -l2 1 -v 1 -rl 1 -q ./saved_model/acl18_alstm/exp -la 0.01 -le 0.05")
    elif args[1] == "kdd17" or args[1] == '1' or args[1] == 1:
        if args[0] == "lstm" or args[0] == '0' or args[1] == 0:
            os.system("python pred_lstm.py -p ./data/kdd17/ourpped/ -l 5 -u 4 -l2 0.001 -a 0 -f 1")
        elif args[0] == "alstm" or args[0] == '1' or args[1] == 1:
            os.system("python pred_lstm.py -p ./data/kdd17/ourpped/ -l 15 -u 16 -l2 0.001 -f 1")
        elif args[0] == "adv-alstm" or args[0] == "advalstm" or args[0] == '2' or args[1] == 2:
            os.system("python pred_lstm.py -p ./data/kdd17/ourpped/ -l 15 -u 16 -l2 0.001 -v 1 -rl 1 -q ./saved_model/kdd17_alstm/model -la 0.05 -le 0.001 -f 1")
        else:
            print("Argument error: " + str(args[0]) + " not a valid ML model")
    else:
        print("Argument error: " + str(args[1]) + " not a valid data-set")
