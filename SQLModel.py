from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

# 基类，所有模型继承它
Base = declarative_base()

class identityENUM(str, Enum):
    teacher = 'teacher'
    parent = 'parent'

# 用户表模型（映射数据库中的users表）
class User(Base):
    __tablename__ = "users"  # 数据库表名
    id = Column(Integer, primary_key=True, index=True)  # 主键
    phone = Column(String(20), unique=True, index=True, nullable=False)  # 手机号（唯一索引）
    nickname = Column(String(50), nullable=False)
    identity = Column(SQLEnum(identityENUM), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255),nullable=False)