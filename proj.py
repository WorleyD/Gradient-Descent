
import pygame
import math
import numpy as np # Required mainly for matrix computation in the GD algorithm
import resources 

## Defining colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200, 50,50)

## Initializing the pygame engine
pygame.init()

screen_w = 1200
screen_h = 600

## Defining the screen size
size = (screen_w, screen_h)

## Creating the screen
screen = pygame.display.set_mode(size)

## Initializing the clock
clock = pygame.time.Clock()

## Loop variable
done = False

mousePressed = False
m_cool = 0

clickCount = 0

## Sliders, Buttons, and Options

noise = resources.Slider((20,25), (100,10), [i for i in range(0,101)], 0, "Noise")
learningRate = resources.Slider((20,60), (100,10), [0.00000001 * i**2 for i in range(0,10001)], 1, "Learning Rate")
polynomialOrder = resources.Slider((20, 95), (100,10), [math.floor(0.1*i + 1) for i in range(0,100)], 0, "Polynomial Order")
regularization = resources.Slider((20,130), (100,10), [0.01 * i / 2 for i in range(0,1001)], 0, "Regularization")
numIters = resources.Slider((20,165), (100,10), [i for i in range(1,1001)], 99, "Total Iterations")
itersTime = resources.Slider((20, 200), (100,10), [math.floor(0.2*i + 1) for i in range(0,100)], 0, "Iteration Time Step")
trainingEx = resources.Slider((20,235), (100,10), [i for i in range(1,1001)], 99, "Training Examples")
batchSize = resources.Slider((20,270), (100,10), [i for i in range(1,1001)], 99, "Batch Size")

options1 = [noise, learningRate, polynomialOrder, regularization, numIters, itersTime, trainingEx, batchSize]

generateData = resources.Button((200, 300), (160, 50), "New Data", 30)
clear = resources.Button((200, 365), (160, 50), "Clear Plot", 30)
run = resources.Button((20, 430), (340, 50), "Run Gradient Descent", 30)
dataSetType = resources.Options((20,300), 20, ["Linear", "Quadratic", "Elliptic", "Sinusoidal"], 0, "Dataset Type")

options2 = [generateData, dataSetType, clear, run]

plotw = resources.plotWindow((400,0), (800,600))
pdimensions = plotw.getDims()

data = None

func = None

GD_RunState = None

theta = None

currentMessage = None 
msgColour = RED

scale_radius = 7/6

cost = 0

## The main loop
while not done:

    ## Event loop for key inputs
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	## Sets the mouse position
	m_pos = pygame.mouse.get_pos()

    ## Changes the mouse click bool
	if pygame.mouse.get_pressed()[0]:
		if m_cool == 0:
			click = True
		else:
			click = False
		mousePressed = True
		m_cool = 3
	else:
		click = False
		mousePressed = False
		if m_cool > 0:
			m_cool-=1
	
	## Filling the screen with WHITE
	screen.fill(WHITE)


	### All GUI MODULE UPDATES
	# Updating options that are sensitive to any mouse press
	for i in range(len(options1)):
		if mousePressed:
			if options1[i].update(m_pos):
				m_pos = [m_pos[0], options1[i].getLoc()[1]]
				pygame.mouse.set_pos(m_pos)
		options1[i].draw(screen)

	# Updating options that are sensitive to single clicks
	for i in range(len(options2)):
		
		options2[i].update(m_pos,click, mousePressed)
		options2[i].draw(screen)

	# Plot update
	plotw.update(screen, cost)

	if data != None:

		plotw.plotData(screen, [[(p[0]+scale_radius)/(2*scale_radius) * pdimensions[1][0], p[1]] for p in data])

	if func != None:
		plotw.plotFunc(screen, [[(p[0]+scale_radius)/(2*scale_radius) * pdimensions[1][0], p[1]] for p in func])

	if currentMessage != None:
		font = pygame.font.Font('freesansbold.ttf', 25)
		text = font.render(currentMessage,True,msgColour)
		screen.blit(text, (10, screen_h - 30))

	### INPUT PROCESSING BEGINS

	
	if click:
		currentMessage = None	

	if clear.getVal():
		data = None
		func = None
		GD_RunState = None
		cost = 0

	if run.getVal():
		if data == None:
			currentMessage = "ERROR: No data generated!"
			msgColour = RED
		else:
			order = polynomialOrder.getVal()

			dataSet = np.matrix([[point[0] ** i for i in range(0, order+1)]+[point[1]] for point in data])

			GD_RunState = [numIters.getVal(), dataSet, learningRate.getVal(),regularization.getVal(), itersTime.getVal(), batchSize.getVal()]

			theta = [[0] for i in range(order+1)]
			theta[0][0] = 300
			theta = np.matrix(theta)
			

	if GD_RunState != None:

		if GD_RunState[0] == 0:
			GD_RunState = None
		else:
			
			iters = min(GD_RunState[4], GD_RunState[0])

			GD_RunState[0] = GD_RunState[0] - iters

			n = GD_RunState[1].shape[1] - 1

			X = np.matrix(GD_RunState[1][:,0:n])
			y = np.matrix(GD_RunState[1][:,n])

			alpha = GD_RunState[2]
			lmda = GD_RunState[3]
			batch_size = GD_RunState[5]

			theta = resources.gradientDescent(X, y, alpha, lmda, iters, batch_size, theta)

			cost = round(resources.avgCost(theta, X, y),3)

			xpoints = [x/250 -2 for x in range(1001)]

			func = [[x, resources.hypothesis(theta, np.matrix([[x**i for i in range(theta.shape[0])]]))] for x in xpoints]

			#resources.getFunc(theta, mean, sdev, [x for x in range(0, pdimensions[1][0], 10)])

			#print(func[0])
			#func = [[x, np.matrix([(x/scale)**i for i in range(theta.shape[0]) ]) * theta] for x in range(0, pdimensions[1][0], 10)]

			#func = [[int(point[0]) , int(point[1])] for point in func]

	if generateData.getVal():

		data = resources.genData(dataSetType.getVal(), trainingEx.getVal(), scale_radius, pdimensions[1], noise.getVal())
		
		#xVals = [2*scale_radius*np.random.random_sample() - scale_radius for x in range(trainingEx.getVal())]
		#data = [[x, -(pdimensions[1][0]*(x+scale_radius)/(2*scale_radius))*(pdimensions[1][0]*(x+scale_radius)/(2*scale_radius) - 800)/800 + 100 +noise.getVal() * np.random.normal()] for x in xVals]
		
	## Code to draw a line
	#pygame.draw.line(screen, BLACK,  (50,60), (100,30), 4)

	## Code to draw a rectangle
	#pygame.draw.rect(screen, BLACK, (0,0,50,50), 5)

	## Code to draw an ellipse
	#pygame.draw.ellipse(screen, BLACK, (100,80,100,50), 5)

	## Code to draw a circle
	#pygame.draw.circle(screen, BLACK,(25,120),20,2)

	## Code to draw a polygon
	#pygame.draw.polygon(screen, BLACK, ((350,0),(400,50),(300,50)),3)


	## Flipping the display
	pygame.display.flip()

	## Setting the fps
	clock.tick(60)

## User friendly quitting
pygame.quit()
