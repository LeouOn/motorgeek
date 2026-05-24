import os
import yaml
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


_engine = None
_SessionLocal = None


def get_db_path() -> Path:
    env_path = os.environ.get("MOTORGEEK_DB_PATH")
    if env_path:
        return Path(env_path)
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Path(config.get("database", {}).get("path", "data/motorgeek.db"))
    return Path("data/motorgeek.db")


def get_engine():
    global _engine
    if _engine is None:
        db_path = get_db_path()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(f"sqlite:///{db_path}", echo=False)
    return _engine


def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal()


def init_db():
    from motorgeek.core.models import Base
    engine = get_engine()
    Base.metadata.create_all(engine)