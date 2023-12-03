from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Time, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import mysql

Base = declarative_base()

class BaseInformation(Base):
    __tablename__ = 'base_information'
    user_id = Column(Integer, primary_key=True)
    user_uuid = Column(String(36))
    eng_ielts = Column(Float)
    eng_toelf = Column(Integer)
    score_gpa = Column(Float)
    target_country = Column(String(255, collation='utf8mb4_unicode_ci'))
    target_university = Column(String(255, collation='utf8mb4_unicode_ci'))
    target_major = Column(String(255, collation='utf8mb4_unicode_ci'))
    target_job = Column(String(255, collation='utf8mb4_unicode_ci'))
    budget = Column(String(255, collation='utf8mb4_unicode_ci'))

def create_database(server, username, password, dbname):
    connection = mysql.connector.connect(
        host = server,
        user = username,
        password = password,
    )
    cursor = connection.cursor()
    cursor.execute(f"Create Database {dbname}")
    cursor.close()
    connection.close()