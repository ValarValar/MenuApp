from pydantic import BaseModel


class DeleteBase(BaseModel):
    deleted: bool

    class Config:
        schema_extra = {
            'example': {
                'deleted': 'True',
            },
        }
