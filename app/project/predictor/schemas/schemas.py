
from rest_framework.schemas import AutoSchema
import coreapi
import coreschema

def get_predictor_schema():
    return AutoSchema(
        manual_fields=[
            coreapi.Field(
                "team_event",
                required=True,
                location="form",
                schema=coreschema.Object()
            ),
            coreapi.Field(
                "team",
                required=True,
                location="form",
                schema=coreschema.Object()
            ),
            coreapi.Field(
                "result_type",
                required=True,
                location="form",
                schema=coreschema.Object()
            ),
            coreapi.Field(
                "prediction",
                required=True,
                location="form",
                schema=coreschema.String()
            )
        ]
    )
