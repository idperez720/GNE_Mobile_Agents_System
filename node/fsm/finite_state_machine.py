from hashlib import new
from tracemalloc import stop
import numpy as np
import multiprocessing as mp
import time, sys

sys.path.append('./')  # To import modules from upper folder

from GNE_Dynamics.dt_dynamics import *


# def compute_pseudo_gradient():


def run_state(communicator):

    # Recibo las condiciones iniciales
    msg, complete_message = communicator.get_message_from_station()
    if(not complete_message or not len(msg) == 32):
        print('ERROR: received an incomplete message (run_state 1).')
        return
    else:
        x = np.array(list(map(float, msg[0:-2]))).reshape(30)
        


    l = x[10:]
    x = x[0:10]
    # Defino mis vectores x, l, z

    x_array = mp.Array('d', 10)
    l_array = mp.Array('d', 20)
    z_array = mp.Array('d', 20)

    for i in range(len(x)):
        x_array[i] = x[i]
    for i in range(len(l)):
        l_array[i] = l[i]

    z_array = mp.Array('d', 20)
    for i in range(20):
        z_array[i] = 0

    
    # # Launches main process
    stop_flag = False
    print('Nodo: ', communicator._node_number)
    while not stop_flag:

        message = np.hstack(((x_array, l_array))) # Estructura el mensaje
        communicator.send_message_to_station(message) # Envia el mensaje a la estación

        msg, complete_message = communicator.get_message_from_station() # Obtiene el mensaje de la station
        print(msg)

        if not complete_message or msg[0] == 'exit': # Variable que indica si debe parar 
            stop_flag = True
        if(not stop_flag): # Si no hay que parar    
            neighbors_info = np.array(list(map(float, msg[:-2]))).reshape(30, -1)
    
            new_x, new_l, new_z = DT_GNE(x_array[0:10], l_array[0:20], z_array[0:20], neighbors_info, 0.01, communicator._node_number)

            #ACTUALIZAR VECTORES
            for i in range(len(new_x)):
                x_array[i] = new_x[i]
            for i in range(len(new_l)):
                l_array[i] = new_l[i]
            for i in range(len(new_z)):
                z_array[i] = new_z[i]
