from pydantic import BaseModel


class ReqModel(BaseModel):
    img_link: str
    title: str
    description: str | None
    tags: list[str]


class ResModel(BaseModel):
    img_link: str
    title: str
    description: str | None

    class Config:
        orm_mode = True