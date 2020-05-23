from django.test import TestCase, override_settings
from PIL import Image
from io import BytesIO ## for Python 3
from django.core.files.base import ContentFile
import random
import os


def get_document():
    __dir__ = os.path.dirname(os.path.realpath(__file__))
    pdf_file = open(__dir__ + '/fixtures/test.png','rb')
    return ContentFile(pdf_file.read(), 'example.png')


@override_settings(THEME=None)
class VotaInteligenteTestCase(TestCase):
    fixtures = ['mini_2.yaml']

    def setUp(self):
        super(VotaInteligenteTestCase, self).setUp()

    def get_image(self):
        image_file = BytesIO()
        color1 = random.randint(0, 255)
        color2 = random.randint(0, 255)
        color3 = random.randint(0, 255)
        image = Image.new('RGBA', size=(50, 50), color=(color1, color2, color3))
        image.save(image_file, 'png')
        image_file.seek(0)
        return ContentFile(image_file.read(), 'test.png')
