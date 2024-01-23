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
         angle = []
         #plt.clf()
         for i in range(8200//2):
             x += [data[2*i]]
             y += [data[2*i + 1]]
             angle += np.arctan(float(data[2*i])/float(data[2*i+1]))
         plt.plot(angle)
         plt.clf()
         #plt.plot(x,y)
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
        freq = np.linspace(0,200,8200//2)
        plt.plot(freq, np.abs(np.fft.fft((x))))
        #x = np.linspace(0,200,8200//2) 
        #plt.xlim(0,8200//4)
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
        freq = np.linspace(0,200,8200//2) 
        plt.plot(freq, np.abs(np.fft.fft((y))))
        #plt.xlim(0,8200//4)
        plt.pause(0.01)
    plt.show()
    return()

def live_plot_iq(cfreq,vmax):
    spectrum = np.zeros_like((10000,4200))
    fig,axs = plt.subplots(2)
    packet_cnt = 0 
    while 1:
        data = parse_packet()
        iq = []
        x = np.linspace(cfreq-100,cfreq+100,4100)
        for i in range(8200//2):
            iq.append(data[2*i] + 1j*data[2*i + 1])
        #plt.clf()
        axs[0].clear()
        axs[1].clear()
        fftd=np.fft.fftshift(np.abs(np.fft.fft(iq)))
        if packet_cnt < 10000:    
            pass
        else:
            pass
        axs[0].plot(x,fftd)
        axs[0].set_xlabel("Frequency(MHz)")
        axs[0].set_title("Live IQ Spectrum")
        axs[1].imshow(spectrum, vmax=vmax)
        axs[1].set_title('IQ Waterfall')
        packet_cnt+=1
        plt.pause(0.01)

    plt.show()
    return()

def parse_packet():
    data = sock.recv(9000)
    if len(data) <  8000:
        print("invalid packet recieved")
    data_2 = struct.unpack('<8200b', data)
    return data_2 

