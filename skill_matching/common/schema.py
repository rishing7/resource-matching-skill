from marshmallow import fields


class TrimmedString(fields.String):
    def __init__(self, **kwargs):
        super(TrimmedString, self).__init__(**kwargs)

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, "strip"):
            value = value.strip()
        return super()._deserialize(value, *args, **kwargs)
