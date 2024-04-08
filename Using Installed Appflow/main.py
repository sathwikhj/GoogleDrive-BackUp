import os
import os.path
import logging
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = None

if os.path.exists("api_tokens.json"):
    creds = Credentials.from_authorized_user_file("api_tokens.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("api_tokens.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("drive", "v3", credentials=creds)
    response = service.files().list(
        q="name='<Folder-Name>' and mimeType='application/vnd.google-apps.folder'",  # In the name tag, provide the name for backup folder
        spaces="drive"
    ).execute()

    logging.info("Response: %s", response)

    if 'files' in response and not response['files']:
        file_metadata = {
            "name": "<Folder-Name>",  # Name of Google Drive folder where you want the backups to be stored
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = service.files().create(body=file_metadata, fields="id").execute()
        folder_id = folder.get('id')
    elif 'files' in response and response['files']:
        folder_id = response['files'][0]['id']
    else:
        raise Exception("Response does not contain 'files' key or is empty.")

    backup_date_folder_name = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    file_metadata = {
        "name": backup_date_folder_name,
        "parents": ["folder_id"],
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
