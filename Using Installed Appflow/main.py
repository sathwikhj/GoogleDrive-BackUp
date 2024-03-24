import os
import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = None

if os.path.exists("api_tokens.json"):
    creds = Credentials.from_authorized_user_file("api_tokens.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credenti.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("api_tokens.json", "w") as token:
        token.write(creds.to_json())

try:
    service=build("drive","v3",credentials=creds)
    response = service.files().list(
        q="name='CC_BackUp' and mimeType='application/vnd.google-apps.folder'",
        spaces="drive"
    ).execute()
    
    print("Response:", response) 
    
    if 'files' in response and not response['files']:
        file_metadata = {
            "name": "CC_BackUp",
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
        "parents": ["1iL1vzmXQMtsDxWVJ08YOnDC-08hhwVV-"],
        "mimeType": "application/vnd.google-apps.folder"
    }
    datetime_folder = service.files().create(body=file_metadata, fields="id").execute()
    datetime_folder_id = datetime_folder.get('id')

    assignment_folder_path = 'assignment'
    if not os.path.exists(assignment_folder_path):
        print("File not found")
    else:
        count=0
        for filename in os.listdir('assignment'):
            file_metadata = {
                "name": filename,
                "parents": [datetime_folder_id]
            }
            media = MediaFileUpload(f"assignment/{filename}")
            upload_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print("Backed Up file:", filename)
            count+=1
        print("Files in the folder: "+str(count))

except Exception as e:
    print("Error:", str(e))
