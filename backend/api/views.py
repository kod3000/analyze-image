import base64
import string
import tempfile
import random
import os
import requests
import zipfile
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser
from wsgiref.util import FileWrapper
from .serializers import FileUploadSerializer
from .vision_processing import process_vision

SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/png']  # TODO : Add PDF and Video support
THUMBNAIL_SIZE = (128, 128)
RESIZED_IMAGE_SIZE = (512, 512)


class HealthStatusView(APIView):
    """
    General health status of the API
    """

    def get(self, request):
        return JsonResponse({'status': 'healthy'}, status=status.HTTP_200_OK)


class ServeThumbnailView(APIView):
    """
    Serve thumbnails back for the API response
    """
    def get(self, request, filename):
        thumbnails_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/thumbnails')
        image_path = os.path.join(thumbnails_folder, filename)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                response = HttpResponse(FileWrapper(image_file), content_type='image/png')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        else:
            # Return a 404 Not Found response if the image doesn't exist
            # TODO : Create a placeholder image for the thumbnail if it doesn't exist
            return JsonResponse({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)


class ImageApiQueryUploadView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser, JSONParser)
    """
    Image API Query Upload View
    """

    def post(self, request):
        uploaded_file = request.FILES.get('uploaded_file')
        if uploaded_file.content_type not in SUPPORTED_IMAGE_TYPES:
            return JsonResponse({'error': 'The file type is not suppoerted'}, status=status.HTTP_400_BAD_REQUEST)

        unique_prefix = "aiv_" + self.generate_unique_ai_vision_prefix()
        resized_image_path, thumbnail_path, zip_path = self.process_images(uploaded_file, unique_prefix)
        data = self.prepare_data(resized_image_path, thumbnail_path, zip_path)

        serializer = FileUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # send to AI Vision
            openai_response = process_vision(data['ready_up_base64'], True)  # Set to False to test error handling
            # TODO : Handle openai_response['error'] via server logs
            # if openai_response['error']:
            #     print(openai_response['error'])

            # TODO: save response to db


            # give back data on response
            response = {
                'message': 'Image uploaded successfully',
                'thumbnail': serializer.data['thumbnail'],
                'openai_response': openai_response,
            }
            return JsonResponse(response, status=status.HTTP_200_OK)

        response_error = {
            'error': 'Apologize',
            'message': 'Something went wrong... Please try again later.',
            'more_info': serializer.errors,
        }
        return JsonResponse(response_error, status=status.HTTP_400_BAD_REQUEST)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_unique_ai_vision_prefix(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

    def fetch_api_key(self):
        return requests.get("https://api.openai.com/v1/engines").json()

    def prepare_data(self, resized_image_path, thumbnail_path, zip_path):
        data = {}
        for file_path, key in [(resized_image_path, 'resized_file'), (thumbnail_path, 'thumbnail'),
                               (zip_path, 'zip_file')]:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                data[key] = ContentFile(file_content, name=os.path.basename(file_path))
                if key == 'resized_file':
                    # save data as base64 before deleting
                    data['ready_up_base64'] = self.encode_image(file_path)
            os.remove(file_path)
        return data

    def process_images(self, uploaded_file, unique_prefix):
        original_image = Image.open(uploaded_file)
        resized_image_path = self.save_image_with_background(original_image, RESIZED_IMAGE_SIZE, 'resized',
                                                             uploaded_file.name, unique_prefix)
        thumbnail_path = self.save_resized_image(original_image, THUMBNAIL_SIZE, 'thumbnail', uploaded_file.name,
                                                 unique_prefix)
        zip_path = self.save_in_zip(uploaded_file, 'original', uploaded_file.name, unique_prefix)
        return resized_image_path, thumbnail_path, zip_path

    def save_image_with_background(self, image, size, prefix, original_name, unique_prefix):
        background = Image.new('RGB', size, (0, 0, 0))
        resized_image = image.copy()
        resized_image.thumbnail(size)
        background.paste(resized_image, ((size[0] - resized_image.width) // 2, (size[1] - resized_image.height) // 2))
        return self.save_temp_image(background, prefix, original_name, unique_prefix)

    def save_in_zip(self, file, prefix, original_name, unique_prefix):
        _, ext = os.path.splitext(original_name)
        zip_path = tempfile.NamedTemporaryFile(delete=False, suffix='.zip', prefix=f'{prefix}_{unique_prefix}_').name
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            file.seek(0)
            zip_file.writestr(f'{unique_prefix}_{prefix}{ext}', file.read())
        return zip_path

    def save_resized_image(self, image, size, prefix, original_name, unique_prefix):
        resized_image = image.copy()
        resized_image.thumbnail(size)
        return self.save_temp_image(resized_image, prefix, original_name, unique_prefix)

    def save_temp_image(self, image, prefix, original_name, unique_prefix):
        _, ext = os.path.splitext(original_name)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext, prefix=f'{prefix}_{unique_prefix}_')
        image.save(temp_file, format=image.format)
        return temp_file.name
