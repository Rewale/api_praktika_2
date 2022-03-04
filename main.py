from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

import models

app = FastAPI()

# ORM
app.state.database = models.database


class Material(BaseModel):
    price: int
    image: bytes
    count: int
    type: str
    suppliers: List[str]


@app.get('/migrations')
async def migrate():
    models.metadata.create_all(models.engine)


@app.get('/image/{image_name}')
def get_file(image_name):
    try:
        return FileResponse(path=f'materials/{image_name}')
    except:
        return FileResponse(path=f'materials/picture.png')


@app.get('/material/insert')
async def insert_material():
    model = await models.MaterialType.objects.create(name="test")
    return model


@app.get('/material/import')
async def import_all():
    await models.import_materials()
    await models.import_suppliers()
    # await models.import_suppliers_material()

    return "Import - ok"


@app.get('/material')
async def list_materials():
    """ Получение списка материала"""

    return await models.Material.objects.select_all().all()



@app.get('/suppliers')
async def list_suppliers():
    """ Получение списка поставщиков """

    return await models.MaterialSupplier.objects.all()


# ORM quit
@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
