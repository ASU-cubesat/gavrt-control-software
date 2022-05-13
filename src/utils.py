import socket
import struct
import matplotlib.pyplot as plt
import numpy as np


UDP_IP = "10.10.10.1"
UDP_PORT = 10003
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))


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

def live_plot_iq():
    plt.figure()
    while 1:
        data = parse_packet()
        #x = []
        #y = []
        #for i in range(8200//2):
        #    x += [data[2*i]]
        #    y += [data[2*i + 1]]
        plt.clf()
        plt.plot(np.abs(np.fft.fft((data))))
        plt.xlim(0,8200//2)
        plt.pause(0.01)
    plt.show()
    return()

def parse_packet():
    data = sock.recv(9000)
    if len(data) <  8000:
        print("invalid packet recieved")
    data_2 = struct.unpack('<8200b', data)
    return data_2 

