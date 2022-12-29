import pcapy
import dpkt
import sys
import numpy as np
from scipy.stats import norm
from scapy.all import *

#Set logging directory
log_file = open("/logs/anomaly.log", "w")

# Set the network interface to listen on
interface = "eth0"

# Set the capture filter (e.g. "tcp port 80")
capture_filter = "tcp port 80"

# Create a packet capturer using pcapy
pc = pcapy.open_live(interface, 65536, 1, 0)

# Set the capture filter
pc.setfilter(capture_filter)

# Initialize an empty list to store packet sizes
packet_sizes = []

# Capture packets in a loop
while True:
  (header, packet) = pc.next()
  packet = dpkt.ethernet.Ethernet(packet)
  # Extract the packet size from the packet data
  packet_size = len(packet)
  # Add the packet size to the list
  packet_sizes.append(packet_size)
  # Fit a Gaussian distribution to the packet sizes
  mu, std = norm.fit(packet_sizes)
  # Check if the current packet size is an anomaly
  if packet_size > mu + 3*std:
    print("Anomaly detected: packet size ="), packet_size
    sys.stdout = log_file
    log_file.close()