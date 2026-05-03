from sqlalchemy import Integer,DateTime
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class BaseModel(Base):
        __abstract__ = True
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        created_at: Mapped[str] = mapped_column(DateTime,default=datetime.datetime.utcnow, nullable=False)
        updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)