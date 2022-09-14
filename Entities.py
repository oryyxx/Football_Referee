import math
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import logging
import cv2



class BaseEntity():
    def __init__(self, object, mapper_color = (255, 255, 255)):

        self.id = object.id
        self.object = object
        self.pointCloud = object.bounding_box
        self.point = pointcloud_to_2Dcoordinate(self.pointCloud)
        self.point2D = object.bounding_box_2d
        self.position = object.position
        self.raw_label = object.raw_label
        self.tracking_state = object.tracking_state
        self.mapper_color = mapper_color #NOT USING IT
        self.score = 0
        self.team = "A"
    
    def isPlayer(entity):

        if entity.raw_label == 0:
            return True
        else:
            return False

    def isBall(entity):

        #there could be more labels for the ball
        if entity.raw_label == 32 or entity.raw_label == 36:
            return True
        else:
            return False

    def isWanted(entity):
        return BaseEntity.isBall(entity) or BaseEntity.isPlayer(entity)

    def absDistance(point1, point2):
        try:
            return math. sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        except:
            return 100

    def isIntersect(points, start, end):

        point = getMid(points[0], points[len(points)-1])

        if point[0] >= start[0] and point[0] <= end[0]:

            if point[1] >= start[1] and point[1] <= end[1]:
                return True

        return False
    

    def PredictTeam(image, entity):

        try:

            x = entity.point2D[0][0]
            y = entity.point2D[0][1]
            w = entity.point2D[2][0] - x
            h = entity.point2D[2][1] - y

            y = int(y + y * 0.2)
            h = int(h - h * 0.4)

            # cv2.rectangle(image, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)

            bar = MostColor(image, x, y, w, h)
            entity.team = is_b_or_w(bar)

        except Exception as e:
            logging.error("The error raised is: ", e)

class ball_pre:
    def __init__(self, ballpre):
        self.ball_pre = ballpre


def getMid(point1, point2):

    sumx = point1[0] + point2[0]
    sumy = point1[1] + point2[1]

    avgx = int(sumx/2)
    avgy = int(sumy/2)

    return (avgx, avgy)


def MostColor(image, x, y, w, h):

  crop = []
  crop = image[int(y):int(y+h), int(x):int(x+w)]

  crop = crop.reshape((crop.shape[0] * crop.shape[1], 4)) #(width, height, 4)  ====> (width*height, 4)

  #Find the dominate color
  clt = KMeans(n_clusters = 1)
  clt.fit(crop)

  hist = centroid_histogram(clt)
  bar = plot_colors(hist, clt.cluster_centers_)

  return bar

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		# cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
		# 	color.astype("uint8").tolist(), -1)
		# startX = endX
	
	# return the bar chart
	return bar

def is_b_or_w(image, black_max_bgr=(100, 100, 100)):

    mean_bgr_float = np.mean(image, axis=(0,1))
    mean_bgr_rounded = np.round(mean_bgr_float)
    mean_bgr = mean_bgr_rounded.astype(np.uint8)

    mean_intensity = int(round(np.mean(image)))
    
    return 'black' if np.all(mean_bgr < black_max_bgr) else 'white'

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

#estimates object coordinate on 2D plane from 8 data points
def pointcloud_to_2Dcoordinate(points):

    sumx = 0
    sumz = 0

    if len(points) == 0:
        return

    for i in range(0, 7):
        
        x = points[i][0]
        z = points[i][2]

        sumx += x
        sumz += z

    x = round((sumx / 7), 2) 
    z = round((sumz / 7), 2) 

    return x, z

