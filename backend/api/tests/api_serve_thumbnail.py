from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status
import os


class ServeThumbnailViewTest(TestCase):

    def test_image_retrieval(self):
        # Test retrieval of the specific image
        filename = 'thumbnail_aiv_aaa_sample.png'
        response = self.client.get(reverse('thumbnail-serve', args=[filename]))
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads/thumbnails', filename)
        self.assertTrue(os.path.exists(image_path))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attachment; filename="{}"'.format(filename), response['Content-Disposition'])

    def test_image_not_found(self):
        # Test retrieval of a non-existing image
        filename = 'non_existing_image.png'
        response = self.client.get(reverse('thumbnail-serve', args=[filename]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'Image not found'})
