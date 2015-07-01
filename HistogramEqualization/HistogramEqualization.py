import numpy as np
import matplotlib.pyplot as plt
import cv2

class HistogramEqualization:
	def __init__(self, image):
		# assume that image is grayscale image
		self.image = image
		self.equalized = None
		self.row = image.shape[0]
		self.col = image.shape[1]
		self.totalPixels = 0
		self.probabilityDistribution = {}
		self.cdf = {}

	def getProbabilityDistribution(self):
		if self.image is None:
			print "image is Null!"
			return

		for i in range(256):
			self.probabilityDistribution[i] = 0

		for i in range(self.row):
			for j in range(self.col):
				self.totalPixels = self.totalPixels + 1
				self.probabilityDistribution[self.image[i,j]] = self.probabilityDistribution[self.image[i,j]] + 1

		for key in self.probabilityDistribution.keys():
			self.probabilityDistribution[key] = self.probabilityDistribution[key]/(self.totalPixels * 1.0)


	def getCdf(self):
		if len(self.probabilityDistribution) == 0:
			print "probabilityDistribution is not calculated!"
			return

		for i in range(256):
			self.cdf[i] = 0

		for cdfkey in self.cdf.keys():
			for distkey in self.probabilityDistribution.keys():
				self.cdf[cdfkey] = self.probabilityDistribution[distkey] + self.cdf[cdfkey]
				if cdfkey == distkey:
					break

	def equalize(self):
		if len(self.cdf) == 0:
			print "cdf is not calculated!"
			return

		copyImg = np.zeros((self.row, self.col))

		for i in range(self.row):
			for j in range(self.col):
				L = 256 - 1
				copyImg[i, j] = self.cdf[self.image[i, j]] * L

		self.equalized = copyImg


if __name__ == "__main__":
	print "Equalizing..."
	img = cv2.imread("test.jpg", 0)
	ins = HistogramEqualization(img)
	ins.getProbabilityDistribution()
	ins.getCdf()
	ins.equalize()
	plt.tick_params(labelbottom="off", labeltop="off")
	plt.subplot(2,2,1)
	plt.title("Original")
	plt.imshow(cv2.imread("test.jpg"))
	plt.subplot(2,2,2)
	plt.title("Original Histogram")
	plt.hist(img.flatten(), 256, range=(0, 255), fc='k')
	plt.subplot(2,2,3)
	plt.title("Equalized")
	plt.imshow(ins.equalized, cmap=plt.cm.Greys_r)
	plt.subplot(2,2,4)
	plt.title("Equalized Histogram")
	plt.hist(ins.equalized.flatten(), 256, range=(0, 255), fc='k')
	plt.show()



