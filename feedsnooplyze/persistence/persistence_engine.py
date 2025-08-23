from sqlalchemy.engine import Engine
from .persistence_registry import ENGINE_BUILDERS

PersistenceEngineIcon = {
    "DUCKDB": "🦆",
    "SQLITE": "📁",
    "POSTGRESQL": "🐘",
    "MSSQLSERVER": "🛢️",
    "MYSQL": "🐬"
}


_ENGINE_CACHE = {}

def _get_cached_engine(config) -> Engine:
    db_type = config.persistence.lower()
    key = (db_type, tuple(sorted(config.__dict__.items())))
    
    if key in _ENGINE_CACHE:
        return _ENGINE_CACHE[key]
    
    builder = ENGINE_BUILDERS.get(db_type)
    if not builder:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    engine = builder(config)
    _ENGINE_CACHE[key] = engine
    return engine



def get_engine(config: dict):
    db_type = config.persistence.lower()
    builder = ENGINE_BUILDERS.get(db_type)
    if not builder:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return _get_cached_engine(config)