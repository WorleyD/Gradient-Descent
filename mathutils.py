import numpy as np
import math


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

	if data_type == 4: #Random
		data_type = np.random.choice([1,2,3]) 

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

	if data_type == 3: # Sinusoidal
		xStretch = np.random.random_sample() + 1
		yStretch = 100 * (np.random.random_sample() + 1/2) * np.random.choice([1,-1])
		xShift = np.random.random_sample() * math.pi
		shift = win_size[1]/2 + 50* np.random.normal() 

		data = [[x, yStretch * math.sin((x+scale_radius)/(2*scale_radius) * 2 * math.pi * xStretch + xShift) + shift + noise*np.random.normal()] for x in xVals]
	return data
