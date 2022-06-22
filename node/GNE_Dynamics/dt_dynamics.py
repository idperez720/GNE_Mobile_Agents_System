import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.linalg import block_diag
from scipy.optimize import minimize
from functions import *

c = 30

A1 = np.array([[1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0]])
A2 = np.array([[-1, 0],
               [1, 0],
               [0, -1],
               [0, 1],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0]])
A3 = np.array([[0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [-1, 0],
               [1, 0],
               [0, 1],
               [0, -1],
               [1, 0],
               [-1, 0],
               [0, 1],
               [0, -1],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0]])
A4 = np.array([[0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [-1, 0],
               [1, 0],
               [0, -1],
               [0, 1],
               [1, 0],
               [-1, 0],
               [0, 1],
               [0, -1]])
A5 = np.array([[0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [-1, 0],
               [1, 0],
               [0, -1],
               [0, 1],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [0, 0],
               [-1, 0],
               [1, 0],
               [0, -1],
               [0, 1]])



def DT_GNE(current_x, current_lambdas, current_z, neighbors_info, dt, node):

    xi = current_x[0:2]
    x_i = current_x[2:]

    #TODO: REVISAR DIMENSION DE neighbors_info
    l = current_lambdas
    z = current_z


    if node == 1:
        Ai = A1
    elif node == 2:
        Ai = A2
    elif node == 3:
        Ai = A3
    elif node == 4:
        Ai = A4
    elif node == 5:
        Ai = A5


    #TODO: TERMINAR DINAMICAS
    #====================================================================
    # CALCULO DE X
    ui = -(F(xi, x_i) + np.dot(np.transpose(Ai), l) + c * 2*xi - (np.sum()))
    x_dot = dt*(proj_tan_con(x_i, ui))
    pass 