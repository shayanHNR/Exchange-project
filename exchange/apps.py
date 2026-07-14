from django.apps import AppConfig


class ExchangeConfig(AppConfig):
    name = 'exchange'
    verbose_name='صرافی'

    def ready(self):
        import exchange.signals