from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2012),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2019),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2022),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2019),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2003),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2001)
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(None, title='id is not required')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_year: int = Field(gt=0, lt=3000)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Famous author',
                'description': 'Excellent book',
                'rating': 3,
                'published_year': 2024,
            }
        }
    

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    # We didn't find a book with that ID, so raise exception
    raise HTTPException(status_code=404, detail='Item not found')
        
@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0,lt=6)):
    results = []
    for book in BOOKS:
        if book.rating == rating:
            results.append(book)

    return results

@app.get("/books/published_year/{published_year}", status_code=status.HTTP_200_OK)
async def get_books_by_published_year(published_year: int):
    results = []
    for book in BOOKS:
        if book.published_year == published_year:
            results.append(book)

    return results

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    item_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            item_found = True

    if not item_found:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    item_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            item_found = True
            break

    if not item_found:
        raise HTTPException(status_code=404, detail="Item not found")
