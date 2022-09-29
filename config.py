from os.path import abspath, dirname, join
# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))
# Media dir
MEDIA_DIR = join(BASE_DIR, 'media')
POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')

class Config(object):
    SECRET_KEY = 'michifuntis'

class DevConfig(Config):
     DEBUG = True