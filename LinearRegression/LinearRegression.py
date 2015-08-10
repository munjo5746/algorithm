

class Regressor():
    def __init__(self, data):
        self.data = data

    def computeSSD(self, slope, yIntercept):
        """
        This function calculates the Sum of Square Difference for all data
        points with given slope and y-intercept. This will be our error function
        and the fomula is (1/N) Sum{y_i - (slope * x_i + b)**2}.
        """
        if slef.data is None:
            print "No data!"
            return
        N = len(self.data) # data will be assumed as set of pairs.[(x_0,y_0), ...]
        S = 0
        error = 0
        for (x,y) in data:
            S += (y - (slope * x) + b)**2
        error = float(S)/N
        return error
