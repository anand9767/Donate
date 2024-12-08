from django.apps import AppConfig
from firebase_admin import credentials, initialize_app


class FirebaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firebase_app'

    def ready(self):

        # This is executed when Django starts
        firebase_credentials_path = '/Users/anand/djangoProjects/donate_project/Donate/firebase_admin_credentials.json'
        # print("sas123",firebase_credentials_path)
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred)
