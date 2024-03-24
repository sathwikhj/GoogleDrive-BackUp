import os
import os.path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
creds = None


creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

service = build("drive", "v3", credentials=creds)

try: 
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
