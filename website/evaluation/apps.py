from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .db_triggers import create_score_backup_trigger


class DscivConfig(AppConfig):
    name = 'evaluation'

    def ready(self):
        post_migrate.connect(create_score_backup_trigger, sender=self)
