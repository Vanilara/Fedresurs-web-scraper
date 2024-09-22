from database import DB


for schema in DB.get_all_schemas():
    schema.remake_schema()