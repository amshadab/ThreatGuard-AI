from sqlalchemy import create_engine
from server.config import settings
from server.model import Base, Profile, URLScan
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine, tables=[Profile.__table__, URLScan.__table__])


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
