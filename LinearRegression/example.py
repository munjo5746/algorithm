from LinearRegression import Regressor as linear
import numpy as np
import matplotlib.pyplot as plt

def generateData():
    data = np.random.standard_normal(100)

    sampled = np.random.choice([ele * 100 for ele in data], size=100, replace=True)
    return sampled.reshape((50,2))

if __name__ == "__main__":
    data = generateData()
    # fig = plt.figure()
    # axis = fig.add_subplot(1,1,1)
    # axis.scatter(data[:,0], data[:,1], color="blue")
    # plt.show()

    arr = np.array([[1,2,3], [3,4,5]])
    ins = linear(arr)
    ins.computeGeneralSSD(np.array([1,2]), np.array([3,4]))
