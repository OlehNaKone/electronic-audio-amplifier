#! /usr/bin/python3

import tda7419
import os
import requests

if __name__ == "__main__":

    work_dir = os.path.split(os.path.abspath(__file__))[0]

    settings_file = os.path.join(work_dir,"settings.json")

    tda7419_chip1 = tda7419.tda7419(settings_file)

    tda7419_chip1.system_testing_mode(mode="Mon")
    tda7419_chip1.system_testing_mode(enable=True)
    tda7419_chip1.system_testing_mode(enable=False)
    tda7419_chip1.system_testing_mode(enable=True)
    tda7419_chip1.system_testing_mode(mode="Left_Volume")
    tda7419_chip1.system_testing_mode(enable=True)
    tda7419_chip1.system_testing_mode(enable=False)
    print("exit")

