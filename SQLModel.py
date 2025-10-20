from sqlalchemy import Column, String, Integer, Enum as SQLEnum, Text, DECIMAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

# 基类，所有模型继承它
Base = declarative_base()

class identityENUM(str, Enum):
    teacher = 'teacher'
    parent = 'parent'

class statusENUM(str, Enum):
    active = 'active'
    inactive = 'inactive'
    banned = 'banned'

# 用户表模型（映射数据库中的users表）
class User(Base):
    __tablename__ = "users"  # 数据库表名
    id = Column(Integer, primary_key=True, index=True)  # 主键
    phone = Column(String(20), unique=True, index=True, nullable=False)  # 手机号（唯一索引）
    nickname = Column(String(50), nullable=False)
    identity = Column(SQLEnum(identityENUM), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    status = Column(SQLEnum(statusENUM), default=statusENUM.active)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# 老师信息表模型
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    subject = Column(String(100), nullable=False)
    education = Column(String(50), nullable=True)
    experience = Column(Text, nullable=True)
    introduction = Column(Text, nullable=True)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    rating = Column(DECIMAL(3, 2), default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# 家长信息表模型
class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    child_grade = Column(String(50), nullable=True)
    needs = Column(Text, nullable=True)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())