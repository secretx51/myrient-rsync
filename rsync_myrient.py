import os
import zipfile
from sh import rsync
from tqdm import tqdm

RSYNC_HOME = 'rsync://rsync.myrient.erista.me/files/No-Intro/'
DOWNLOAD_DIR = 'downloads'
DELETE_ZIP = True
SYSTEMS = [] # Add name of system directories for specific downloads, skips system whitelist/blacklist

SYSTEM_WHITELIST = ["Nintendo DS (Decrypted)"]
SYSTEM_BLACKLIST = ["Private"]
GAME_WHITELIST = ["Pokemon", "USA"]
GAME_BLACKLIST = ["Demo"]

def get_rsync_files(rsync_url):
    # Use rsync to list files in the directory
    print(f'Downloading from: {rsync_url}')
    try:
        rsync_output = rsync("--list-only", rsync_url)
        files_list = rsync_output.split("\n") 
        return files_list
    except Exception as e:
        print("Error:", e)
        return []

def filter_files(files_list):
    # Filter files based on criteria
    return [file_name.split(':')[-1][2:].strip() for file_name in files_list]

def filter_white(file_names, filter_terms):
    # Filter files based on criteria
    return [file_name for file_name in file_names if all(term in file_name for term in filter_terms)]

def filter_black(file_names, filter_terms):
    return [file_name for file_name in file_names if not all(term in file_name for term in filter_terms)]

def apply_filters(file_names, white_filter, black_filter):
    filtered_files = filter_files(file_names)
    if white_filter:
        filtered_files = filter_white(filtered_files, white_filter)
    if black_filter:
        filtered_files = filter_black(filtered_files, black_filter)
    return filtered_files

def getSystemURLs():
    # Get list of files from rsync directory
    system_list = get_rsync_files(RSYNC_HOME)
    # Filter files based on criteria
    filt_systems =  apply_filters(system_list, SYSTEM_WHITELIST, SYSTEM_BLACKLIST)
    print(filt_systems)
    return filt_systems

def makeDownloadDir(download_dir):
    # Create download directory
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def unzipFile(zip_file, rom_path, file_name):
    # Unzip the file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(rom_path)
    print("Unzipped:", file_name)
    if DELETE_ZIP:
        # Delete the original zip file
        os.remove(zip_file)
        print("Deleted original zip file:", file_name)

def download_files(filtered_files, rsync_url, download_dir):
    # Download filtered files
    for file_name in tqdm(filtered_files, desc="Downloading files", unit="file"):
        # Path setup
        file_url = os.path.join(rsync_url, file_name)
        zip_path = makeDownloadDir(f'{download_dir}/zips')
        zip_file = os.path.join(zip_path, file_name)
        rom_path = makeDownloadDir(f'{download_dir}/roms')
        # Rsync and unzip files
        rsync("-avz", file_url, zip_file)
        print("Downloaded:", file_name)
        unzipFile(zip_file, rom_path, file_name)

def downloadGames(system):
    rsync_url = f'{RSYNC_HOME}{system}/'
    # Get list of files from rsync directory
    files_list = get_rsync_files(rsync_url)
    # Filter files based on criteria
    filtered_files = apply_filters(files_list, GAME_WHITELIST, GAME_BLACKLIST)
    download_dir = os.path.join(DOWNLOAD_DIR, system)
    # Download filtered files
    download_files(filtered_files, rsync_url, download_dir)

def main():
    # Get list of systems
    if not SYSTEMS:
        for system in getSystemURLs():
            downloadGames(system)
    else:
        for system in SYSTEMS:
            downloadGames(system)

if __name__ == "__main__":
    main()
