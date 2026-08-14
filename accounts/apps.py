from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_Auto_field = "django.db.models.BigAutoField"
    name = 'accounts'

    #allows djanago to use the signals.py to setup and assign roles
    def ready(self):
        import accounts.signals
