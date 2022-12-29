import sys
import wmi
import numpy as np
import socket
import struct
from scipy.stats import norm

#Set logging directory
log_file = open(r"logs\anomaly.log", "w")

# Create a WMI object
c = wmi.WMI()

# Get a list of all network adapters
adapters = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)

# Print a list of the network adapters
print("Select a network adapter:")
for i, adapter in enumerate(adapters):
    print(f"{i+1}. {adapter.Description} ({adapter.IPAddress[0]})")

# Prompt the user to select a network adapter
selected_adapter = int(input("Enter the number of the adapter you want to use: "))

# Get the selected network adapter
selected_adapter = adapters[selected_adapter - 1]

# Get the selected adapter's MAC address
mac_address = selected_adapter.MACAddress

# Create a raw socket using the AF_PACKET socket type
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

# Bind the socket to the selected network adapter's MAC address
sock.bind((selected_adapter.Description, 0))

# Set the socket to promiscuous mode
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# Capture packets from the network
while True:
    # Receive a packet from the network
    packet = sock.recv(65565)
    
    # Unpack the packet header
    header = struct.unpack("!6s6sH", packet[:14])
    source_mac = header[0]
    destination_mac = header[1]
    ethertype = header[2]
    
    # Get the packet size
    packet_size = len(packet)
    
    # Fit a Gaussian distribution to the packet size data
    mu, std = norm.fit(packet_size)
    if packet_size > mu + 3*std:
      print("Anomaly detected: packet size ="), packet_size
      sys.stdout = log_file
      log_file.close()
  