import subprocess
import platform

# function to display to current network configuration
def display_network_config():
    os_type = platform.system()
    try:
        if os_type in ["Linux", "Darwin"]:
            subprocess.run(["ifconfig"])
        elif os_type == "Windows":
            subprocess.run(["ipconfig", "/all"])
        else:
            print("Unsupported OS.")
    except Exception as e:
        print(f"Error: {e}")