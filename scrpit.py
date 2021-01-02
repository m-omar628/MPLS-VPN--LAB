#!/usr/bin/env python3
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import getpass
import re

#SSH credentials
user = input('Enter username: ')
passwords = getpass.getpass()

def file_open(file_name):
    with open (file_name) as f:
        file = f.read().splitlines()
    return file
#defined function to ssh to the devices.
def ssh_device(devcie_ip,user_name,pass_word):
    connect_to_device = {
                            'device_type': 'cisco_ios',
                            'ip': devcie_ip,
                            'username': user_name,
                            'password': pass_word
                        }

    try:
        net_connect = ConnectHandler(**connect_to_device)
    except (AuthenticationException): #this error happens if there is a problem to whether username or password
        print('Authentication failure: ' + str(devcie_ip))
    except (NetMikoTimeoutException):#this occurs as you don't have a connection to the device
    #whether the interface is turned off or there is a problem to the physical connection like cables for example
        print('Timeout to the device: ' + str(devcie_ip))
    except (EOFError):
        print('End of file while attempting the device: ' + str(devcie_ip))
    except (SSHException):#this error happens if you dont't have a SSH connection enabled on the device
        print('SSH issue. Are you sure SSH is enabled?, to the device: ' + str(devcie_ip))
    except Exception as unknown_error:
        print('some other error: ' + unknown_error)
    return net_connect

#parsing the files
devices_ip = file_open ('device_ips')
PE_configs = file_open ('PE_configs_file')
P_configs  = file_open ('P_configs_file')
SW_configs = file_open ('Switch_configs_file')

for device in devices_ip:
     device = device.split(',')
     #Sending configs to PE1 and PE2
     if re.search(r"^PE[0-9]$",device[0]):
        print('************************ Connecting to: ',str(device[0]),'.... ************************')
        print(device[1])
        net_connect = ssh_device(device[1],user,passwords)
        output = net_connect.send_config_set(PE_configs)
        print(output)
    #Sending configs to P1 and P2
     elif re.search(r"^P[0-9]$",device[0]):
        print('************************ Connecting to: ',str(device[0]),'.... ************************')
        net_connect = ssh_device(device[1],user,passwords)
        output = net_connect.send_config_set(P_configs)
        print(output)
