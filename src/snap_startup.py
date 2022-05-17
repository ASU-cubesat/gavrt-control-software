import casperfpga
from casperfpga import snapadc
import argparse

parser = argparse.ArgumentParser(description='Inputs for snap startup')
parser.add_argument("hostname", help = "ip address of the SNAP board to initialize")
parser.add_argument("--bitfile", help = ".fpg file to program board with", default = None)
parser.add_argument("--ref", help = "reference frequency for clocking", default = 10)
parser.add_argument("--samplerate", help = "Sampling Rate for ADC", default = 200)
parser.add_argument("--numchannel", help = "Demux mode for SNAP, 1ch = demux by 4, 2ch = demux by 2, 4ch = no demux", default = 4)
args = parser.parse_args()

fpga = casperfpga.CasperFpga(str(args.hostname))

if args.bitfile == None:
    fpga.transport.prog_user_image()
else:
    fpga.transport.upload_to_ram_and_program(str(args.bitfile))

adc = casperfpga.snapadc.SNAPADC(fpga, ref=args.ref)
success = None
while success==None:
    try:
         success = adc.init(samplingRate=args.samplerate, numChannel=args.numchannel)
    except:
        pass


#Program the board 

