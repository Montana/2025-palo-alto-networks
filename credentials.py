import requests
import xml.etree.ElementTree as ET

PA_IP = "192.168.1.1"
USERNAME = "admin"
PASSWORD = "password"

def get_api_key():
    url = f"https://{PA_IP}/api/?type=keygen&user={USERNAME}&password={PASSWORD}"
    response = requests.get(url, verify=False)
    root = ET.fromstring(response.text)
    return root.find(".//key").text

API_KEY = get_api_key()

def get_security_policies():
    url = f"https://{PA_IP}/api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry/rulebase/security"
    headers = {"X-PAN-KEY": API_KEY}
    response = requests.get(url, headers=headers, verify=False)
    return response.text

print(get_security_policies())
