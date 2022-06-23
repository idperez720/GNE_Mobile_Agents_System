# CLIENTE
import socket
import time
import numpy as np
from graphs.models import *
from communication.camera_server import Camera_Server
import multiprocessing as mp
from scipy.linalg import block_diag
#from detection.detector import Detector

class Main_Station(Camera_Server):

    def __init__(self, robots=['red', 'blue', 'purple', 'yellow', 'lime']):
        
        Camera_Server.__init__(self, robots=robots)

        # Core variables
        self._dt = 0.01

        # Station variables
        self._system_info = np.zeros((30, self._n)) #x, l
        self._graph = cycle(len(robots)) # Communication graphs
        self._sim_time = np.linspace(0,300, 3000)

        x10 = np.array([-0.4, 0.12])
        x20 = np.array([-0.4, 0.42])
        x30 = np.array([0.1, 0.35])
        x40 = np.array([0.4, 0.35])
        x50 = np.array([0.45, 0.12])

        self._init_pos = block_diag(x10, x20, x30, x40, x50)
        self._init_pos = np.transpose(np.hstack((self._init_pos, np.ones((5, 20)))))

        # Create Sockets
        self._station_sckts = []
        for addr in self._node_addresses:
            sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sckt.connect((addr, 2000))
            self._station_sckts.append(sckt)

        


        ## TODO: VARIABLES MULTIPROCESADO
        # Multiprocessing variables
        self._positions_array = mp.Array('d', self._n*3)    # Multiprocessing array with [xs, ys, phis]
        self._keep_running = mp.Array('i', [1])             # Controller running flag

        # Run processes
        self.execute_multiprocesses()

    def execute_multiprocesses(self):
        

        time.sleep(1)
        self.send_message_to_all_nodes('run')

        self.run_station()

        self.send_message_to_all_nodes('exit')
        
    def update_system_info(self):
        for i, sckt in enumerate(self._station_sckts):
            msg = sckt.recv(self._buffer_size).decode('utf-8').split(self._msg_delimiter)
            if(msg.count(self._msg_end) == 1 and msg[-2] == self._msg_end):
                self._system_info[:, i] = list(map(float, msg[:-2]))
            
            else:
                print('ERROR: an incomplete message was received from:', self._node_addresses[i])
                self._keep_running[0] = 0

            #print()
            #print(self._system_info)
    
    def update_mp_targets(self):
        for i in range(self._n):
            self._targets_array[i] = self._system_info[2, i]
            self._targets_array[i + self._n] = self._system_info[3, i]

    def run_station(self):
        

        #Inicializo la posición inicial de los agentes-
        for i, sckt in enumerate(self._station_sckts):
            msg = self._msg_delimiter.join(list(map(str, self._init_pos[:, i]))) # Envio la posición objetivo a todos los nodos
            sckt.sendall(bytes(msg + self._msg_tail, 'utf-8'))


        stop_flag = False

        # Main loop
        for i in self._sim_time:
            print('================================================')
            print(f'Iteration: {i}')
            self.update_system_info()
            time.sleep(self._dt)

            for i, sckt in enumerate(self._station_sckts):
                neighbors_info = self._system_info[:, np.where(self._graph[i, :] == 1)].reshape(-1)
                neighbors_info = np.round(neighbors_info, 3)
                msg = self._msg_delimiter.join(list(map(str, neighbors_info)))
                sckt.sendall(bytes(msg+self._msg_tail, 'utf-8'))

    def send_message_to_all_nodes(self, msg):
        for sckt in self._station_sckts:
            sckt.sendall(bytes(msg + self._msg_tail, 'utf-8'))

    def close_sockets(self):
        for sckt in self._station_sckts:
            sckt.close()
        print('Closed all sockets!')


if __name__ == '__main__':
    station = Main_Station(robots=['blue', 'purple', 'red', 'green', 'lime'])
