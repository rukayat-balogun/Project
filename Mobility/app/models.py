from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    age = Column(Integer)
    date_of_birth = Column(Date)

    def __repr__(self):
        return f"<User(firstname='{self.firstname}', lastname='{self.lastname}', age='{self.age}', date_of_birth='{self.date_of_birth}')>"
