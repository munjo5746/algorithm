from LinearRegression import Regressor as linear
import numpy as np
import matplotlib.pyplot as plt

def generateData():
    data = np.random.standard_normal(100)

    sampled = np.random.choice([ele * 100 for ele in data], size=100, replace=True)
    return sampled.reshape((50,2))

if __name__ == "__main__":
    data = generateData()
    instance = linear(data)

    error = 0
    x = range(10)
    y = range(10, 20)
    for (slope, yInt) in zip(x,y):
        error = instance.computeSSD(slope, yInt)
        print "slope : %s, y-Int : %s, error : %s" %(slope, yInt, error)
        error = 0
