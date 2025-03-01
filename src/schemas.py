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
   bookname: str = Field('book_1', pattern=r"^\S*$")
   author: str = Field('author_1', pattern=r"^\S*$")
   description: Optional[str] = Field(None)
   Genre: Optional[str] = Field(None)
   quantity: Optional[int] = Field(None)

class BooksDeleteSсhema(BaseModel):
   bookname: Optional[str] = Field('book_1', pattern=r"^\S*$")
   author: Optional[str] = Field('author_1', pattern=r"^\S*$")



class AuthorSсhema(BaseModel):
   authorname: str
   biography: str
   date_of_born: str

class AuthorFilterSсhema(BaseModel):
   authorname: str = Field('author_1', pattern=r"^\S*$")


""" class AuthorUpdateSсhema(BaseModel):
   authorname: str = Field('book_1', pattern=r"^\S*$")
   biography: Optional[str] = Field('author_1', pattern=r"^\S*$")
   date_of_born: Optional[str] = Field(None) """




