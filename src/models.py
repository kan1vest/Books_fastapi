import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]



class UsersOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Сохраняем хешированный пароль

class BooksOrm(Base):   # создаем таблицы
    __tablename__ = "books_table" # создаем имя таблицы

    id: Mapped[intpk]
    bookname: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    author: Mapped[str]
    Genre: Mapped[str]
    quantity: Mapped[int]
    """ resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
    ) """
    
class AuthorOrm(Base):   # создаем таблицы
    __tablename__ = "author_table" # создаем имя таблицы

    id: Mapped[intpk]
    authorname: Mapped[str]
    biography: Mapped[str]
    date_of_born: Mapped[str]
"""   resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
    )
 """