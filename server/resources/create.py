from sqlalchemy import create_engine, inspect, event, Table, Boolean, MetaData, Float
from sqlalchemy.ext.automap import automap_base
from copy import deepcopy


def create_db_resources(creds):
    engines = deepcopy(creds)
    tables = deepcopy(creds)
    inspectors = deepcopy(creds)
    engines_created = 0

    for db, data in creds.items():
        engines_created += 1
        print(f'Creating resources for database "{db}"')
        conn_str = "postgresql+psycopg2://{username}:{password}@{hostname}".format(
            **data)
        print(conn_str)
        eng = create_engine(conn_str, echo=False)
        metadata = MetaData()
        metadata.reflect(eng, schema=data['schema'])
        # Base = automap_base()
        # Base.prepare(eng, reflect=True)
        engines[db] = eng
        tables[db] = metadata.tables
        inspectors[db] = inspect(eng)
    if engines_created == 0:
        raise Exception('Not a single database engine created. Check Config attributes "DEBUG_DB_NAME" and "DEBUG_PRODUCT_NAME" when environmental variable "DEBUG_FLAG" is TRUE. Database name or product does not exist')
    return engines, tables, inspectors
