#!/usr/bin/env python3
import argparse
import re
import sys

# Import your modular functions
from network_info.display_net import display_network_config
from ip.change_ip import change_ip
from mac.change_mac import change_mac
from check_ip.check_ip import check_ip

# Helper functions to validate formats
def is_valid_mac(mac):
    return bool(re.match(r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$', mac))

def is_valid_ip(ip):
    return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip))

# The function that uses optparse
def main():
    # Create the parser
    parser = argparse.ArgumentParser(prog='NetTweak Tool', description='A tool for network configuration management written by Ephraim Norbert and Uchendu Favour')
    
    # Define the available options
    # Show network configuration
    parser.add_argument("-n", "--network", action="store_true", help="Display the current network configuration")
    
    # Change IP address and netmask
    parser.add_argument("-i", "--ip", metavar=("INTERFACE", "NEW_IP", "NETMASK"), nargs=3, help="Change the IP address of a network interface. Requires INTERFACE, NEW_IP, and NETMASK")
    
    # Change MAC address
    parser.add_argument("-m", "--mac", metavar=("INTERFACE", "NEW_MAC"), nargs=2, help="Change the MAC address of a network interface. Requires INTERFACE and NEW_MAC")
    
    # Check current IP address
    parser.add_argument("-c", "--check", metavar="INTERFACE", nargs=1, help="Check the current IP address")

    # Parse the command line options and arguments
    args = parser.parse_args()

    # Check for network configuration option
    if args.network:
        display_network_config()

    # Check for IP change option
    elif args.ip:
        interface, new_ip, netmask = args.ip
        
        if not is_valid_ip(new_ip):
            print("[-] Invalid IP address format.")
            sys.exit(1)
        
        if not is_valid_ip(netmask):
            print("[-] Invalid netmask format.")
            sys.exit(1)
            
        change_ip(interface, new_ip, netmask)

    # Check for MAC address change option
    elif args.mac:
        interface, new_mac = args.mac
        
        if not is_valid_mac(new_mac):
            print("[-] Invalid MAC address format. Use XX:XX:XX:XX:XX:XX")
            sys.exit(1)
        
        change_mac(interface, new_mac)

    # Check the current IP address
    elif args.check:
        interface = args.check[0]
        check_ip(interface)

    # If no arguments are provided, display help
    else:
        parser.print_help()

# Run the main function
if __name__ == "__main__":
    main()