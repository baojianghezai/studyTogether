import configparser
from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Depends
from phone_send import Sample_send
from phone_check import Sample_check
import json
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session, sessionmaker
from SQLModel import User, identityENUM
from passlib.context import CryptContext

config = configparser.ConfigParser()
config.read("config.ini")
DB_CONFIG = config["DATABASE"]

# 配置密码上下文：指定使用 bcrypt 算法
pwd_context = CryptContext(
    schemes=["bcrypt"],  # 加密方案（可指定多个，优先使用第一个）
    deprecated="auto"    # 自动处理过时的加密方案
)

# 创建引擎（连接池核心）
engine = create_engine(
    f"mysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
    pool_size=10,  # 连接池默认大小
    max_overflow=20,  # 超出pool_size时允许的临时连接数
    pool_recycle=3600,  # 连接超时时间（秒），避免连接被数据库主动关闭
    pool_pre_ping=True  # 每次从池获取连接时检查有效性，自动重连
)

# 创建会话工厂（用于获取数据库会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 使用示例：从连接池获取连接（会话）
def get_db():
    db = SessionLocal()  # 从连接池取一个连接
    try:
        yield db  # 供业务逻辑使用
    finally:
        db.close()  # 放回连接池（并非真正关闭连接）

@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("数据库连接池初始化成功")
    yield
    # 关闭连接池（释放所有连接）
    engine.dispose()
    print("数据库连接池已关闭")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.post("/api/v1/login")
def login(
    phoneNum: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    hash_passwd = db.query(User.password_hash).filter(User.phone == phoneNum).first()
    if not hash_passwd:
        return {'code':10002, 'msg':'phone number not regist'}
    userInfo = db.query(User.id, User.nickname, User.identity).filter(User.phone == phoneNum).first()
    hash_passwd = hash_passwd[0]
    print(password)
    print(hash_passwd)

    result = pwd_context.verify(password, hash_passwd)
    if result:
        return {
            'code': 0,
            'msg': 'success',
            'id': userInfo.id,
            'nickname': userInfo.nickname,
            'identity': userInfo.identity.value
        }
    else:
        return {'code': 100, 'msg': 'passwd error'}


@app.post("/api/v1/regist/getNum")
def regist_getNum(phoneNum: str = Form(), db: Session = Depends(get_db)):
    #数据库验证，防止已注册的手机号重复注册
    user = db.query(User).filter(User.phone == phoneNum).first()
    if( user is not None ):
        print('user not None')
        return {'code':10001, 'msg':'already registed'}
    else:
        print('user is none')
        Sample_send.main(phoneNum)
        return {'code':0, 'msg':'success'}

@app.post("/api/v1/regist/verityNum")
def regist_vrityNum(
        phoneNum: str = Form(),
        vriCode: str = Form(),
        Nickname: str = Form(),
        Identity: identityENUM = Form(),
        Password: str = Form(),
        Email: str | None = Form(None),
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.phone == phoneNum).first()
    if (user is not None):
        print('user not None')
        return {'code': 10001, 'msg': 'already registed'}

    #阿里云api直接用，返回结果就是data
    data = json.loads(Sample_check.main(phoneNum, vriCode))
    result = data["body"]["Model"]["VerifyResult"]
    if result == "PASS":  #验证码正确
        #密码哈希处理
        hash_passwd = pwd_context.hash(Password)
        # 验证函数pwd_context.verify(明文密码, hashed_password)
        #添加到数据库并返回
        user_db = User(
            phone = phoneNum,
            nickname = Nickname,
            identity = Identity.value,
            password_hash = hash_passwd,
            email = Email
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {'code': 0, 'msg': 'success'}
    elif result == "UNKNOWN":
        return {'code': 101, 'msg': 'varity error'}

# 路由中使用数据库连接
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    # 执行SQL查询
    result = db.execute(text("SELECT 1")).scalar()
    return {"status": "success", "result": result}