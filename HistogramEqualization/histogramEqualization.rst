Histogram Equalization
======================

The **Histogram Equalization** is an algorithm to increase the contrast of the input image. If an image's pixel intensities are distributed largely in certain range, the objects in the image will be difficult to distincguish. An example would be the image both foreground and background are dark or bright. By increasing the global contrast of the image, it easier to see the objects. The idea is that distribute the most frequent pixel intensities equally over the intensity range which is same as flatten the pixel intensities. The steps of the algorithm is following.

	1. For given image :math:`I_{i, j}`, we first need to find the probability distribution of the pixel intensities. Let :math:`N` be the total number of pixels, :math:`n_i` be the number of pixels at the intensity level :math:`i`. Then, the probability distribution :math:`p(x=i)` will be defined as :math:`p(x=i) = \frac{n_i}{N}` for :math:`i = 0, 1, \ldots, L`.
	2. Then, define the **cumulative distribution function** :math:`cdf(x=i)` as :math:`cdf(x=i) = \sum_{k=0}^{L} p(x=k).` 
	3. Then, the transformed image :math:`I'_{i,j}` can be found by :math:`I'_{i,j} = floor(L * cdf(x=I_{i,j}))` 

