from typing import Optional, List
import ormar
import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///sqlite.db")
engine = sqlalchemy.create_engine("sqlite:///sqlite.db")


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class MaterialType(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)


class MaterialSupplier(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)


class Material(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    minimal_count: int = ormar.Integer()
    count: int = ormar.Integer()
    image: Optional[str] = ormar.String(max_length=1000, nullable=True, sql_nullable=True)
    price: int = ormar.Integer()
    type: MaterialType = ormar.ForeignKey(MaterialType)
    suppliers: Optional[List[MaterialSupplier]] = ormar.ManyToMany(MaterialSupplier)


async def import_suppliers():
    suppliers_txt = '/home/wale/Рабочий стол/Задание ПМ.01/Сессия 1/supplier_b_import.txt'
    with open(suppliers_txt, 'r') as file:
        data = file.readlines()
        first = True
        for line in data:
            if first:
                first = False
                continue
            line = line.split(',')
            await MaterialSupplier.objects.create(name=line[0])


async def import_materials():
    materials_txt = '/home/wale/Рабочий стол/Задание ПМ.01/Сессия 1/materials_b_import.csv'
    with open(materials_txt, 'r') as file:
        data = file.readlines()
        first = True
        for line in data:
            if first:
                first = False
                continue
            line = line.split(';')
            price = int(line[3].replace(' рублей', '').replace(' руб', '').split('.')[0])
            count = line[4].replace('На складе: ', '')
            count = count.replace(' в наличии', '')
            try:
                image = line[2].split('\\')[2]
            except:
                image = 'None'
            type = await MaterialType.objects.get_or_create(name=line[1])
            await Material.objects.create(title=line[0], type=type, image=image, price=price,
                                          count=count,
                                          minimal_count=int(line[5]))


async def import_suppliers_material():
    material_supplier = '/home/wale/Рабочий стол/Задание ПМ.01/Сессия 1/materialsupplier_b_import.csv'
    with open(material_supplier, 'r') as file:
        data = file.readlines()
        first = True
        for line in data:
            if first:
                first = False
                continue
            line = line.split(',')
            material = await Material.objects.get(title=line[0])
            try:
                supplier = await MaterialSupplier.objects.get(name=line[1].replace('\n', ''))
                await material.suppliers.add(supplier)
                # await material.save()
            except:
                print(line[1])


