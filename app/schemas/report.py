from pydantic import BaseModel


class Report(BaseModel):
    verbose_name: str
    options: list[str]