import socket
import struct
import matplotlib.pyplot as plt
import numpy as np


UDP_IP = "10.10.10.1"
UDP_PORT = 10003
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))



def live_plot_ivq():
    plt.figure()     
    while 1:
         data = parse_packet()
         x = []
         y = []
         #plt.clf()
         for i in range(8200//2):
             x += [data[2*i]]
             y += [data[2*i + 1]]
         plt.clf()
         plt.plot(x,y)
         plt.pause(0.01)
    plt.show()
    return()


def live_plot_i():
    plt.figure()
    while 1:
        data = parse_packet()
        x = []
        y = []
        for i in range(8200//2):
            x += [data[2*i]]
            y += [data[2*i + 1]]
        plt.clf()
        plt.plot(np.abs(np.fft.fft((x))))
        plt.xlim(0,8200//4)
        plt.pause(0.01)
    plt.show()
    return()

def live_plot_q():
    plt.figure()
    while 1:
        data = parse_packet()
        x = []
        y = []
        for i in range(8200//2):
            x += [data[2*i]]
            y += [data[2*i + 1]]
        plt.clf()
        plt.plot(np.abs(np.fft.fft((y))))
        plt.xlim(0,8200//4)
        plt.pause(0.01)
    plt.show()
    return()

def live_plot_iq(lofreq,dlfreq,bw=False):
    plt.figure()
    while 1:
        data = parse_packet()
        iq = []
        #x = []
        #y = []
        #iq = data[::2] + 1j*data[1::2]
        #x = [0]*8200//2
        #offset = lofreq-dlfreq
        #dlbb = 250-offset
        x = np.linspace(lofreq-250,lofreq-50,8200//2)
        for i in range(8200//2):
            iq.append(data[2*i] + 1j*data[2*i + 1])
        plt.clf()
        plt.plot(x,np.abs(np.fft.fft((iq))))
        if bw is not False:
            plt.xlim(dlfreq-bw/2,dlfreq+bw/2)
        else:
            plt.xlim(lofreq-250,lofreq-50)
        plt.xlabel("Frequency(MHz)")
        plt.pause(0.01)
    plt.show()
    return()

def parse_packet():
    data = sock.recv(9000)
    if len(data) <  8000:
        print("invalid packet recieved")
    data_2 = struct.unpack('<8200b', data)
    return data_2 

