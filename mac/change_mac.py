import subprocess
import platform
import re
import time

# Conditionally import winreg only on Windows
if platform.system() == "Windows":
    import winreg

def change_mac(interface, new_mac):
    os_type = platform.system()

    try:
        if os_type in ["Linux", "Darwin"]:
            subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
            subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
            print(f"[+] MAC address changed to {new_mac} on {interface}")

        elif os_type == "Windows":
            mac_clean = new_mac.replace(":", "")
            reg_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

            found = False
            with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hklm:
                with winreg.OpenKey(hklm, reg_path) as base_key:
                    for i in range(0, 200):
                        try:
                            subkey_name = f"{i:04}"
                            with winreg.OpenKey(base_key, subkey_name, 0, winreg.KEY_ALL_ACCESS) as adapter_key:
                                name, _ = winreg.QueryValueEx(adapter_key, "NetCfgInstanceId")
                                if name.lower() == interface.lower():
                                    winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, mac_clean)
                                    found = True
                                    print(f"[+] Registry updated with new MAC: {new_mac}")
                                    break
                        except FileNotFoundError:
                            break
                        except Exception as e:
                            continue

            if not found:
                print("[-] Could not find matching adapter in registry.")
                return

            # Restart the interface
            print("[*] Restarting the network interface...")
            subprocess.run(f'netsh interface set interface "{interface}" admin=disabled', shell=True)
            time.sleep(2)
            subprocess.run(f'netsh interface set interface "{interface}" admin=enabled', shell=True)
            print(f"[+] MAC address change applied on {interface}")

        else:
            print("Unsupported OS.")

    except Exception as e:
        print(f"[-] Error changing MAC address: {e}")
