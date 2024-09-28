from marshmallow import fields, Schema
from common.schema import TrimmedString


class ResourceDetailSchema(Schema):
    name = TrimmedString(required=True)
    skills = fields.List(fields.Str(), required=True)
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)


class TasksDetailSchema(Schema):
    name = TrimmedString(required=True)
    skills = fields.List(fields.Str(), required=True)
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)


class ProjectDetailSchema(Schema):
    name = TrimmedString(required=True)
    # tasks = fields.List(
    #     fields.Nested(TasksDetailSchema, load_only=True), required=False
    # )
