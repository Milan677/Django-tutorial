from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .drive_utils import get_drive_service
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import tempfile
import os

# Create your views here.

@api_view(['GET'])
def list_folders_api(request):
    parent_id = request.query_params.get('parent_id') or None

    try:
        service = get_drive_service()

        query = "mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = service.files().list(
            q=query,
            fields="files(id, name)",
            pageSize=100
        ).execute()

        folders = results.get("files", [])

        return Response(
            {
                "success": True,
                "count": len(folders),
                "data": folders
            },
            status=status.HTTP_200_OK
        )

    # 🔹 Google API specific errors
    except HttpError as e:

        return Response(
            {
                "success": False,
                "message": "Failed to fetch folders from Google Drive",
                "details": str(e)
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # 🔹 Invalid parent_id or bad request
    except ValueError as e:
       
        return Response(
            {
                "success": False,
                "message": "Invalid request parameters",
                "details": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔹 Catch-all (last line of defense)
    except Exception as e:

        return Response(
            {
                "success": False,
                "message": "Internal server error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def list_files(request, folder_id):
    if not folder_id:
        return Response(
            {
                "success": False,
                "message": "folder_id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        service = get_drive_service()

        query = f"'{folder_id}' in parents and trashed=false"

        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields=(
                "files("
                "id, "
                "name, "
                "mimeType, "
                "size, "
                "webViewLink, "
                "webContentLink, "
                "thumbnailLink"
                ")"
            )
        ).execute()


        files = results.get("files", [])

        return Response(
            {
                "success": True,
                "count": len(files),
                "data": files
            },
            status=status.HTTP_200_OK
        )

    # 🔹 Google Drive API errors (auth, permission, rate limit)
    except HttpError as e:
        return Response(
            {
                "success": False,
                "message": "Failed to fetch files from Google Drive",
                "details": str(e)
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # 🔹 Unexpected server errors
    except Exception as e:
        return Response(
            {
                "success": False,
                "message": "Internal server error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 

@api_view(['POST'])
def create_folder_in_drive(request):
    folder_name = request.data.get("name")
    parent_id = request.data.get("parent_id")
    
    try:
        service = get_drive_service()

        file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()

        return Response({
            "id":folder['id'],
            "name":folder["name"]
        })

    # 🔹 Google API specific errors
    except HttpError as e:

        return Response(
            {
                "success": False,
                "message": "Failed to fetch folders from Google Drive",
                "details": str(e)
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # 🔹 Invalid parent_id or bad request
    except ValueError as e:
       
        return Response(
            {
                "success": False,
                "message": "Invalid request parameters",
                "details": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔹 Catch-all (last line of defense)
    except Exception as e:

        return Response(
            {
                "success": False,
                "message": "Internal server error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def upload_file_to_drive(request):
    file = request.FILES['file']
    folder_id = request.data['folder_id']

    try:
        service = get_drive_service()

        # Save the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        file_metadata = {
            "name": file.name,
            "parents": [folder_id]
        }

        media = MediaFileUpload(
            temp_file_path,
            resumable=True
        )

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields=(
                "id, "
                "name, "
                "mimeType, "
                "size, "
                "webViewLink, "
                "webContentLink, "
                "thumbnailLink"
            )
        ).execute()

        return Response(
            {
                "success": True,
                "message": "File uploaded successfully",
                "data": uploaded_file
            },
            status=status.HTTP_201_CREATED
        )

    except HttpError as e:
        return Response(
            {
                "success": False,
                "message": "Failed to upload file to Google Drive",
                "details": str(e)
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": "Internal server error"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    finally:
        # 🧹 ALWAYS clean up temp file
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
