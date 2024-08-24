import subprocess
import sys
import platform
from time import sleep

from colorama import init, Fore
from colorpick import pick 
import distro

RED, GREEN, CYAN, = ['']*3

SELECTION_MAPPING = {}

def stompcolors_init():
    init(autoreset=True)
    color_dict = dict(zip(filter(str.isupper, dir(Fore)), list(map(lambda ea: getattr(Fore, ea), filter(str.isupper, dir(Fore))))))
    for color, code in color_dict.items():
        globals()[color] = code
    print(f"Setup colors: {' '.join([v+k+Fore.RESET for k, v in color_dict.items()])}")

stompcolors_init()

NTAB = "\n\t"

def is_windows():
    return platform.system().lower() == "windows"

def is_linux():
    return platform.system().lower() == "linux"

def ensure_nmcli():
    if not subprocess.getoutput('which nmcli'):
        print("nmcli is not installed.")
        if is_linux():
            linux_distro = distro.id().lower()
            instructions = "You can install it with:\n\t"
            if "ubuntu" in linux_distro or "debian" in linux_distro:
                print(f"{instructions}sudo apt-get install network-manager")
            elif "centos" in linux_distro or "rhel" in linux_distro or "fedora" in linux_distro:
                print(f"{instructions}sudo yum install NetworkManager")
            else:
                print(f"Please refer to your distribution's documentation to install NetworkManager.")
        else:
            print(f"Operating system {platform.system()} not recognized. Please check the installation instructions for your OS.")
        
        sys.exit(1)

def catch_error_message(error):
    print(f"{RED}\t{error}\n")

def prompt_reload_menu():
    input(f"{CYAN}\tPress 'enter' to go back")
    load_menu()

def reload_menu_now():
    load_menu()

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        catch_error_message(e)
        return None

def configure_hotspot_windows():
    ssid = ""
    while not ssid:
        ssid = input(f"{CYAN}\tPlease specify the SSID (name) of network:{NTAB}SSID: ")
        if not ssid:
            print(f"{RED}{NTAB}The name can't be empty!")
    
    password = ""
    while not password or len(password) < 8:
        password = input(f"{CYAN}{NTAB}Please specify a password for the network:{NTAB}Password: ")
        if not password:
            print(f"{RED}{NTAB}The field can't be empty!")
        elif len(password) < 8:
            print(f"{RED}{NTAB}The password can't be less than eight characters!")
    
    answer = ""
    while answer.lower() not in ["y", "n"]:
        answer = input(f"{CYAN}{NTAB}Do you want to broadcast the SSID (name) of the network? (Y/N): ").lower()
        if answer not in ["y", "n"]:
            print(f"{RED}{NTAB}Please enter 'Y' for yes or 'N' for no")
    
    broadcast_ssid = "allow" if answer == "y" else "disallow"
    
    command = f"netsh wlan set hostednetwork mode={broadcast_ssid} ssid={ssid} key={password}"
    if execute_command(command):
        print(f"{GREEN}\tCreated Wifi Hotspot '{ssid}' successfully")
    
    answer = ""
    while answer.lower() not in ["y", "n"]:
        answer = input(f"{CYAN}{NTAB}Do you wish to start the new network now? (Y/N): ").lower()
        if answer == "n":
            reload_menu_now()
        else:
            command = "netsh wlan start hostednetwork"
            if execute_command(command):
                prompt_reload_menu()

def start_hotspot_windows():
    execute_command("netsh wlan start hostednetwork")
    sleep(3)
    prompt_reload_menu()

def stop_hotspot_windows():
    execute_command("netsh wlan stop hostednetwork")
    prompt_reload_menu()

def view_hotspot_settings_windows():
    execute_command("netsh wlan show hostednetwork")
    prompt_reload_menu()

def view_wlan_settings_windows():
    execute_command("netsh wlan show settings")
    prompt_reload_menu()

def show_blocked_windows():
    execute_command("netsh wlan show blockednetworks")
    prompt_reload_menu()

def show_interface_info_windows():
    execute_command("netsh wlan show interfaces")
    prompt_reload_menu()

def display_all_info_windows():
    execute_command("netsh wlan show all")
    prompt_reload_menu()

def show_available_drivers_windows():
    drivers_output = execute_command("netsh wlan show drivers")
    if drivers_output:
        print(drivers_output)
        if "Hosted network supported  : no" in drivers_output:
            print(f"{RED}\tYou don't support hosting a network :(")
        elif "Hosted network supported  : yes" in drivers_output:
            print(f"{GREEN}\tIt looks like your driver supports hosting WiFi, nice!")
    else:
        print(f"{RED}\tCouldn't find any drivers")
    prompt_reload_menu()

def configure_hotspot_linux():
    ssid = ""
    while not ssid:
        ssid = input(f"{CYAN}\tPlease specify the SSID (name) of network:{NTAB}SSID: ")
        if not ssid:
            print(f"{RED}{NTAB}The name can't be empty!")
    
    password = ""
    while not password or len(password) < 8:
        password = input(f"{CYAN}{NTAB}Please specify a password for the network:{NTAB}Password: ")
        if not password:
            print(f"{RED}{NTAB}The field can't be empty!")
        elif len(password) < 8:
            print(f"{RED}{NTAB}The password can't be less than eight characters!")
    
    command = f"nmcli dev wifi hotspot ifname wlan0 ssid {ssid} password {password}"
    if execute_command(command):
        print(f"{GREEN}\tCreated Wifi Hotspot '{ssid}' successfully")
        prompt_reload_menu()

def start_hotspot_linux():
    print(f"{CYAN}Starting existing hotspot...")
    command = "nmcli connection up Hotspot"
    if execute_command(command):
        sleep(3)
        prompt_reload_menu()

def stop_hotspot_linux():
    command = "nmcli connection down Hotspot"
    execute_command(command)
    prompt_reload_menu()

def view_hotspot_settings_linux():
    execute_command("nmcli connection show Hotspot")
    prompt_reload_menu()

def view_wlan_settings_linux():
    execute_command("nmcli radio wifi")
    prompt_reload_menu()

def show_blocked_linux():
    print(f"{CYAN}Blocked networks aren't directly listed in nmcli.")
    prompt_reload_menu()

def show_interface_info_linux():
    execute_command("nmcli device status")
    prompt_reload_menu()

def display_all_info_linux():
    execute_command("nmcli dev show")
    prompt_reload_menu()

def show_available_drivers_linux():
    execute_command("nmcli device wifi list")
    prompt_reload_menu()

def doggo():
    arf = {"!": ("5f", 2), "_": (2e1, 2), "Z": ('2e', 5), 'Q': (2e1, 4)}
    
    bork = ['20605cg29205c200aQQg60203b3aQg207cQ602d2d5c!2c27200aQQQ2760Qg2c27200aQQQQ202c2d27200a0a','200aQg2027603a2e203aQQ7c2720','5f602d2eg5c5c200aQg3b3a2eg3b3aQg20602d2e5f602d2e5cg5c','20','g','!!5f2e2d272227200aQg3b2cg203bg','Q205c2222272f200ag20273a3a27Q20603a2760g2c2728g5c','200a203b2fg203a3b203bQQQ202c3a27Q2028g202c3a29200ag202c2e2c3a2eQ3b202c3a2e2cg2c2d2e5f20','g602d2e5f200ag2c2fg3ag3b202722Qg603b27QQg2c2d2d','602d2d2d27g20','g5cg3a203bQ207c!5f2fQQQ0aQ5cg205cQ2cg203bg202c3aQ285cg760aQ205cg203a2e2c203a2eQ2c276f29293a206020602d2e200aQ2c2f2c27203b27202c3a3a2227','g2eg20Z20!2f207c20Z2e2eg200ag205c20602d2e203ag60Q3a2eQ','Qg202c272d2e203a207cg3a207c207c5f2f202f7c207c5f7c207cg!2f5f7c203ag0a205c203bQ3bg602d2e!2c27Q602d2e7cg3a205c!!2fg5c!2c207c5c!5f285f29202eg0ag5c203bg203bg3a3a3ag2c3a3a27603a2eg','20','0a0aQQQQQg3b5cQ20ZZZZ2e2e2eg200aQQQQQ207c27205cg203a20!!!QQQ205fg3ag0ag5fQQQQg3b203a203bg3a207c20!5f205cQQg207c207c203ag0a202f20602d2eQQQg2f3a203a207cg3a207c207c5f2f202f205fg205fg!5f7c207c203ag0a7cg2c2d2e602d2eQQg2c273a203a207cg3a207c20!5f205c7c207c207c207c2f205f205c207c203ag0a5cg3ag']
    
    def awoo(b, o, r, k):
        return b.join(o.join(r).split(k))
    
    def woof(b):
        d = awoo('_', '602e', b[::-1], 'g')
        for k, v in arf.items():
            d = d.replace(k, str(v[0] if not str(v[0]).replace('.','').isdigit() else int(v[0]))*v[1])
        return ''.join([chr(int(d[i:i+2], 16)) for i in range(0,len(d), 2)])
    
    print(woof(bork))
    sys.exit()

def make_selection_mapping():
    global SELECTION_MAPPING
    mappings = {
        "windows": {
            1: configure_hotspot_windows,
            2: start_hotspot_windows,
            3: stop_hotspot_windows,
            4: view_hotspot_settings_windows,
            5: view_wlan_settings_windows,
            6: show_blocked_windows,
            7: show_interface_info_windows,
            8: display_all_info_windows,
            9: show_available_drivers_windows,
            10: doggo
        },
        "linux": {
            1: configure_hotspot_linux,
            2: start_hotspot_linux,
            3: stop_hotspot_linux,
            4: view_hotspot_settings_linux,
            5: view_wlan_settings_linux,
            6: show_blocked_linux,
            7: show_interface_info_linux,
            8: display_all_info_linux,
            9: show_available_drivers_linux,
            10: doggo
        }
    }

    if is_windows():
        SELECTION_MAPPING = mappings["windows"]
    elif is_linux():
        ensure_nmcli()
        SELECTION_MAPPING = mappings["linux"]
    else:
        print("Whoops, no workie on macOS, sowwie.")


def load_menu(parameter=None):
    make_selection_mapping()
    selections = {
        'Configure a Wifi HotSpot': 1,
        'Start Wifi HotSpot': 2,
        'Stop Wifi HotSpot': 3,
        'View hosted network settings': 4,
        'Show Wireless LAN settings': 5,
        'Display blocked networks': 6,
        'Show info about interfaces': 7,
        'Display all information': 8,
        'Show available drivers': 9,
        'Exit': 10
    }

    title = f"Choose between these options:"
    options = list(selections.keys())

    if parameter == "start":
        start_hotspot_windows() if is_windows() else start_hotspot_linux()
    elif parameter == "stop":
        stop_hotspot_windows() if is_windows() else stop_hotspot_linux()

    option, _ = pick(options, title)
    SELECTION_MAPPING[selections[option]]()

if __name__ == "__main__":
    load_menu(parameter=sys.argv[1] if len(sys.argv) > 1 else None)
