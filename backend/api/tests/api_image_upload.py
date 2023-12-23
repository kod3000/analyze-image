from django.test import TestCase
from unittest.mock import patch, MagicMock
from api.views import ImageApiQueryUploadView
from rest_framework.test import APIRequestFactory
from django.core.files.base import ContentFile


# TODO : Optimize this test

class TestImageApiQueryUploadView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImageApiQueryUploadView.as_view()

    @patch('api.views.ImageApiQueryUploadView.process_images')
    @patch('api.views.ImageApiQueryUploadView.prepare_data')
    def test_post_valid_image(self, mock_prepare_data, mock_process_images):
        # Mock the process_images and prepare_data methods
        mock_process_images.return_value = (
            '/uploads/resized/resized_aiv_aaa_sample.png',
            '/uploads/thumbnail/thumbnail_aiv_aaa_sample.png',
            '/uploads/zips/original_aiv_aaa_sample.zip')

        # Create mock file-like objects for prepare_data
        mock_resized_file = ContentFile(b"resized file content", name='resized_aiv_aaa_sample.png')
        mock_thumbnail_file = ContentFile(b"thumbnail file content", name='thumbnail_aiv_aaa_sample.png')
        mock_zip_file = ContentFile(b"zip file content", name='original_aiv_aaa_sample.zip')

        # TODO: Review after changing the base method
        mock_prepare_data.return_value = {
            'resized_file': mock_resized_file,
            'thumbnail': mock_thumbnail_file,
            'zip_file': mock_zip_file,
            'ready_up_base64': 'base64string'
        }

    def test_post_invalid_image_type(self):
        # Create a request with an invalid image type
        request = self.factory.post('/api/upload', {'uploaded_file': MagicMock(content_type='text/plain')},
                                    format='multipart')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)  # HTTP 400 Bad Request
