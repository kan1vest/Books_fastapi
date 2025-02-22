from datetime import datetime
from typing import Annotated, Optional

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLoginSсhema(BaseModel):
   username: str
   email: EmailStr = Field(pattern=r".+@*\.com$")
   password: str


class UserAuthSсhema(BaseModel):
   email: EmailStr = Field('Nik@example.com', pattern=r".+@*\.com$")
   password: str = Field('ADMIN')


#CRUD для книг
class BooksSсhema(BaseModel):
   bookname: str
   authors: str
   description: str
   Genre: str
   quantity: int


class BooksFilterSсhema(BaseModel):
    booknames: Optional[str] = Field('book_1,book_2', pattern=r"^\S*$")
    authors: Optional[str] = Field('author_1,author_2', pattern=r"^\S*$")
    genres: Optional[str] = Field('Genre_1,Genre_2', pattern=r"^\S*$")

class BooksUpdateSсhema(BaseModel):
   bookname: Optional[str] = Field('book_1', pattern=r"^\S*$")
   author: Optional[str] = Field('author_1', pattern=r"^\S*$")
   description: Optional[str] = Field(None)
   Genre: Optional[str] = Field(None)
   quantity: Optional[int] = Field(None)

class BooksDeleteSсhema(BaseModel):
   bookname: Optional[str] = Field('book_1', pattern=r"^\S*$")
   author: Optional[str] = Field('author_1', pattern=r"^\S*$")

