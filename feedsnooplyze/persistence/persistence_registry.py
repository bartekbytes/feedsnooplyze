from sqlalchemy import create_engine

ENGINE_BUILDERS = {}

#TODO: use decorator to register engines
#def register_engine(db_type):
#    def decorator(builder):
#        ENGINE_BUILDERS[db_type] = builder
#        return builder
#    return decorator


#@register_engine('duckdb')
def build_duckdb_engine(config):
    return create_engine(f'duckdb:///{config.db_file_path}')


#@register_engine('sqlite')
def build_sqlite_engine(config):
    return create_engine(f'sqlite:///{config.db_file_path}')


#@register_engine('postgresql')
def build_postgresql_engine(config):
    user = config.user
    password = config.password
    host = config.host
    port = config.port
    database = config.database
    return create_engine(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}')


#@register_engine('mysql')
def build_mysql_engine(config):   
    user = config.user
    password = config.password
    host = config.host
    port = config.port
    database = config.database
    return create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

#@register_engine('mssqlserver')
def build_mssqlserver_engine(config):   
    user = config.user
    password = config.password
    host = config.host
    port = config.port
    database = config.database
    return create_engine(f'mssql+pymssql://{user}:{password}@{host}:{port}/{database}')

#@register_engine('oracle')
def build_oracle_engine(config):   
    user = config.user
    password = config.password
    host = config.host
    port = config.port
    service_name = config.service_name
    return create_engine(f'oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service_name}')


ENGINE_BUILDERS = {
    "duckdb": build_duckdb_engine,
    "sqlite": build_sqlite_engine,
    "postgresql": build_postgresql_engine,
    "mysql": build_mysql_engine,
    "mssqlserver": build_mssqlserver_engine,
    "oracle": build_oracle_engine,
}