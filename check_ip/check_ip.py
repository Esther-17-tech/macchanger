import subprocess
import re
import platform

# Check the current IP address
def check_ip(interface):
    os_type = platform.system()
    try:
        if os_type in ["Linux", "Darwin"]:
            result = subprocess.check_output(["ifconfig", interface]).decode()
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result)
            if match:
                print(f"[+] Current IP on{interface}: {match.group(1)}")
            else:
                print("[-] IP address.")
        elif os_type == "Windows":
            result = subprocess.check_output(["ipconfig"]).decode()
            lines = result.splitlines()
            for i, line in enumerate(lines):
                if interface in line:
                    for j in range(i, i+10):
                        if "IPv4 Address" in lines[j]:
                            ip = lines[j].split(":")[-1].strip()
                            print(f"[+] Current IP on {interface}: {ip}")
                            return
            print("[-] IP not found.")
        else:
            print("Unsupported OS.")
    except Exception as e:
        print(f"Error: {e}")