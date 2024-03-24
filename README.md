## Google Drive Backup Script

This Python script allows you to back up files to Google Drive using the Google Drive API.<br>
This repository allows you to **containerise** the code and uses **Kubernetes** to backup in intervals of time.

### Prerequisites

Before running the script, make sure you have the following:

- Python installed on your system (preferably Python 3.x).
- Google account with access to Google Drive.
- Google account registered to Google Cloud Platform which has access to the drive api.
- Rename the json file as Credentials.json.

### Installation

1. Clone or download the repository containing the script.
2. Ensure all dependencies are installed. You can install them using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

