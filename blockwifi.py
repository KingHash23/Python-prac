import json
import winreg
from wlanapi import WlanOpenHandle, WlanCloseHandle, WlanScan, WlanGetAdapterNames, WlanGetAvailableNetworkList, WlanFreeMemory
from pycryptodome.Cipher import Cipher
from pycryptodome.Hash import MD4
from pycryptodome.Protocol.KDF import PBKDF2
import sys
import json
import winreg
import wlanapi

def get_wifi_config():
    key = b"Windows Wireless Password"
    profile_path = os.path.expanduser(r"%APPDATA%\Microsoft\Wlansvc\Profiles\Interfaces")

    guids = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Control\Network\{4D36E972-E325-11CE-BFC1-08002BE10318}", 0, winreg.KEY_READ) as key:
        i = 0
        while True:
            try:
                sub_key_name = winreg.EnumKey(key, i)
                if sub_key_name.startswith("{") and len(sub_key_name) == 36:
                    guids.append(sub_key_name)
              


def get_wifi_config():
    key = b"Windows Wireless Password"
    profile_path = os.path.expanduser(r"%APPDATA%\Microsoft\Wlansvc\Profiles\Interfaces")

    guids = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Control\Network\{4D36E972-E325-11CE-BFC1-08002BE10318}", 0, winreg.KEY_READ) as key:
        i = 0
        while True:
            try:
                sub_key_name = winreg.EnumKey(key, i)
                if sub_key_name.startswith("{") and len(sub_key_name) == 36:
                    guids.append(sub_key_name)
                i += 1
            except WindowsError:
                break

    for guid in guids:
        interface_path = os.path.join(profile_path, guid)
        if os.path.exists(interface_path):
            break

    profiles = []
    for filename in os.listdir(interface_path):
        if filename.endswith(".xml"):
            with open(os.path.join(interface_path, filename), "r") as file:
                try:
                    raw_xml = file.read()
                    data = json.loads(raw_xml[raw_xml.index("{"): raw_xml.rindex("}") + 1])
                    profiles.append(data)
                except Exception as e:
                    print(f"An error occurred while parsing Wi-Fi profile: {e}")

    return profiles

def decrypt_wifi_password(encrypted_password: str) -> str:
    password_hash = MD4.new(key).digest()
    decrypted_password = PBKDF2(password_hash, encrypted_password, dkLen=256 // 8)
    return decrypted_password

def scan_for_wifi():
    hClient = WlanOpenHandle(0, None, None)
    if hClient:
        wlan_adapter_list = []
        ret = WlanGetAdapterNames(hClient, wlan_adapter_list)

        if ret != 0:
            wlan_adapter_names = [chr(c) for c in wlan_adapter_list]
            wlan_adapter_name = "".join(wlan_adapter_names)

            if wlan_adapter_name:
                ret = WlanScan(hClient, wlan_adapter_name, None, None, None)
                if ret == 0:
                    return True

        WlanCloseHandle(hClient)

    return False

def get_wifi_networks():
    scan_for_wifi()

    hClient = WlanOpenHandle(0, None, None)
    if hClient:
        networks = []
        ret = WlanGetAvailableNetworkList