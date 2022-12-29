import sys
import wmi
from scapy.all import *
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

#Live capture packet function
def packet_callback(packet):

    # Get the packet size
    packet_size = len(packet)

    # Print the packet size
    print(packet_size)

    #Gaussian Anomaly Detection of packet size
    mu, std = norm.fit(packet_size)
    if packet_size > mu + 3*std:
      print("Anomaly detected: packet size ="), packet_size
      sys.stdout = log_file
      log_file.close()
      
sniff(iface=selected_adapter.Description, prn=packet_callback)