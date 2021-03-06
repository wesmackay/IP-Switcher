#!/usr/bin/python

#
# Author: Nathan Thomas & Wes MacKay
#
# Resources:
# http://stackoverflow.com/questions/7580834/script-to-change-ip-address-on-windows
# http://timgolden.me.uk/python/wmi/cookbook.html
#
# ToDo:
# - Add a check to not change network config if values entered are the same as current configuration
# - Similar to above but check for existing DHCP config
# - Check for successful result and notify user
#


from tkinter import *            #GUI
import tkinter.messagebox        #Error Message Box
import wmi                       #Network Management on Windows


# ------------------------------------------------
# Classes
# ------------------------------------------------

class createGUI:
   def __init__(self, master):
      self.master = master
      master.title("IP Switcher")       # Create title of app

      ### Create Step Forms
      # First Step
      self.first_step = LabelFrame(master, text=' 1. Network Configuration: ')
      self.first_step.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
      # Second Step
      self.second_step = LabelFrame(master, text=" 2. Execute: ")
      self.second_step.grid(row=1, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

      ### Populate Step Forms
      # First Step
      self.ip_address_lbl =  Label(self.first_step, text='IP Address:')
      self.ip_address = Entry(self.first_step)
      # -------------
      self.subnet_address_lbl =  Label(self.first_step, text='Subnet Address:')
      self.subnet_address = Entry(self.first_step)
      # -------------
      self.gateway_address_lbl =  Label(self.first_step, text='Gateway Address:')
      self.gateway_address = Entry(self.first_step)
      # Second Step
      self.change_btn = Button(self.second_step, text='Change IP', command= lambda: self.configure_network("change"))
      self.restore_btn = Button(self.second_step, text='Restore Network', command= lambda: self.configure_network("restore"))

      ### Assign things to GUI GRID
      # First Step
      self.ip_address_lbl.grid(row=0, column=0, padx=5, pady=2, sticky='E')
      self.ip_address.grid(row=0, column=1, columnspan=7, pady=3, sticky="WE")
      # -------------
      self.subnet_address_lbl.grid(row=1, column=0, padx=5, pady=2, sticky='E')
      self.subnet_address.grid(row=1, column=1, columnspan=7, pady=3, sticky="WE")
      # -------------
      self.gateway_address_lbl.grid(row=2, column=0, padx=5, pady=2, sticky='E')
      self.gateway_address.grid(row=2, column=1, columnspan=7, pady=3, sticky="WE")
      # Second Step
      self.change_btn.grid(row=0, column=0, padx=20, pady=2, sticky='W')
      self.restore_btn.grid(row=0, column=2, padx=20, pady=2, sticky='E')

      # Update fields with current address info
      self.configure_network("retrieve")


   # Update values on GUI
   def update(self, entry, value, type):
      # Update entry value
      if type == "entry":
         entry.delete(0, END)
         entry.insert(0, value)
      # Update menu value
      elif type == "optionmenu":
         entry.set(value)

   # Configure the network (on Windows)
   def configure_network(self, action):
      # Obtain network adaptors configurations
      nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled = True)
      nic = nic_configs[0]          # First network adaptor
      # Get current network information and update GUI
      if action == 'retrieve':
         # Display all configurations
         #for i in nic_configs: print(i)
         ip = nic.IPAddress[0]
         subnet = nic.IPSubnet[0]
         gateway = nic.DefaultIPGateway[0]
         # Update fields with current info
         self.update(self.ip_address, ip, "entry")
         self.update(self.subnet_address, subnet, "entry")
         self.update(self.gateway_address, gateway, "entry")
      # Change network configuration with values entered into app
      elif action == 'change':
         tkinter.messagebox.showinfo('Change', 'I am about to change your network address...')
         # IP address, subnet mask and gateway values should be unicode objects
         ip = self.ip_address.get()
         subnet = self.subnet_address.get()
         gateway = self.gateway_address.get()
         # Set IP address, subnet mask and default gateway
         # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
         nic.EnableStatic(IPAddress = [ip], SubnetMask = [subnet])
         nic.SetGateways(DefaultIPGateway = [gateway])
      # Restore network configuration with DHCP config
      elif action == 'restore':
         tkinter.messagebox.showinfo('Restore', 'I am about to restore your network address...')
         # Enable DHCP
         nic.EnableDHCP()


# ------------------------------------------------
# Main Function
# ------------------------------------------------

if __name__ == '__main__':
   root = Tk()
   # Create GUI
   my_app = createGUI(root)
   # Loop GUI until exit button is pressed
   root.mainloop()