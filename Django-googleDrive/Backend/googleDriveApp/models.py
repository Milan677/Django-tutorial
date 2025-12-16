
import uuid
from django.conf import settings
from django.db import models



class DriveFolder(models.Model):
    folder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    

    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="drive_folders"
    # )

    name = models.CharField(max_length=255)
    google_folder_id = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class DriveFile(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(DriveFolder, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    google_file_id = models.CharField(max_length=255, unique=True)

    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField(null=True, blank=True)

    web_view_link = models.URLField(null=True, blank=True)
    web_content_link = models.URLField(null=True, blank=True)
    thumbnail_link = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
