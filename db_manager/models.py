from sqlalchemy import create_engine, Column,Integer,String,Numeric,ForeignKey,DECIMAL,DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class users(Base) :
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),unique=True, nullable=False)
    password = Column(String(255),nullable=False)
    counter_point = Column(Integer,default=0)
class words(Base) :
    __tablename__ = "words"
    word_id = Column(Integer,primary_key=True,autoincrement=True)
    words_english = Column(String(255),nullable=False)
    words_russian = Column(String(255),nullable=False)
class cities_words(Base) :
    __tablename__ = "cities_words"
    word_id = Column(Integer,primary_key=True,autoincrement=True)
    words_english = Column(String(255),nullable=False)
    words_russian = Column(String(255),nullable=False)
class user_words(Base) :
    __tablename__ = "user_words"
    user_id = Column(Integer,ForeignKey('users.user_id',ondelete="CASCADE"),primary_key=True,nullable=False)
    word_id = Column(Integer,ForeignKey('words.word_id',ondelete="CASCADE"),primary_key=True,nullable=False)
    status = Column(String(50),nullable=False)
class learning_stats(Base) :
    from sqlalchemy import func
    __tablename__ = "learning_stats"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    word_id = Column(Integer,ForeignKey("words.word_id",ondelete="CASCADE"),nullable=False)
    correct_answers = Column(Integer,default=0,nullable=False)
    total_attempts = Column(Integer,default=0,nullable=False)
    last_reviewed = Column(DateTime,default=func.now(),onupdate=func.now())
class ip_save(Base) :
    from sqlalchemy import func
    __tablename__ = "ip_save"
    id = Column(Integer,primary_key=True,autoincrement=True)
    ip = Column(String(20),nullable=True)
    city = Column(String(255),nullable=True)
    login_at = Column(DateTime,default=func.now(),nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
class api_points(Base) :
    __tablename__ = "api_points"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name_simulator = Column(String(255),nullable=False)
    points = Column(Integer,default=0,nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)