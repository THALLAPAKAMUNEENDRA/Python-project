import psutil
import speedtest
import platform
import wmi
import socket
import screeninfo


def get_installed_software():
    installed_software = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pinfo = proc.info
            installed_software.append(pinfo['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return installed_software

def get_internet_speed():
    st = speedtest.Speedtest()
    st.download(threads=None)  # Perform a download test
    st.upload(threads=None)    # Perform an upload test
    download_speed = st.download() / 1_000_000  # in Mbps
    upload_speed = st.upload() / 1_000_000  # in Mbps
    return download_speed, upload_speed

def get_screen_resolution():
    screen = screeninfo.get_monitors()[0]
    return screen.width, screen.height

def get_cpu_info():
    cpu_info = {}
    cpu_info["Model"] = platform.processor()
    cpu_info["Cores"] = psutil.cpu_count(logical=False)
    cpu_info["Threads"] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    gpu_info = None
    try:
        w = wmi.WMI()
        for adapter in w.Win32_VideoController():
            gpu_info = adapter.Name
    except Exception as e:
        pass
    return gpu_info

def get_ram_size():
    ram_size = psutil.virtual_memory().total / (1024**3)  # in GB
    return ram_size

def get_screen_size():
    screen = screeninfo.get_monitors()[0]
    diagonal = ((screen.width ** 2) + (screen.height ** 2)) ** 0.5
    return f"{diagonal / 25.4:.1f} inch"

def get_network_info():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)])
    public_ip = socket.gethostbyname(socket.gethostname())
    return mac_address, public_ip

def get_windows_version():
    windows_version = platform.platform()
    return windows_version

if __name__ == "__main__":
    installed_software = get_installed_software()
    download_speed, upload_speed = get_internet_speed()
    screen_width, screen_height = get_screen_resolution()
    cpu_info = get_cpu_info()
    gpu_info = get_gpu_info()
    ram_size = get_ram_size()
    screen_size = get_screen_size()
    mac_address, public_ip = get_network_info()
    windows_version = get_windows_version()

    # Printing system details in a user-friendly format
    print("Installed Software:", installed_software)
    print("Internet Speed (Download, Upload):", download_speed, "Mbps,", upload_speed, "Mbps")
    print("Screen Resolution:", screen_width, "x", screen_height)
    print("CPU Model:", cpu_info["Model"])
    print("Number of Cores:", cpu_info["Cores"])
    print("Number of Threads:", cpu_info["Threads"])
    print("GPU Model:", gpu_info)
    print("RAM Size:", ram_size, "GB")
    print("Screen Size:", screen_size)
    print("MAC Address:", mac_address)
    print("Public IP Address:", public_ip)
    print("Windows Version:", windows_version)
