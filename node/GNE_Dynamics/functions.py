import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.linalg import block_diag
from scipy.optimize import minimize
import random

# Generar F (Está Fijo para el caso N = 5)
def F(xi, x_i):
    F = xi - np.array([random.uniform(-1,1), random.uniform(-1,1)])+ 8*(xi)
    return np.reshape(F, (2,))


#================================================================================================================
# FUNCION DE PROYECCION
def proj_tan_con(x, u, lb, ub, type):
    #x es mi coordenada actual
    #y es hacia donde me voy a mover.
    #ub es el limite superior
    #lb es el limite inferior
    #type = 1: x
    #type = 0: lambdas

    #p es mi nueva dirección
    p = []

    # verifico si son los lambdas o los x
    if type == 1:
        for i in range(len(x)):
            
                # si y está en la región factible me puedo mover
                if x[i] > lb and x[i] < ub:
                    p.append(u[i])
                # si y está por encima de la región factible y el cambio decrece
                elif x[i] >= ub and u[i] < 0:
                    p.append(u[i])
                # si y está por debajo de la región factible y el cambio crece
                elif x[i] <= lb and u[i] > 0:
                    p.append(u[i])
                # si y está por encima de la región factible y el cambio crece
                elif x[i] >= ub and u[i] > 0:
                    p.append(0)
                # si y está por debajo de la región factible y el cambio decrece
                elif x[i] <= lb and u[i] < 0:
                    p.append(0)
                else:
                    p.append(0)
    else:
        for i in range(len(x)):
            # si y está en la región factible me puedo mover
            if x[i] > lb and x[i] < ub:
                p.append(u[i])
            # si y está por encima de la región factible y el cambio decrece
            elif x[i] >= ub and u[i] < 0:
                p.append(u[i])
            # si y está por debajo de la región factible y el cambio crece
            elif x[i] <= lb and u[i] > 0:
                p.append(u[i])
            # si y está por encima de la región factible y el cambio crece
            elif x[i] >= ub and u[i] > 0:
                p.append(0)
            # si y está por debajo de la región factible y el cambio decrece
            elif x[i] <= lb and u[i] < 0:
                p.append(0)
            else:
                 p.append(0)
            
    return np.array(p)