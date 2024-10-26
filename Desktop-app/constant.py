import json
import platform
import os
import logging
import socket

# Define the logger configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s %(name)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Create the logger instance
logger = logging.getLogger('FileSharing: ')

# Set the logger level to debug
logger.setLevel(logging.DEBUG)

# Define the config file name and current version
config_file_name = ".config.json"
current_version = "4"  # Set the current version of the configuration

def get_config_file_path():
    # Get the home directory and create a DataDash folder in the appropriate cache location
    if platform.system() == 'Windows':
        cache_dir = os.path.join(os.getenv('APPDATA'), 'DataDash')
    elif platform.system() == 'Linux':
        cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'DataDash')
    elif platform.system() == 'Darwin':  # macOS
        cache_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'DataDash')
    else:
        logger.error("Unsupported OS!")
        return None

    os.makedirs(cache_dir, exist_ok=True)
    logger.info("Config directory created/ensured: %s", cache_dir)
    return os.path.join(cache_dir, config_file_name)
#com.an.Datadash

config_file = get_config_file_path()
if config_file is None:
    exit(1)  # Exit if the config file path is not valid

def get_default_path():
    if platform.system() == 'Windows':
        file_path = "C:\\Received"
    elif platform.system() == 'Linux':
        home_dir = os.path.expanduser('~')
        os.makedirs(os.path.join(home_dir, "received"), exist_ok=True)
        file_path = os.path.join(home_dir, "received")
    elif platform.system() == 'Darwin':
        home_dir = os.path.expanduser('~')
        documents_dir = os.path.join(home_dir, "Documents")
        os.makedirs(os.path.join(documents_dir, "received"), exist_ok=True)
        file_path = os.path.join(documents_dir, "received")
    else:
        logger.error("Unsupported OS!")
        file_path = None
    logger.info("Default path determined: %s", file_path)
    return file_path

def write_config(data, filename=config_file):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    logger.info("Configuration written to %s", filename)

def get_config(filename=config_file):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        logger.info("Loaded configuration from %s", filename)
        return data
    except FileNotFoundError:
        logger.warning("Configuration file %s not found. Returning empty config.", filename)
        return {}
    #com.an.Datadash

# Check if the config file exists, and if not, create it
if not os.path.exists(config_file):
    file_path = get_default_path()

    default_config = {
        "version": current_version,  # Add version number
        "device_name": platform.node(),
        "save_to_directory": file_path,
        "max_filesize": 1000,
        "encryption": False,
        "android_encryption": False,
        "show_warning": True
    }

    write_config(default_config, config_file)
    logger.info("Created new configuration file.")

else:
    # Load the existing configuration
    config_data = get_config(config_file)

    # Check if version exists and matches
    if "version" not in config_data or config_data["version"] != current_version:
        logger.warning("Configuration version mismatch or missing. Overwriting with default config.")
        file_path = get_default_path()
        
        # Write the new default configuration
        default_config = {
            "version": current_version,  # Ensure the version number is included
            "device_name": platform.node(),
            "save_to_directory": file_path,
            "max_filesize": 1000,
            "encryption": False,
            "android_encryption": False,
            "show_warning": True
        }
        
        write_config(default_config, config_file)
    else:
        logger.info("Loaded configuration: %s", config_data)
        #com.an.Datadash

def get_broadcast():
    try:
        # Create a socket to connect to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Attempt to connect to an external server (this will not send data)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        logger.info("Local IP determined: %s", local_ip)
    except Exception as e:
        logger.error("Error obtaining local IP: %s", e)
        local_ip = "Unable to get IP"
    finally:
        s.close()
    
    if local_ip == "Unable to get IP":
        return local_ip

    # Split the IP address into parts
    ip_parts = local_ip.split('.')
    # Replace the last part with '255' to create the broadcast address
    ip_parts[-1] = '255'
    # Join the parts back together to form the broadcast address
    broadcast_address = '.'.join(ip_parts)
    logger.info("Broadcast address determined: %s", broadcast_address)
    return broadcast_address
#com.an.Datadash

BROADCAST_ADDRESS = get_broadcast()
BROADCAST_PORT = 12345
LISTEN_PORT = 12346

logger.info("Broadcast address: %s, Broadcast port: %d, Listen port: %d", BROADCAST_ADDRESS, BROADCAST_PORT, LISTEN_PORT)
#com.an.Datadash
