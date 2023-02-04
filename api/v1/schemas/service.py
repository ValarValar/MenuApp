from pydantic import BaseModel


class DeleteBase(BaseModel):
    deleted: bool

    class Config:
        schema_extra = {
            "example": {
                "deleted": "True",
            },
        }


class TestDataBase(BaseModel):
    push_test_data: bool

    class Config:
        schema_extra = {
            "example": {
                "push_test_data": "True",
            },
        }
