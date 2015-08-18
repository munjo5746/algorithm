import numpy as np

class Regressor():
    def __init__(self, data):
        self.data = data

    def computeSSD(self, slope, yIntercept):
        """
        This function calculates the Sum of Square Difference for all data
        points with given slope and y-intercept. This will be our error function
        and the fomula is (1/N) Sum{y_i - (slope * x_i + b)**2}.
        """
        if self.data is None:
            print "No data!"
            return
        N = len(self.data) # data will be assumed as set of pairs.[(x_0,y_0), ...]
        S = 0
        error = 0
        estimated = 0
        for (x,y) in self.data:
            estimated = (slope * x) + yIntercept
            S += (y - estimated)**2
        error = float(S)/N
        return error

    def computeGeneralSSD(self, partial, yIntercept):
        """
        This computes SSD in higher dimension.
        """
        if self.data is None:
            print "No data!"
            return

        N = len(self.data[:, 0])
        S = 0
        error = 0
        estimated = 0
        temp = None

        for v in self.data:
            temp = v[ : len(v) - 1]
            estimated = np.add(np.dot(partial, temp), yIntercept)
            S += (v[len(v) - 1] - estimated)**2
        print S, N
        error = float(S)/N
        return error

    def computeMinError(self, slope, yIntercept, alpha):
        """
        This function will calculate the error for given slope and y-intercept.
        The alpha controls how far we should move at each iteration.
        """
        respSlope = 0
        respYIntercept = 0
        N = len(self.data)
        for (x,y) in self.data:
            respSlope += (y - (slope * x + yIntercept)) * (-1 * x)
            respYIntercept += (-1 * (y - (slope * x + yIntercept)))
        newSlope = slope - (alpha * respSlope)
        newYIntercept = yIntercept - (alpha * respYIntercept)
        return (newSlope, newYIntercept)

    def computeLocalMin(self, initSlope, initY, iterations):
        newS = initSlope
        newY = initY
        for i in xrange(iterations):
            newS, newY = self.computeMinError(newS, newY, 0.5)
        return (newS, newY)
