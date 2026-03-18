import json
from django.core.management.base import BaseCommand
from cards.models import ThaiAddress

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open("thai_address.json", encoding="utf8") as f:
            data = json.load(f)

        for a in data:
            ThaiAddress.objects.create(
                subdistrict=a["subdistrict"],
                district=a["district"],
                province=a["province"],
                zipcode=a["zipcode"]
            )

        self.stdout.write("Import success")