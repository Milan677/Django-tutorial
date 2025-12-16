from django.urls import path
from .views import *

urlpatterns = [
   path('get-folders-from-drive/',list_folders_api),
   path('get-files-from-drive/<str:folder_id>/',list_files),

   path('create-folder-in-drive/',create_folder_in_drive),
   path('upload-file-to-drive/',upload_file_to_drive),
]