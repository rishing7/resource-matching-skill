# your_app/management/commands/create_resource.py

from django.core.management.base import BaseCommand
from resources.models import ResourceDetail

RESOURCE_LIST = [
    {
        "name": "Rishikesh",
        "skills": ["Python", "Django", "AWS"],
        "from_date": "2024-09-01",
        "to_date": "2024-09-30",
    },
    {
        "name": "Rishi",
        "skills": ["MySQL", "Postgres"],
        "from_date": "2024-09-10",
        "to_date": "2024-10-15",
    },
    {
        "name": "Raj",
        "skills": ["AWS"],
        "from_date": "2024-09-01",
        "to_date": "2024-09-25",
    },
]


class Command(BaseCommand):
    help = "Create a new resource with name, skills, and availability"

    def handle(self, *args, **kwargs):
        # TODO: Duplicate entries could be avoided
        ResourceDetail.objects.bulk_create(
            [ResourceDetail(**item) for item in RESOURCE_LIST]
        )
        self.stdout.write(
            self.style.SUCCESS("Resources have been created successfully.")
        )
