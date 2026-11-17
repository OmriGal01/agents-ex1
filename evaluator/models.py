from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    is_acceptable: bool = Field(
        ...,
        description="Whether the candidate answer meets all evaluation criteria.",
    )
    feedback: str = Field(
        ...,
        description=(
            "Short reasoning for the decision. In case of rejection, a detailed "
            "explanation of the issue and actionable instructions for fixing it."
        ),
    )
