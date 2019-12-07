

# Final Project for COMP 3710 Class

  ## Introduction
This project simulates various gradient descent algorithms on randomly generated linear, quadratic, elliptical, or sinusoidal data, allowing user set variables to modify the gradient descent Parameters

___

## Prerequisites

This program requires Python 3.5+, Pygame, and Numpy to be installed in order to run. Once the prerequisites are installed, clone the repository and launch proj . py to begin the program

##  User Parameters

Upon launching the program you'll be greeted with a window consisting of a blank plotting surface, as well as sliders and buttons to tweak parameters, generate data, and run the program. An explanation of all tweak-able parameters is provided below.

Learning Rate: min = 0, max = 1 (float)

  Controls the step size in gradient descent. Setting this value too high will cause the algorithm to fail, but setting it     too low will make it run too slow.

Regularization: min = 0, max = 0.5 (float)

  Changing this value changes the cost function slightly to solve the problem of overfitting.

Total Iterations: min = 1, max = 1000 (int)

  The number of iterations (parameter updates) gradient descent will make.

Iteration Time Step: min = 1, max = 20 (int)

  Number of iterations to run gradient descent per frame in the application. This controls how slow or fast the model runs. 

Batch Size: min = 1, max = 1000 (int)


  Changing this value determines which variant of gradient descent will be used. Explicitly, the algorithm will run normally
  if the Batch Size is greater or equal to the number of training examples and will make updates based on Batch Size number 
  of examples at a time otherwise.

Noise: min = 0, max = 100 (int)

  This value controls how much "randomness" is introduced into the generated data. 

Polynomial Order: min = 1, max = 10 (int)

  This determines the degree of the polynomial approximation of the data gradient descent will obtain. Higher order
  polynomials can provide better predictions of data but are prone to overfitting and can make the gradient descent algorithm
  take much longer to run.
  
Type of Data: 4 options

  This value lets the user pick which type of data to generate. (Linear, Quadratic, Elliptic, and Sinusoidal)
  
Training Examples: min = 1, max = 1000 (int)

  The number of training examples or data points to generate.





## Running the Program
Once Parameters are tweaked to the users liking, data can be generate by selecting Linear, Quadratic, Elliptic, or Sinusoidal, based on what the user would like to approximate.

From there, simply press generate data until you get data you are satisfied with, and then press 'Run Gradient Descent' button to watch the magic unfold.

## Authors 

Daniel D.  
Patrick D.  
Tara V.  
David W.  



## Authors Note
![alt text](https://imgs.xkcd.com/comics/machine_learning.png "The pile gets soaked with data and starts to get mushy over time, so it's technically recurrent.")

