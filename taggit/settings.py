from os.path import normpath, dirname, join

from django.conf import settings


TAGGIT_ROOT = normpath(dirname(__file__))
TAGGIT_MEDIA_DIR = getattr(settings, 'TAGGIT_MEDIA_DIR', join(TAGGIT_ROOT, 'media'))
TAGGIT_AUTOCOMPLETE_WIDGET = getattr(settings, 'TAGGIT_AUTOCOMPLETE_WIDGET', False)
TAGGIT_FORCE_LOWERCASE = getattr(settings, 'TAGGIT_FORCE_LOWERCASE', False)
TAGGIT_STOPWORDS = getattr(settings, 'TAGGIT_STOPWORDS', None)
TAGGIT_ENABLE_SPACE_SPLIT_IF_NOT_QUOTES = getattr(settings, 'TAGGIT_ENABLE_SPACE_SPLIT_IF_NOT_QUOTES', True)
