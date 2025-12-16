import os
import mimetypes
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from django.conf import settings

# Path to Google Service Account JSON Key
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, "googleDriveApp", "service_accounts.json")

# Ensure the service account file exists
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise FileNotFoundError(f"❌ Service account file not found at: {SERVICE_ACCOUNT_FILE}")

# Google Drive API Scopes
SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    drive_service = build("drive", "v3", credentials=creds)
    return drive_service