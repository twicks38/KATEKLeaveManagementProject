from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    #allows djanago to use the signals.py to setup and assign roles
    def ready(self):
        import accounts.signals
