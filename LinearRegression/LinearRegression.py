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
        # check if the data is None
        if self.data is None:
            print "No data!"
            return

        # assumption is 2-D. check for dimension.
        r,c = self.data.shape
        if c != 2:
            print "Dimension does not match!"
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

    def computeGeneralSSD(self, weight):
        """
        This computes SSD in higher dimension. Unlike 2-D case of SSD, this
        function extends the dimension to general n-D case.
        The linear function in higher dimension, it can be represented as
        dot product of two vectors that have same dimension. So if we let
        t, v are in R^n, then t * v makes sense. But as in 2-D case, the linear
        function needs the y - intercept. So if we let t_0 = 1, then the original
        vector t is in {1} cross R^{n-1}.
        """

        if self.data is None:
            print "No data!"
            return
        # weight is {1, w_0, w_1, ...}
        rowVector = None
        try:
            rowVector = self.data[0, :] # first row
        except Exception as e:
            print e
            return

        # assumption is that the last column correspond to the real value
        # of each data. In 2-D case, this column is y component of (x,y).
        if len(rowVector) - 1 != len(weight):
            print "Dimension does not match!"
            return


        N = len(self.data[:, 0]) # number of data and each row is in R^n
        S = 0
        error = 0
        estimated = 0
        temp = None
        y = 0

        for v in self.data:
            temp = v[: len(v) - 1]
            y = v[len(v) - 1]
            estimated = np.dot(weight, temp)
            S += (y - estimated)**2
            print v
            print "estimated : %s" % estimated
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
            respSlope += (y - (slope * x + yIntercept)) * (-1 * x) * (1.0/N)
            respYIntercept += (-1 * (y - (slope * x + yIntercept))) * (1.0/N)
        newSlope = slope - (alpha * respSlope)
        newYIntercept = yIntercept - (alpha * respYIntercept)
        return (newSlope, newYIntercept)

    def computeLocalMin(self, initSlope, initY, iterations):
        newS = initSlope
        newY = initY
        for i in xrange(iterations):
            newS, newY = self.computeMinError(newS, newY, 0.5)
        return (newS, newY)
