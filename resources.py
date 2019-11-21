import pygame 
import math
import numpy as np

BLACK = (0,0,0)

#hardcoded bounds check
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

	def update(self,screen, score = None):

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

'''
Some notes:

Throughout the comments in this code a "*" after an id (like identifier*) indicates that identifier is
initially a parameter or attribute of the constructor of the class 
'''

'''
--- Slider Class ---
	Attributes:

	-- loc*          -- 2-tuple containing the x-y coord of the top left of the slider, 
	-- size*         -- 2-tuple containing the width and height of the slider,
	-- valueRange*   -- ordered list of values of the slider,
	-- defaultValue* -- index of the default value in valueRange,
	-- varName*      -- string containing the title of the slider
	-- var           -- stored the index (in valueRange) of the current value of the slider

	Methods:

	-- getVal --
		returns the the current value of the slider

	-- update --
		under the assumption that mouse is pressed at the given position, the index of the current 
		value of the slider is updated if needed

	-- draw --
		draws the slider

	-- getLoc --
		returns the location of the slider

'''
class Slider:
	def __init__(self, loc, size, valueRange, defaultValue, varName):
		self.valueRange = valueRange 
		self.size = size
		self.loc = loc
		self.var = defaultValue
		self.varName = varName
	
	def getVal(self):
		return self.valueRange[self.var]

	def update(self, m_pos):
		if self.loc[0]-10 <= m_pos[0] <= self.loc[0]+self.size[0]+10 and self.loc[1] - self.size[1]/2-5 <= m_pos[1] <= self.loc[1]+self.size[1]/2 + 5:
			relativePos = (m_pos[0] - self.loc[0])/self.size[0]
			if relativePos > 1:
				relativePos = 1
			elif relativePos < 0:
				relativePos = 0
			self.var = int(relativePos * (len(self.valueRange) - 1))	
			return True
		return False

	def draw(self, screen):

		# Horizontal line of slider
		pygame.draw.line(screen, BLACK,  self.loc, (self.loc[0] + self.size[0], self.loc[1]), 2)

		# Var location
		x_pos = int((self.var+1) / len(self.valueRange) * self.size[0] + self.loc[0])
		pygame.draw.line(screen, BLACK,  (x_pos, self.loc[1] - self.size[1]), (x_pos, self.loc[1] + self.size[1]), 4)

		# End points
		pygame.draw.line(screen, BLACK,  (self.loc[0], self.loc[1] - (3*self.size[1])//4), (self.loc[0], self.loc[1] + (3*self.size[1])//4), 2)
		pygame.draw.line(screen, BLACK,  (self.loc[0]+self.size[0], self.loc[1] - (3*self.size[1])//4), (self.loc[0]+self.size[0], self.loc[1] + (3*self.size[1])//4), 2)
		
		font = pygame.font.Font('freesansbold.ttf', self.size[1]*2)
		text = font.render(self.varName + ": " + str(round(self.valueRange[self.var],5)),True,BLACK)
		screen.blit(text, (self.loc[0]+self.size[0]+10, self.loc[1] - int(text.get_height()/2)+1))
		
	def getLoc(self):
		return self.loc


'''
--- Options Class ---
	Attributes:

	-- loc*          -- 2-tuple containing the x-y coord of the top left of the options, 
	-- size*         -- size of the options bar,
	-- options*      -- ordered list of options (strings),
	-- defaultValue* -- index of the default option in options,
	-- title*        -- string containing the title of the options,
	-- var           -- stored the index (in options) of the current value of the options

	Methods:

	-- update --
		under the assumption that mouse is clicked at the given position, the index of the current 
		value of the options is updated if needed

	-- draw --
		draws the options

'''
class Options:
	def __init__(self, loc, size, options, defaultValue, title):
		self.loc = loc
		self.size = size
		self.options = options
		self.var = defaultValue
		self.title = title

	def getVal(self):
		return self.var

	def update(self, m_pos, click, pressed):

		if not click:
			return False 
		size1 = int(self.size * 3/4)
		for i in range(len(self.options)):
			if self.loc[0] <= m_pos[0] <= self.loc[0]+size1 and self.loc[1]+(i+1)*self.size+3 <= m_pos[1] <= self.loc[1]+(i+1)*self.size+3 + size1:
				self.var = i
				return True
		return False
		
	
	def draw(self, screen):
		font = pygame.font.Font('freesansbold.ttf', self.size)
		text = font.render(self.title,True,BLACK)
		screen.blit(text, self.loc)
		
		
		size1 = int(self.size * 3/4)
		size2 = int(0.7*size1)
		ds = int((size1-size2)/2)+1		

		for i in range(len(self.options)):
			pygame.draw.rect(screen, BLACK, (self.loc[0],self.loc[1]+(i+1)*self.size+5,size1,size1), 2)			
			
			if i == self.var:
				pygame.draw.rect(screen, BLACK, (self.loc[0]+ds ,self.loc[1]+(i+1)*self.size+5+ds,size2,size2), 0)

			font = pygame.font.Font('freesansbold.ttf', self.size)
			text = font.render(self.options[i],True,BLACK)
			screen.blit(text, (self.loc[0]+self.size, self.loc[1]+5+(i+1)*self.size))
			

'''
--- Button Class ---
	Attributes:

	-- loc*     -- 2-tuple containing the x-y coord of the top left of the button, 
	-- size*    -- 2-tuple containing the width and height of the button,
	-- varName* -- string containing the title of the buttons,
	-- pushed   -- bool denoting whether or not the button is currently pressed

	Methods:

	-- update --
		under the assumption that mouse is clicked at the given position, the pushed attribute is
		updated if needed

	-- draw --
		draws the button
'''
class Button:
	def __init__(self, loc, size, varName, textSize):
		self.size = size
		self.loc = loc
		self.varName = varName
		self.clicked = False
		self.pushed = False
		self.textSize = textSize

	def getVal(self):
		return self.clicked

	def update(self, m_pos, click, pressed):
		T = self.loc[0] <= m_pos[0] <= self.loc[0] + self.size[0] and self.loc[1] <= m_pos[1] <= self.loc[1] + self.size[1]
			
		if T and click:
			self.clicked = True
		else:
			self.clicked = False
		if T and pressed:
			self.pushed = True
		else:
			self.pushed = False	 
			

	def draw(self, screen):
		pygame.draw.rect(screen, BLACK, (self.loc[0],self.loc[1],self.size[0],self.size[1]), 5)

		font = pygame.font.Font('freesansbold.ttf', self.textSize)
		text = font.render(self.varName,True,BLACK)

		w = text.get_width()
		h = text.get_height()

		screen.blit(text, (self.loc[0]+max((self.size[0] - w)//2, 0) , self.loc[1]+max((self.size[1] - h)//2,0)))

		if self.pushed:
			diff = min(6, self.size[0]//15)
			pygame.draw.rect(screen, BLACK, (self.loc[0]+diff,self.loc[1]+diff,self.size[0]-2*diff,self.size[1]-2*diff), 4)


'''
--- GradientDescent Function ---
	
	*gradient computed is for linear regression

	Parameters:

	-- X          -- numpy matrix of training examples as rows (m by n matrix),
	-- y          -- corresponding y-values of the training examples in X,
	-- alpha      -- learning rate,
	-- lmda       -- regularization parameter,
	-- iters      -- number of iterations to run the GD algorithm,
	-- batch_size -- Size of batchs in GD, if batch_size >= m, the reasulting algorithm is batch GD,
	-- init_theta -- initial value of theta

	Returns the new theta value after the specified number of iterations
'''
def gradientDescent(X, y, alpha, lmda, iters, batch_size, init_theta):
	
	m,n = X.shape
	
	theta = init_theta

	if batch_size > m:
		batch_size = m

	for i in range(iters):
		
		if batch_size < m:
			T = np.concatenate((X,y),axis=1)

			np.random.shuffle(T)

			X = T[:,0:n]
			y = T[:,n]
		
		for j in range(m // batch_size):

			X_new = X[j*batch_size: min((j+1)*batch_size, m)]
			y_new = y[j*batch_size: min((j+1)*batch_size, m)]

			temp = theta
			theta = temp - (alpha / batch_size) * (np.transpose(X_new) * (X_new*temp - y_new) - lmda * temp)

	return theta


def powerMatrix(xVals, order):

	X = [[x**i for i in range(order+1)] for x in xVals]

	return np.matrix(X)

def avgCost(theta, X, y):

	m = X.shape[0]

	delta = X * theta - y
	
	err = np.transpose(delta) * (1/(2*m) * delta)

	err = err.tolist()[0][0] 

	err = min(err, 1000000000000)

	return 1/(1+(abs(err) / 1000  + err**2 / (10**10)))

def hypothesis(theta, Xval):

	y = (Xval * theta)

	y = y.tolist()[0][0]

	if y > 0:
		y = min(y, 100000)
	if y < 0:
		y = max(y, -100000)

	return y

def genData(data_type, num, scale_radius, win_size, noise):

	xVals = [scale_radius*(2*np.random.random_sample()-1) for i in range(num)]

	if data_type == 0: # linear
		a = (2*np.random.random_sample()-1)

		c = win_size[1]/6 *np.random.random_sample()

		if a > 0:
			c = -c 

		c = win_size[1]/2 + c

		data = [[x, a*((x+scale_radius)/(2*scale_radius) * win_size[0])+ c + noise*np.random.normal()] for x in xVals]

	if data_type == 1: # Quadratic

		roots = [60 + (win_size[0]/2 - 70) *np.random.random_sample(), win_size[0]/2 + 10 +(win_size[0]/2 - 70) *np.random.random_sample()]

		scale = np.random.choice([1,-1]) * (9*np.random.random_sample() + 2)/2500
		
		shift = np.random.random_sample() * win_size[1]/3
		
		if scale > 0:
			shift = -shift

		data = [[x, scale * ((x+scale_radius)/(2*scale_radius) * win_size[0] - roots[0]) * ((x+scale_radius)/(2*scale_radius) * win_size[0] - roots[1]) + win_size[1]/2+ shift + noise*np.random.normal()] for x in xVals]

	
	if data_type == 2: # Elliptical

		center = [100* np.random.normal(), win_size[1]/2 + 100* np.random.normal()]

		shift = [50* np.random.normal(),50* np.random.normal()]

		a = 150* np.random.random_sample() + 50

		b = 150* np.random.random_sample() + 50

		

		data = [[(a * math.cos((x+scale_radius)/(2*scale_radius) * win_size[0] - shift[0]) + center[0] + noise*np.random.normal()/math.sqrt(2))* 2 / win_size[0], b * math.sin((x+scale_radius)/(2*scale_radius) * win_size[0] - shift[1]) + center[1] + noise*np.random.normal()/math.sqrt(2)] for x in xVals]

	if data_type == 3:
		xStretch = np.random.random_sample() + 1
		yStretch = 100 * (np.random.random_sample() + 1/2) * np.random.choice([1,-1])
		xShift = np.random.random_sample() * math.pi
		shift = win_size[1]/2 + 50* np.random.normal() 

		data = [[x, yStretch * math.sin((x+scale_radius)/(2*scale_radius) * 2 * math.pi * xStretch + xShift) + shift + noise*np.random.normal()] for x in xVals]
	return data
