from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from common import api_exceptions
from common.decorators import validate_json_request
from resources.models import ResourceDetail, ProjectDetail, TaskInfo
from common.responses.success import RESOURCE_LIST


@require_http_methods(["GET"])
@api_exceptions.api_exception_handler
@validate_json_request
def matched_resources(request):
    """
    @apiDescription Fetch Resource Matching
    This API could be used to fetch resource matchin as per project name
    @api {get} /api/v1/matched-resources/ Fetch Matched Resource
    @apiName Fetch Matched Resource
    @apiGroup Resources

    @apiHeader {String} Content-Type application/json
    @apiParam {String} name Project Name of the System

    @apiSuccessExample {json} Success-Response: For Valid Project Name
    HTTP/1.1 200 OK
    {
        "message": "Information has been extracted successfully.",
        "data": [
            {
                "name": "Rishikesh",
                "skills": [
                    "Python",
                    "C"
                ]
            }
        ],
        "statuc_code": 200
    }

    @apiSuccessExample {json} Success-Response: For Invalid Project Name
    HTTP/1.1 200 OK
    {
        "message": "Information has been extracted successfully.",
        "data": [],
        "statuc_code": 200
    }
    @apiParamExample {json} Request-Example: Resource Details
    {
        [
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
    }

    @apiParamExample {json} Request-Example: Project Tasks Mapping
    {
        [
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
    }

    """

    obj = ProjectDetail.objects.filter(name=request.GET.get("name"))
    response_data = []
    if obj.exists():
        # TODO: Only for unique project name exist in the system
        tasks = TaskInfo.objects.filter(project=obj.first())
        for task in tasks:

            # TODO: Apply subset filter for skills subset.
            resources = ResourceDetail.objects.filter(
                from_date__lte=task.from_date,
                to_date__gte=task.to_date,
            )
            for res in resources:
                # Serialize the object data
                if set(task.skills).issubset(set(res.skills)):
                    response_data.append({"name": res.name, "skills": res.skills})

    return JsonResponse(
        {"message": RESOURCE_LIST, "data": response_data, "statuc_code": 200},
        status=200,
    )
