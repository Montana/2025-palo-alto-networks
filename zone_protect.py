import requests
import xml.etree.ElementTree as ET

PA_IP = "192.168.1.1"  
USERNAME = "admin"     
PASSWORD = "password"  

requests.packages.urllib3.disable_warnings()

def get_api_key():
    url = f"https://{PA_IP}/api/?type=keygen&user={USERNAME}&password={PASSWORD}"
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        api_key = root.find(".//key")
        if api_key is not None:
            return api_key.text
        else:
            print("Failed to retrieve API key.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def apply_zone_protection(api_key):
    zone_protection_payload = """
    <entry name="Zone-Protect">
        <dos-protection>
            <tcp-syn>
                <enable>yes</enable>
                <red>yes</red>
                <red-percentage>90</red-percentage>
            </tcp-syn>
        </dos-protection>
    </entry>
    """

    url = f"https://{PA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/zone-protection-profile&element={zone_protection_payload}"
    headers = {"X-PAN-KEY": api_key}

    response = requests.post(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        print("Zone Protection Profile applied successfully.")
        print(response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    API_KEY = get_api_key()
    
    if API_KEY:
        apply_zone_protection(API_KEY)
    else:
        print("Failed to retrieve API key. Exiting.")
