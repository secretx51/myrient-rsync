# Myrient Rsync

## rsync_myrient.py

This script is used to download files from a remote server using rsync. It allows you to specify a whitelist and blacklist for both systems and games. The script will only download files that match the whitelist and do not match the blacklist.

### Prerequisites

- Python 3.x
- rsync
- tqdm
- sh

You can install the Python dependencies with pip:

```bash
pip install -r requirements.txt
```
### Configuration

You can configure the script by modifying the following variables at the top of the script:

- `RSYNC_HOME`: The rsync URL to download from.
- `DOWNLOAD_DIR`: The directory to download files to.
- `DELETE_ZIP`: Whether to delete the zip file after extraction.
- `SYSTEMS`: List of system directories for specific downloads, skips system whitelist/blacklist.
- `SYSTEM_WHITELIST`: List of systems to download.
- `SYSTEM_BLACKLIST`: List of systems to not download.
- `GAME_WHITELIST`: List of games to download.
- `GAME_BLACKLIST`: List of games to not download.

### Usage

You can run the script with Python:

```bash
python rsync_myrient.py
```
This will download the files to the specified directory.

### Functions

- `get_rsync_files(rsync_url)`: This function uses rsync to list files in the directory and returns a list of files.
- `filter_files(files_list)`: This function is not fully implemented yet. It is intended to filter the files based on the whitelist and blacklist.

### Example

If you want to download all Pokemon games for the Nintendo DS, you could configure the script like this:

```python
RSYNC_HOME = 'rsync://rsync.myrient.erista.me/files/No-Intro/'
DOWNLOAD_DIR = 'downloads'
DELETE_ZIP = True
SYSTEMS = [] 
SYSTEM_WHITELIST = ["Nintendo DS (Decrypted)"]
SYSTEM_BLACKLIST = ["Private"]
GAME_WHITELIST = ["Pokemon", "USA"]
GAME_BLACKLIST = ["Demo"]
```
