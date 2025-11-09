import tempfile
import shutil
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Villa, VillaImage


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class VillaImageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # create a superuser for image upload permissions
        self.user = User.objects.create_superuser(email='admin@example.com', name='Admin', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.villa = Villa.objects.create(title='Test Villa', city='Test City')

    def tearDown(self):
        # cleanup media
        shutil.rmtree(self._get_media_root(), ignore_errors=True)

    def _get_media_root(self):
        # the override_settings decorator set a tempdir; read from settings
        from django.conf import settings
        return settings.MEDIA_ROOT

    def test_model_validation_requires_image(self):
        vi = VillaImage(villa=self.villa, caption='no image')
        with self.assertRaises(Exception):
            # full_clean should raise ValidationError
            vi.full_clean()

    def test_image_upload_endpoint(self):
        # create a small valid JPEG file in memory using Pillow
        from io import BytesIO
        try:
            from PIL import Image
        except Exception:
            Image = None
        if Image:
            bio = BytesIO()
            img_obj = Image.new('RGB', (10, 10), color='red')
            img_obj.save(bio, 'JPEG')
            bio.seek(0)
            img = SimpleUploadedFile('test.jpg', bio.read(), content_type='image/jpeg')
        else:
            # fallback: use minimal JPEG header (may fail on strict validators)
            img = SimpleUploadedFile('test.jpg', b'\xff\xd8\xff\xd9', content_type='image/jpeg')
        url = '/api/villas/villa-images/'
        data = {
            'villa': str(self.villa.id),
            'image': img,
            'caption': 'API upload',
            'type': 'media',
            'is_primary': True,
            'order': 0,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201, msg=response.content)
        # ensure image record created and image_url present
        self.assertIn('image_url', response.data)
        vi = VillaImage.objects.get(pk=response.data['id'])
        self.assertTrue(bool(vi.image))
