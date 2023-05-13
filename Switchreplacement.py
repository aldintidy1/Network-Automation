#Written by Alex Tolliver
#This script will generate a bootstrap configuration for a cisco or juniper switch ; then generate an API call to send the rest of the configuration
#requires installation of netmiko
from netmiko import ConnectHandler
import requests

# Prompt the user to enter the device parameters
device_ip = input("Enter the device IP address: ")
device_name = input("Enter the device name: ")
username = input("Enter the username: ")
password = input("Enter the password: ")

# Define the device information
device = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}

# Define the bootstrap configuration
bootstrap_config = [
    f'hostname {device_name}',
    'no ip domain-lookup',
    'enable secret cisco',
    'interface GigabitEthernet1/0/1',
    'description Uplink to Router',
    'ip address 192.168.1.2 255.255.255.0',
    'no shutdown'
]

# Connect to the device
with ConnectHandler(**device) as net_connect:
    # Send the bootstrap configuration
    output = net_connect.send_config_set(bootstrap_config)
    print(output)

    # Make an API call to the web server to push the rest of the configuration
    web_server_url = 'http://example.com/api/configure-switch'
    response = requests.post(web_server_url, auth=(device['username'], device['password']), data={'config': ''})

    # Print the response from the web server
    print(response.text)