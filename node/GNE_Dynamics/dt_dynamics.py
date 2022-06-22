import numpy as np
import random, sys, os


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

bi = np.array([0.2]*20)

# Generar F (Está Fijo para el caso N = 5)
def F(xi, x_i):
    ri = np.array([random.uniform(-1,1), random.uniform(-1,1)])
    Fi = ri + np.multiply(9, xi)
    print(np.shape(Fi))
    return Fi


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


def DT_GNE(current_x, current_lambdas, current_z, neighbors_info, dt, node):

    xi = current_x[(node-1)*2:((node-1)*2)+2]
    xij = neighbors_info[(node-1)*2:((node-1)*2)+2, :]
    Neigh_number = np.shape(neighbors_info)[1]
    
    x_i = np.delete(current_x, [(node-1)*2, ((node-1)*2)+1])

    lj = neighbors_info[10:, :]
    sum_lj = np.sum(lj, axis=1)

    sum_x_ij = np.sum(neighbors_info[:10], axis=1)
    
    sum_x_ij = np.delete(sum_x_ij, [(node-1)*2, ((node-1)*2)+1])
    
    sum_xij = np.sum(xij, axis=1)
    
    
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


    #====================================================================
    # CALCULO DE xi
    ui = -(F(xi, x_i) + np.dot(np.transpose(Ai), l) + c * (np.multiply(Neigh_number,xi) - sum_xij))
    xi_dot = dt*(proj_tan_con(xi, ui, 0.1, 0.5, 1))
    xi_new = xi + xi_dot

    #====================================================================
    # CALCULO DE x_i
    x_i_dot = dt * np.multiply(-c, (x_i - sum_x_ij))
    x_i_new = x_i + x_i_dot

    #====================================================================
    # CALCULO DE zi
    z_dot = dt * np.multiply(Neigh_number, l) - sum_lj
    z_new = z + z_dot
    

    #====================================================================
    # CALCULO DE li
    lik = np.dot(Ai, xi) - bi - z - np.multiply(Neigh_number, l) - sum_lj
    li_dot = proj_tan_con(l, lik, 0, np.inf, 0)
    l_new = l + li_dot

    x_new = np.insert(x_i_new, (node-1)*2, xi_new)

    return x_new, l_new, z_new
