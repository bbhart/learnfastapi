from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(None, title='id is not required')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Famous author',
                'description': 'Excellent book',
                'rating': 3,
            }
        }
    

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
@app.get("/books/")
async def get_books_by_rating(rating: int):
    results = []
    for book in BOOKS:
        if book.rating == rating:
            results.append(book)

    return results

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
