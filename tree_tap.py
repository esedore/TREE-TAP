import sys
import wmi
from scapy.all import *
import struct
from scipy.stats import norm
import pyarrow.parquet as pq
import pandas as pd
import pickle4 as pickle

#load the parquet model
model_table = pd.read_table('data/classifier.parquet')
model = model_table.to_pandas()

#Set logging directory
with open(r"logs\anomaly.log", "a") as log_file:

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

      #get the protocol
      protocol = packet[IP].proto

      # Print the packet size
      print(packet_size)
      print(protocol)

      #Gaussian Anomaly Detection of packet size
      mu, std = norm.fit(packet_size)
      if packet_size > mu + 3*std:
        print("Anomaly detected: packet size ="), packet_size
        sys.stdout = log_file

      #pandas dataframe from features
      X = pd.DataFrame({'packet_size':[packet_size],'protocol':[protocol]})

      #Guessing time
      y_pred = model.predict(X)

      if y_pred == 1:
        print("Anomalous traffic detected! :(")
        sys.stdout = log_file
      else:
        print("Benign :)")
  sniff(iface=selected_adapter.Description, prn=packet_callback, filter='tcp')