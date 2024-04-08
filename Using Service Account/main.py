import os
import os.path
import logging
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = None

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

service = build("drive", "v3", credentials=creds)

try:
    backup_date_folder_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    file_metadata = {
        "name": backup_date_folder_name,
        "parents": ["<folder-id>"],  # Add folder id as mentioned in the image
        "mimeType": "application/vnd.google-apps.folder"
    }
    datetime_folder = service.files().create(body=file_metadata, fields="id").execute()
    datetime_folder_id = datetime_folder.get('id')

    assignment_folder_path = '<Folder-path>'  # Provide path to the folder on the local system which you want backed up
    if not os.path.exists(assignment_folder_path):
        logging.error("File not found")
    else:
        count = 0
        for filename in os.listdir('<Name of the directory>'):  # Provide the name of the directory
            file_metadata = {
                "name": filename,
                "parents": [datetime_folder_id]
            }
            media = MediaFileUpload(f"<Name of the directory>/{filename}")  # Provide the name of the directory
            upload_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            logging.info("Backed Up file: %s", filename)
            count += 1
        logging.info("Files in the folder: %d", count)

except Exception as e:
    logging.error("Error: %s", str(e))
