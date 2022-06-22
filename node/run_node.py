# SERVIDORES
import socket
import numpy as np

from communication.node_communicator import Node_Comunicator
from fsm.finite_state_machine import *

sys.path.append('./')

# Creates server socket and launches server
communicator = Node_Comunicator()
communicator.bind_server_socket()
communicator.run_server()

# Lauches main loop (finite state machine)
stop_flag = False
while(not stop_flag):
    msg, complete_message = communicator.get_message_from_station()  # Waits command from station

    if(complete_message):
        if(msg[0] == 'exit'):
            print('Closing finite state machine!')
            stop_flag = True

        elif(msg[0] == 'run'):
            run_state(communicator)
            stop_flag = True

    elif(not complete_message):
        print('Received an incomplete message from the station. Closing...')
        stop_flag = True

communicator.close()
print('Node closed.')