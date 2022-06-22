from hashlib import new
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

    
    # Defino mis vectores x, l, z

    x_array = mp.Array('d', 10)
    l_array = mp.Array('d', 20)
    z_array = mp.Array('d', 20)
    for i in range(len(x)):
        if i < 10:
            x_array[i] = x[i]
        else:
            l_array[i] = x[i]

    z_array = mp.Array('d', 20)
    for i in range(20):
        z_array[i] = 0

    
    # # Launches main process
    stop_flag = False
    print('Nodo: ', communicator.__node_number)
    while not stop_flag:

        message = np.hstack(((x_array, l_array))) # Estructura el mensaje
        communicator.send_message_to_station(message) # Envia el mensaje a la estación

        msg, complete_message = communicator.get_message_from_station() # Obtiene el mensaje de la station

        stop_flag = (not complete_message) or (msg[0] == 'exit') # Variable que indica si debe parar

        if(not stop_flag): # Si no hay que parar    
            neighbors_info = np.array(list(map(float, msg[:-2]))).reshape(30, -1)
            new_info = DT_GNE(x_array, l_array, z_array, neighbors_info, 0.01, communicator.__node_number)

            for i in range(len(new_info)):
                if i < 10:
                    x_array[i] = new_info[i]
                elif i < 30:
                    l_array[i] = new_info[i]
                else:
                    z_array[i] = new_info[i]

