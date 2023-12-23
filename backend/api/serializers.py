from rest_framework import serializers
from .models import FileUpload
from django.utils.crypto import get_random_string
import os

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        # note for our og file we save it in the zip file
        fields = ['resized_file', 'thumbnail', 'zip_file']

    def validate_uploaded_file(self, value):
        # Get the original file name
        original_file_name = value.name

        # Sanitize the file name
        # For example, using a random string and keeping the original extension
        file_extension = os.path.splitext(original_file_name)[1]
        sanitized_file_name = get_random_string(15) + file_extension

        # Update the file name
        value.name = sanitized_file_name

        return value