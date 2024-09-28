# your_app/management/commands/create_resource.py

from django.core.management.base import BaseCommand
from resources.models import ResourceDetail, ProjectDetail, TaskInfo
from datetime import datetime

PROJECT_TASK_MAPPING = [
    {
        "name": "Software Development Project",
        "tasks": [
            {
                "name": "Backend Development",
                "skills": ["Python", "Django", "REST API"],
                "from_date": "2024-09-01",
                "to_date": "2024-09-15",
            },
            {
                "name": "Frontend Development",
                "skills": ["React", "JavaScript", "CSS"],
                "from_date": "2024-09-16",
                "to_date": "2024-09-30",
            },
        ],
    },
    {
        "name": "IT Infrastructure Upgrade",
        "tasks": [
            {
                "name": "Server Upgrade",
                "skills": ["AWS"],
                "from_date": "2024-09-05",
                "to_date": "2024-09-10",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Create a new resource with name, skills, and availability"

    def handle(self, *args, **kwargs):
        # TODO: Duplicate entries could be avoided
        for item in PROJECT_TASK_MAPPING:
            obj = ProjectDetail.objects.create(name=item["name"])
            for task in item["tasks"]:
                TaskInfo.objects.create(project=obj, **task)

            self.stdout.write(
                self.style.SUCCESS(f'Project "{obj.name}" created successfully.')
            )
