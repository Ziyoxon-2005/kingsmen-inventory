from .settings import *

# Test specific settings
DEBUG = True
TEMPLATE_DEBUG = True

# Use a fast password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use in-memory storage for static files during tests
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Media files configuration for tests
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
MEDIA_URL = '/media/'

# Static files configuration for tests
STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] 