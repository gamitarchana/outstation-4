from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7@-qr1ld5e44q@m@!zegp#6dzfak9)yuua#p0md4@v#n$o*&-x'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'archana-pc', '192.168.1.100']


try:
    from .local import *
except ImportError:
    pass
