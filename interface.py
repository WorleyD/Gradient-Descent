import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200, 50,50)

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

