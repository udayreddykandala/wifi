import subprocess


def get_wifi_interface():
    try:
        # Get a list of all network interfaces
        network_services = subprocess.check_output(
            ['networksetup', '-listallhardwareports'],
            stderr=subprocess.STDOUT
        ).decode('utf-8').split('\n')

        wifi_interface = None
        for i, line in enumerate(network_services):
            if 'Wi-Fi' in line:
                wifi_interface = network_services[i + 1].split(': ')[1]
                break
        return wifi_interface
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while listing network interfaces: {e.output.decode('utf-8')}")
        return None


def get_wifi_details(interface):
    try:
        wifi_details = subprocess.check_output(
            ['networksetup', '-getairportnetwork', interface],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        return wifi_details.split(': ')[1].strip()  # Extract Wi-Fi network name
    except subprocess.CalledProcessError as e:
        return f"An error occurred while getting Wi-Fi details: {e.output.decode('utf-8')}"


def get_wifi_password(ssid):
    try:
        password = subprocess.check_output(
            ['security', 'find-generic-password', '-D', 'AirPort network password', '-a', ssid, '-w'],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        return password
    except subprocess.CalledProcessError as e:
        return f"An error occurred while retrieving Wi-Fi password: {e.output.decode('utf-8')}"


wifi_interface = get_wifi_interface()
if wifi_interface:
    wifi_ssid = get_wifi_details(wifi_interface)
    if "An error occurred" not in wifi_ssid:
        print(f"Wi-Fi SSID: {wifi_ssid}")
        wifi_password = get_wifi_password(wifi_ssid)
        print(f"Wi-Fi Password: {wifi_password}")
    else:
        print(wifi_ssid)
else:
    print("No Wi-Fi interface found.")
