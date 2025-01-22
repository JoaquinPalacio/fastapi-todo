# basemodel -> define modelos de datos 
# fiel -> define metadatos adicionales (como _id)
from pydantic import BaseModel, Field
# optional -> permite que el campo sea opcional
from typing import Optional
# bson -> maneja los objetos id
from bson import ObjectId


# clase para manejar los objetos id
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    # valida que el objeto id sea valido -- sino lanza una excepcion
    @classmethod
    def validate(cls, v, values=None, **kwargs):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    # define que el id sea string en los esquemas json
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


# modelo de la tarea
class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    completed: bool = False

    class Config:
        # permite poblar los campos por nombre
        populate_by_name = True
        # permite que el id sea un string
        arbitrary_types_allowed = True
        # define que el id sea string en los esquemas json
        json_encoders = {ObjectId: str}