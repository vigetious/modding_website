from django.apps import AppConfig, apps
import secretballot


class ModConfig(AppConfig):
    name = 'mod'

    def ready(self):
        reviewRating_model = apps.get_model("mod", "ReviewRating")
        secretballot.enable_voting_on(reviewRating_model)
