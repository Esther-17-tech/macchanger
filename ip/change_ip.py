import subprocess
import platform

# function to change IP address and netmask of a network interface
def change_ip(interface, new_ip, netmask="255.255.255.0"):
    os_type = platform.system()
    try:
        if os_type in ["Linux", "Darwin"]:
            subprocess.run(["sudo", "ifconfig", interface, new_ip, "netmask", netmask], check=True)
            print(f"[+] IP address changed to {new_ip} with netmask {netmask} on {interface}")
        elif os_type == "Windows":
            cmd = f'netsh interface ip set address name="{interface}" static {new_ip} {netmask}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"[+] IP address changed to {new_ip} with netmask {netmask} on {interface}")
        else:
            print("Unsupported OS.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to change IP address: {e}")