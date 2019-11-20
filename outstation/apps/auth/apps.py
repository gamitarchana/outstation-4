from django.apps import AppConfig
#from . import checks  # NOQA

class AuthAppConfig(AppConfig):
    name = 'outstation.apps.auth'
    label = 'outstationauth'
    verbose_name = "Outstation Authentication"
