import email
from operator import contains
import re
from unittest import result
from fastapi import HTTPException
from sqlalchemy import Integer, True_, and_, cast, delete, func, insert, inspect, or_, select, text, true, tuple_
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import Base, async_engine, async_session_factory, session_factory, sync_engine
from models import UsersOrm, BooksOrm, AuthorOrm

from passlib.context import CryptContext
from sqlalchemy.sql._elements_constructors import true


# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class AsyncORM:
    
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all) 

    @staticmethod
    async def insert_users(username, email, password):
        async with async_session_factory() as session:
            user = UsersOrm(username=username, email=email, hashed_password=get_password_hash(password))
            session.add_all([user])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()
      

    @staticmethod
    async def select_users_registration(email: str, password):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email)
                .filter_by(email=email)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.first()
            return result
        

    @staticmethod
    async def select_users_auth(email: str, password):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email, UsersOrm.hashed_password)
                .filter_by(email=email)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.first()
            if result:
                return result
            else:
                raise HTTPException(status_code=401, detail=f"Пользователь с email {email} не зарегистрирован")
    
    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(UsersOrm.username, UsersOrm.email)
            result = await session.execute(query)
            res = dict(result.all())
            return res

    # CRUD для книг  ############################################################
    @staticmethod
    async def insert_books():
        async with async_session_factory() as session:
            book_1 = BooksOrm(bookname='book_1', author='author_1', description='description_1', Genre='Genre_1', quantity=1)
            book_2 = BooksOrm(bookname='book_2', author='author_1', description='description_2', Genre='Genre_1', quantity=2)
            book_3 = BooksOrm(bookname='book_3', author='author_2', description='description_3', Genre='Genre_2', quantity=3)
            book_4 = BooksOrm(bookname='book_4', author='author_3', description='description_4', Genre='Genre_3', quantity=4)
            session.add_all([book_1, book_2, book_3, book_4])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush() 
            await session.commit()

    @staticmethod
    async def create_books(bookname, authors, description, Genre, quantity):
        async with async_session_factory() as session:
            book = BooksOrm(bookname=bookname, authors=authors, description=description, Genre=Genre, quantity=quantity)
            session.add(book)
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush() 
            await session.commit()

    @staticmethod
    async def select_books(books_filter):
        if books_filter.booknames:
            books = BooksOrm.bookname.in_(books_filter.booknames.split(','))
        else:
            books = true()
        if books_filter.authors:
            authors = BooksOrm.author.in_(books_filter.authors.split(','))
        else:
            authors = true()
        if books_filter.genres:
            genres = BooksOrm.Genre.in_(books_filter.genres.split(','))
        else:
            genres = true()
        async with async_session_factory() as session:
            query = (
                select(BooksOrm)
                .where(
                    and_(
                        books, authors, genres
                        )
                )
            )
            res = await session.execute(query)
            result = res.scalars().all()
            return result

    @staticmethod
    async def update_book(updates):
        async with async_session_factory() as session:
            query = (
                select(BooksOrm.id)
                .where(
                    and_(
                    BooksOrm.bookname.in_(updates.bookname.split(',')),
                    BooksOrm.author.in_(updates.author.split(','))
                )
                    )
            )
            res = await session.execute(query)
            upd_id = res.first()
            upd = await session.get(BooksOrm, upd_id[0])
            book = {
                'bookname': upd.bookname, 
                'author': upd.author, 
                'description': upd.description, 
                'Genre': upd.Genre, 
                'quantity': upd.quantity,
            } 
            if updates.description:
                upd.description = updates.description
            if updates.Genre:
                upd.Genre = updates.Genre
            if updates.quantity:
                upd.quantity = updates.quantity
            book_update = {
                'bookname': upd.bookname, 
                'author': upd.author, 
                'description': upd.description, 
                'Genre': upd.Genre, 
                'quantity': upd.quantity,
            }     
            await session.flush()
            await session.commit()
            return {
                'Книга с параметрами': book,
                "Изменена на книгу с параметрами": book_update
            }
                
    @staticmethod
    async def delete_book(delete_data):
        async with async_session_factory() as session:
            query_select = (
                select(BooksOrm)
                .filter(
                    and_(
                    BooksOrm.bookname.contains(delete_data.bookname),
                    BooksOrm.author.contains(delete_data.author) 
                )
                    )
            )
            query_delete = (
                delete(BooksOrm)
                .filter(
                    and_(
                    BooksOrm.bookname.contains(delete_data.bookname),
                    BooksOrm.author.contains(delete_data.author) 
                )
                    )
            )
            res = await session.execute(query_select)
            await session.execute(query_delete)
            result = res.scalars().all()
            await session.commit()
            return {
                'Удалена книга с параметрами':  result
            }         
            

# CRUD авторы ############################################################
    @staticmethod
    async def update_user(user_email, new_username):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.id)
                .filter_by(email=user_email)
            )
            res = await session.execute(query)
            user_id = res.first()
            user = await session.get(UsersOrm, user_id[0])
            user.username = new_username
            await session.flush()
            await session.commit()




