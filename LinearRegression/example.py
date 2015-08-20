from LinearRegression import Regressor as linear
import numpy as np
import matplotlib.pyplot as plt

def generateData(dimension):
    data = np.random.standard_normal(100)

    sampled = np.random.choice([ele * 100 for ele in data], size=100, replace=True)
    return sampled.reshape((50,dimension))

if __name__ == "__main__":
    data = generateData(2)
    instance = linear(data)

    error = 0
    x = [np.random.randint(0,10) for i in range(10)]
    y = [np.random.randint(0,10) for i in range(10)]
    for (slope, yInt) in zip(x,y):
        error = instance.computeSSD(slope, yInt)
        print "slope : %s, y-Int : %s, error : %s" %(slope, yInt, error)
        error = 0
    t1 = 0
    t2 = 1
    error = 0
    for i in range(500):
        t1, t2 = instance.computeMinError(t1, t2, 0.001)
        error = instance.computeSSD(t1, t2)
        print "w1 : %s, w2 : %s, error : %s" %(t1,t2,error)
