from fastapi import FastAPI
from app.database import Base, engine
from app.routers import books

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(books.router)


@app.get("/")
def root():
    return {"message": "Welcome to Book Management API "}
