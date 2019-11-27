import pygame 
import math
import numpy as np

BLACK = (0,0,0)
RED = (255, 0,50)
GREEN = (0, 255, 50)

# Check if points are within screen range
def inBounds(point, loc, size):
	if point[0] >= loc[0] and point[0] <= loc[0]+size[0] and point[1] >= loc[1] and point[1] <= loc[1]:
		return True
	return False

# Helper function for intersecting lines
# Find the orientation of 3 points
def orientation(P1,P2,P3):
	o = (P2[1] - P1[1])*(P3[0] - P2[0]) - (P2[0] - P1[0])*(P3[1] - P2[1])

	if o == 0:
		return 0	#points are collinear

	return 1 if o > 0 else 2

# Finds whether or not two line segments intersect
def intersecting(P1, P2, Q1, Q2):
	o1 = orientation(P1, P2, Q1)
	o2 = orientation(P1, P2, Q2)
	o3 = orientation(Q1, Q2, P1)
	o4 = orientation(Q1, Q2, P2)

	if o1 != o2 and o3 != o4:
		return True

	return False

# We use this in the plotting to ensure no points go beyond our boundary
# Find the intersection point of 2 line segments
def intersectionPoint(P1,P2,Q1,Q2):
	# Equation of line P1,P2
	a1 = P2[1] - P1[1]
	b1 = P1[0] - P2[0]
	c1 = a1*P1[0] + b1*P1[1]

	# Equation of line Q1, Q2
	a2 = Q2[1] - Q1[1]
	b2 = Q1[0] - Q2[0]
	c2 = a2*Q1[0] + b2*Q1[1]

	determinant = a1*b2 - a2*b1

	if determinant == 0:
		#parallel lines
		return (None, None)

	else:
		x = (b2*c1 - b1*c2)/determinant
		y = (a1*c2 - a2*c1)/determinant
		p = [x,y]
		return p

class plotWindow:
	'''
	loc  - 2-tuple containing the x-y coord of the top left corner of the plot window
	size - 2-tuple containing the width and height of the window

	- we'll probably add colour parameters for the different type of plotting later
	'''
	def __init__(self, loc, size):
		self.size = size
		self.loc = loc

	def getDims(self):
		return [self.loc, self.size]

	def update(self,screen, score = None, message = None, iter_ratio = None):

		pygame.draw.line(screen, BLACK,  self.loc, (self.loc[0]+self.size[0],self.loc[1]), 4)
		pygame.draw.line(screen, BLACK,  self.loc, (self.loc[0],self.loc[1]+self.size[1]), 4)
		pygame.draw.line(screen, BLACK,  (self.loc[0]+self.size[0],self.loc[1]+self.size[1]), (self.loc[0]+self.size[0],self.loc[1]), 4)
		pygame.draw.line(screen, BLACK,  (self.loc[0]+self.size[0],self.loc[1]+self.size[1]), (self.loc[0],self.loc[1]+self.size[1]), 4)

		if score != None:
			score = min(1, score)
			score = max(0, score)
			font = pygame.font.Font('freesansbold.ttf', 25)
			colour = (int((1-score)* 255), int(score*255), 50)
			text = font.render("Score: " +str(int(score*100)) + "%",True,colour)
			screen.blit(text, (self.loc[0]+20, self.loc[1]+25 - int(text.get_height()/2)+1))

		if message != None:
			font = pygame.font.Font('freesansbold.ttf', 25)
			text = font.render(message,True,RED)
			screen.blit(text, (self.loc[0]+20, self.loc[1]+55 - int(text.get_height()/2)+1))

		if iter_ratio != None:
			x_len = iter_ratio * self.size[0] + self.loc[0]

			i = self.loc[0]

			pygame.draw.line(screen, BLACK,  (self.loc[0]+self.size[0],self.loc[1]+self.size[1]-27), (self.loc[0],self.loc[1]+self.size[1]-27), 2)

			while i < self.size[0] + self.loc[0]:
				if i < x_len:
					pygame.draw.rect(screen, GREEN, (i,self.loc[1]+self.size[1]-25,25,25), 0)
				pygame.draw.line(screen, BLACK, (i,self.loc[1]+self.size[1]-25), (i,self.loc[1]+self.size[1]), 2)
				i = i + 25

	'''
	data - list of ordered pairs to plotted (points only drawn if in the window)
	
	note: #pygame.draw.circle(screen, BLACK,(25,120),20,0) would draw a black circle
	of radius 20 at pos (25,120)
	
	- no return value
	'''
	def plotData(self, screen, data):

		data = [[int(point[0]), int(point[1])] for point in data]
		# Normalizing
		data = [[point[0]+self.loc[0], self.loc[1]+self.size[1] - point[1]] for point in data]

		for point in data: 
			# Out of range, dont plot
			if point[0] <= self.loc[0] or point[0] >= self.loc[0]+self.size[0] or point[1] <= self.loc[1] or point[1] >= self.loc[1]+self.size[1]:
				continue
			else:
				#plot the point as a very small, filled circle
				pygame.draw.circle(screen, BLACK, (point[0], point[1]),2)

	'''
	func - list of some of the x-y pairs of the function

	We want to connect adjacent x-y pairs with a line, this can done with:

	pygame.draw.line(screen, BLACK,  (x1,y1), (x2,y2), 4)

	(last param is line width just fyi)

	If a line would land outside of the window border we dont want to draw it and if
	its on the border we want draw it to the border and stop.

	- no return value here either
	'''
	def plotFunc(self, screen, points):

		points = [[int(point[0]), int(point[1])] for point in points]
		# Normalizing
		points = [[point[0]+self.loc[0], self.loc[1]+self.size[1] - point[1]] for point in points]

		n = len(points)
		for i in range(n-1):
			bound = False
			valid = None
			# If point 0 is in the valid range
			if self.loc[0] <= points[i][0] <= self.loc[0]+self.size[0] and self.loc[1] <= points[i][1] <= self.loc[1]+self.size[1]:
				# Both are in range, plot as is
				if self.loc[0] <= points[i+1][0] <= self.loc[0]+self.size[0] and self.loc[1] <= points[i+1][1] <= self.loc[1]+self.size[1]:
					pygame.draw.line(screen, BLACK, points[i], points[i+1], 4)
				# Point 1 is out of range, so (point[i], point[i+1]) intersects the plotting surface
				else:
					bound = True
					valid = points[i]

			# Point 0 is out of range
			else:
				# Point 1 is in range, so (point[i],point[i+1]) intersects the plotting surface
				if self.loc[0] <= points[i+1][0] <= self.loc[0]+self.size[0] and self.loc[1] <= points[i+1][1] <= self.loc[1]+self.size[1]:
					bound = True
					valid = points[i+1]
				# Both points are out of range
				else:
					continue

			if bound:
				l = None
				# Find which bound (point[i], point[i+1]) intersects and save it

				# Upper axis
				if intersecting(points[i], points[i+1], self.loc, [self.loc[0]+self.size[0],self.loc[1]]):
					l = [self.loc, [self.loc[0]+self.size[0],self.loc[1]]]
				# Left axis
				elif intersecting(points[i],points[i+1], self.loc, [self.loc[0],self.loc[1]+self.size[1]]):
					l = [self.loc, [self.loc[0],self.loc[1]+self.size[1]]]
				# Lower axis
				elif intersecting(points[i], points[i+1], [self.loc[0]+self.size[0], self.loc[1]+self.size[1]],[self.loc[0],self.loc[1]+self.size[1]]):
					l = [[self.loc[0],self.loc[1]+self.size[1]],[self.loc[0]+self.size[0], self.loc[1]+self.size[1]]]
				# Right axis
				elif intersecting(points[i], points[i+1], [self.loc[0]+self.size[0],self.loc[1]],[self.loc[0]+self.size[0],self.loc[1]+self.size[1]]):
					l = [[self.loc[0]+self.size[0],self.loc[1]],[self.loc[0]+self.size[0],self.loc[1]+self.size[1]]]

				# Error check	
				if l == None:
					print("Something went wrong: ", points[i+1])
					continue
				# Get the intersection point and draw a line from it to the valid point
				p = intersectionPoint(points[i], points[i+1], l[0], l[1])
				pygame.draw.line(screen, BLACK, valid, p,4)
