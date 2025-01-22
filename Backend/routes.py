from fastapi import APIRouter, HTTPException, status
# manejo de objetos id en mongodb
from bson import ObjectId
# modelo de la tarea
from models import TodoModel
from typing import List

router = APIRouter()


# listar todas las tareas
@router.get("/", response_model=List[TodoModel])
async def list_todos():
    # se obtienen las primeras 1000 tareas
    todos = await router.mongodb.todos.find().to_list(1000)
    # se retornan las tareas iterando sobre cada una
    return [TodoModel(**todo) for todo in todos]


# obtener una tarea por id -- parametro: el id de la tarea
@router.get("/{id}", response_model=TodoModel)
async def get_todo(id: str):
    # se verifica que la tarea exista
    if (todo := await router.mongodb.todos.find_one({"_id": ObjectId(id)})) is not None:
        # se retorna la tarea
        return TodoModel(**todo)
    # se lanza una excepcion si la tarea no existe
    raise HTTPException(status_code=404, detail=f"Todo {id} not found")


# crear una tarea -- parametro: una tarea con el modelo todomodel
@router.post("/", response_model=TodoModel)
async def create_todo(todo: TodoModel):
    # genera un diccionario de la tarea excluyendo el id (se genera automaticamente)
    todo_dict = todo.model_dump(by_alias=True, exclude=["id"])
    # se inserta en la base de datos
    new_todo = await router.mongodb.todos.insert_one(todo_dict)
    # se busca la tarea insertada
    created_todo = await router.mongodb.todos.find_one({"_id": new_todo.inserted_id})
    # se retorna la tarea insertada
    return TodoModel(**created_todo)


# actualizar una tarea -- parametro: el id de la tarea y la tarea con el modelo todomodel
@router.put("/{id}", response_model=TodoModel)
async def update_todo(id: str, todo: TodoModel):
    # se genera un diccionario de los nuevos datos de la tarea excluyendo el id
    todo_dict = todo.model_dump(by_alias=True, exclude=["id"])
    # se verifica que la tarea exista
    if (existing_todo := await router.mongodb.todos.find_one({"_id": ObjectId(id)})) is not None:
        # se actualiza la tarea en la base de datos con el mismo id y los nuevos datos
        update_result = await router.mongodb.todos.update_one(
            {"_id": ObjectId(id)}, {"$set": todo_dict}
        )
        # se verifica que la tarea haya sido actualizada
        if update_result.modified_count == 1:
            # se busca la tarea actualizada
            if (updated_todo := await router.mongodb.todos.find_one({"_id": ObjectId(id)})) is not None:
                # se retorna la tarea actualizada
                return TodoModel(**updated_todo)
    # se lanza una excepcion si la tarea no existe
    raise HTTPException(status_code=404, detail=f"Todo {id} not found")


# borrar una tarea -- parametro: el id de la tarea
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: str):
    # se elimina de la base de datos la tarea con el id dado
    delete_result = await router.mongodb.todos.delete_one({"_id": ObjectId(id)})
    # se verifica que la tarea haya sido eliminada
    if delete_result.deleted_count == 0:
        # se lanza una excepcion si no se elimino ninguna tarea
        raise HTTPException(status_code=404, detail=f"Todo {id} not found")