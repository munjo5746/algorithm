# Otsu's thresholding
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage.data import camera, page
import numpy as np
import time
from skimage.filter import threshold_otsu
from copy import deepcopy

def padwithtens(vector, pad_width, iaxis, kwargs):
	vector[:pad_width[0]] = 0
	vector[-pad_width[1]:] = 0
	return vector

class adaptive_otsu():
	"""implementation of otsu's thresh"""
	def __init__(self, img=None):
		
		self.img = img
		self.row, self.col = img.shape
		# dictionary type.
		self.dist = None
		self.first_moment = {}
		self.second_moment = {}
		self.T = 0

	def distribution(self):
		if self.img == None:
			print "No image!"
			return
		else:
			# map from intensity to freq.
			flatten_img = self.img.flatten()

			self.dist = np.array([0 for i in xrange(256)])

			for intensity in flatten_img:
				self.dist[intensity] += 1
		if len(self.dist) == 0:
			print "Distribution not found!"
			return
		else:
			r, c = self.img.shape
			t = r*c # total number of pixels.
			self.dist = self.dist * (1.0/t)
		# print self.dist
		# print "Distribution found successfully!"

		intensity = 1
		T = 0
		for prob in self.dist:
			T += intensity * prob
			intensity += 1
		self.T = T
		return

	def variance(self, k):
		# return optimal thresholding value.
		w = np.sum(self.dist[1:k+1])
		# print w
		intensity = 1 # if set this equal to 0, it does not work. why??
		u = 0
		for prob in self.dist[1:k+1]:
			u += intensity * prob
			intensity += 1
		# print "first moment : ", u		
		sigma = ((self.T * w - u)**2)/(w*(1-w))
		return sigma

	def otsu(self):
		# self.distribution()
		opt = 0
		max_variance = 0
		for k in xrange(1,256):
			var = self.variance(k)
			# print var
			if var > max_variance:
				max_variance = var
				var = 0
				opt = k

		return opt

	def adaptive_none(self, grid_number):
		# First divide the image into number of grid.
		# Total, grid_number^2 number of grids.
		# 7, 5 are not working
		x, y = 0, 0
		img = deepcopy(self.img)
		while(True):
			# Find left upper corner only.
			if x + grid_number >= self.col and y + grid_number >= self.row:
				# at last grid.
				subimg = self.img[y: , x: ]
				opt = threshold_otsu(subimg)
				img[y:, x:] = self.img[y:, x:] > opt
				break
			elif x + grid_number >= self.col and y + grid_number < self.row:
				# at the right edge.
				subimg = self.img[y : y + grid_number, x :]
				opt = threshold_otsu(subimg)
				img[y : y + grid_number, x :] = self.img[y : y + grid_number, x :] > opt
				y = y+grid_number
				x = 0
			elif x + grid_number < self.col and y + grid_number >= self.row:
				subimg = self.img[y : , x : x + grid_number]
				opt = threshold_otsu(subimg)
				img[y : , x : x + grid_number] = self.img[y : , x : x + grid_number] > opt
				# print self.img[y : , x : x + width]
				x = x + grid_number
			else:
				subimg = self.img[y : y + grid_number, x : x + grid_number]
				opt = threshold_otsu(subimg)
				img[y : y + grid_number, x : x + grid_number] = self.img[y : y + grid_number, x : x + grid_number] > opt				
				# print self.img[y : y + height, x : x + width]
				x = x+grid_number

		return img

	def adaptive_overap(self, grid_size):
		# Assumption is that the grid_size is odd positive integer. 
		# otherwise, we can't make the current pixel placed at the center of the patch.
		if grid_size % 2 == 0:
			print "Odd number required!"
			return

		# we want to make the current pixel placed at the center of the patch.
		# if we can't, then make the patch using appropriate size.
		patch_size = grid_size/2
		start_row, end_row = 0, 0
		start_col, end_col = 0, 0
		img_copy = self.img
		for y in xrange(self.row):
			for x in xrange(self.col):
				# check if we are near the left edge.
				# handles col of the patch.
				if patch_size <= x and patch_size + x < self.col:
					# we are at the middle.
					start_col = x - patch_size
					end_col = x + patch_size
				elif x < patch_size:
					# when patch_size - (x+1) == 0, the number of pixels to the left
					# is patch_size-1.
					start_col = 0
					end_col = x + patch_size
				elif patch_size + x >= self.col:
					# we are at near the right edge.
					start_col = x - patch_size
					end_col = self.col - 1

				# handles row of the patch.
				if patch_size <= y and patch_size + y < self.row:
					# we are at the middle.
					start_row = y - patch_size
					end_row = y + patch_size
				elif y < patch_size:
					start_row = 0
					end_row = y + patch_size
				elif patch_size + y >= self.row:
					# we are at the bottom of the image.
					start_row = y - patch_size
					end_row = self.row - 1

				subimg = self.img[start_row:end_row+1, start_col:end_col+1]
				threshold = threshold_otsu(subimg)
				img_copy[y,x] = img_copy[y,x] > threshold

		return img_copy

if __name__=="__main__":
	# ###### Test cases.
    

	# ######Regular otsu.
	# regular_otsu = adaptive_otsu(camera())
	# regular_otsu.distribution() # find prob. dist.
	# threshold = regular_otsu.otsu()
	# binary_img = camera() > threshold

	# plt.figure(1)
	# plt.subplot(1,2,1)
	# plt.imshow(camera(), cmap=plt.cm.gray)
	# plt.subplot(1,2,2)
	# plt.imshow(binary_img, cmap=plt.cm.gray)




	# ## adaptive otsu - non-overwrap
	# ## ###############################
	# ## For non-overwrap, the mask size is tested with 25, 30, 50. 
	# ## Some other mask size did not work because numpy libray complains
	# ## about argmax. 
	# ################################
	# plt.figure(2)
	# non_overwrap = adaptive_otsu(page())
	# start = time.time() # measuring time.
	# non_img = non_overwrap.adaptive_none(25) 
	# end = time.time() # measuring time.
	# print "Otsu none overwrap method took : %s" % (end-start)
	# plt.subplot(1,2,1)
	# plt.imshow(page(), cmap=plt.cm.gray)
	# plt.subplot(1,2,2)
	# plt.imshow(non_img, cmap=plt.cm.gray)

	# ########################################
	# ## overwrap otsu tested with mask size 11, 13, 21. 
	# ## NOTE : ONLY odd square matrix is accepted in order to make current pixel 
	# ##        at the center of the mask.
	# ######################################
	# plt.figure(3)
	# overwrap = adaptive_otsu(page())
	# start = time.time() # measuring time.
	# overwrap_img = overwrap.adaptive_overap(21)
	# end = time.time() # measuring time.
	# print "Otsu overwrap method took : %s" % (end-start)
	# plt.subplot(1,2,1)
	# plt.imshow(page(), cmap=plt.cm.gray)
	# plt.subplot(1,2,2)
	# plt.imshow(overwrap_img, cmap=plt.cm.gray)
	# plt.show()

	# img = imread("wiki.jpg")
	# plt.figure(1)
	# non_overwrap = adaptive_otsu(img)
	# non_img = non_overwrap.adaptive_none(40) 
	# plt.subplot(1,2,1)
	# plt.imshow(img, cmap=plt.cm.gray)
	# plt.subplot(1,2,2)
	# plt.imshow(non_img, cmap=plt.cm.gray)
	img = imread("wiki.jpg")
	overwrap = adaptive_otsu(img)
	start = time.time() # measuring time.
	overwrap_img = overwrap.adaptive_overap(21)
	end = time.time() # measuring time.
	print "Otsu overwrap method took : %s" % (end-start)
	plt.subplot(1,2,1)
	plt.imshow(img, cmap=plt.cm.gray)
	plt.subplot(1,2,2)
	plt.imshow(overwrap_img, cmap=plt.cm.gray)
	plt.show()