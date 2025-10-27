from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Book(Base):
    __tablename__='books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False )
    author = Column(String(200), nullable=False)
    genre = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)



