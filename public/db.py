from sqlalchemy import create_engine
from models.models import Base
from config import settings

ur_s = settings.POSTGRESS_DATABASE_URLS
ur_a = settings.POSTGRESS_DATABASE_URLA
print(ur_s)

engine_s = create_engine(ur_s, echo=True)


def create_tables():
    Base.metadata.create_all(bind=engine_s)
