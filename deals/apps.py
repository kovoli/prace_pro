from django.apps import AppConfig
from watson import search as watson

class DealsConfig(AppConfig):
    name = 'deals'
    verbose_name = 'Скидки'

    def ready(self):
        deals = self.get_model('Deal')
        watson.register(deals, fields=('name', 'description'))
