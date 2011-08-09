import os.path
from django.conf import settings

TAGGIT_ROOT = os.path.normpath(os.path.dirname(__file__))
TAGGIT_MEDIA_DIR = getattr(settings, 'TAGGIT_MEDIA_DIR', os.path.join(TAGGIT_ROOT, 'media'))
