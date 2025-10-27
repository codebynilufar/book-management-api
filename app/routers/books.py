from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/books", tags=["Books"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books



@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book



@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, updated: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in updated.dict().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.get("/search/", response_model=list[schemas.BookResponse])
def search_books(search: str = Query(..., description="Search by title or author"), db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(
        (models.Book.title.ilike(f"%{search}%")) | (models.Book.author.ilike(f"%{search}%"))
    ).all()
    return books


@router.get("/filter/", response_model=list[schemas.BookResponse])
def filter_books(
    min: int = Query(..., description="Minimum year"),
    max: int = Query(..., description="Maximum year"),
    db: Session = Depends(get_db),
):
    books = db.query(models.Book).filter(models.Book.year.between(min, max)).all()
    return books
