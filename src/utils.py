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

def live_plot_iq(cfreq):
    spectrum = []
    fig,axs = plt.subplots(2,2)
    plt.tight_layout()
    packet_cnt = 0 
    while 1:
        data = parse_packet()
        iq = []
        ilist= []
        qlist = []
        x = np.linspace(cfreq-100,cfreq+100,4100)
        x2 = np.linspace(cfreq, cfreq+100,2051)
        for i in range(8200//2):
            iq.append(data[2*i] + 1j*data[2*i + 1])
            ilist.append(data[2*i+1])
            qlist.append(data[2*i])
        
        #plt.clf()
        axs[0,0].clear()
        axs[0,1].clear()
        axs[1,0].clear()
        axs[1,1].clear()

        fftd=np.fft.fftshift(np.abs(np.fft.fft(iq)))
        fftd.reshape(4100)

        if packet_cnt < 100:    
            spectrum.append(fftd) 
        else:
            spectrum.pop(0)
            spectrum.append(fftd)

        axs[0,0].plot(x,fftd)
        axs[0,0].set_xlabel("Frequency(MHz)")
        axs[0,0].set_title("Live IQ Spectrum")
        
        axs[1,0].plot(x2, np.abs(np.fft.rfft(ilist)))
        axs[1,0].set_xlabel("Frequency(MHz)")
        axs[1,0].set_title("Live I Spectrum")

        axs[1,1].plot(x2, np.abs(np.fft.rfft(qlist)))
        axs[1,1].set_xlabel("Frequency(MHz)")
        axs[1,1].set_title("Live Q Spectrum")

        axs[0,1].imshow(spectrum,extent=(cfreq-100,cfreq+100,0,100),aspect='auto')
        axs[0,1].set_title('IQ Waterfall')
        axs[0,1].set_xlabel("Frequency(MHz)")
        
        packet_cnt+=1
        plt.pause(0.001)

    plt.show()
    return()

def parse_packet():
    data = sock.recv(9000)
    if len(data) <  8000:
        print("invalid packet recieved")
    data_2 = struct.unpack('<8200b', data)
    return data_2 

