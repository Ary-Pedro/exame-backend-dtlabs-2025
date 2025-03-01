from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import os
from modelos.database import connect_to_postgres
from sqlalchemy.sql import text 

#GARANTIR A EXISTENCIA DO BANCO DE DADOS
connect_to_postgres()

DATABASE_URL = "postgresql://postgres:82001728@localhost:5433/API_SERVER"   #TODO ALTERAR POR . ENV!!!
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo de Usuário
class User(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True)
    hashed_password = Column(String(255))
    #FUTUROS CAMPOS DE VALIDAÇÃO

Base.metadata.create_all(bind=engine)
# Configuração do JWT
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "super-secret-key") #TODO ALTERAR POR . ENV!!!

@AuthJWT.load_config
def get_config():
    return Settings()

# Schemas Pydantic
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Configuração de Hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint de Registro
@app.post("/auth/register", status_code=status.HTTP_201_CREATED)#need a timer for not stress the server
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash da senha
    hashed_password = pwd_context.hash(user.password)
    
    # Cria novo usuário
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    
    return {"message": "User created successfully"}

# Endpoint de Login
@app.post("/auth/login")
async def login(user: UserLogin, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Busca usuário no banco
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # Verifica credenciais
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Gera token JWT
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}

@app.get("/health") #TODO ALTERAR PARA APENAS PARA TESTE,  REMOVER
async def health_check(db: Session = Depends(get_db)):
    try:
        # Testa a conexão e coleta informações do banco
        db.execute(text("SELECT 1"))  # Teste básico de conexão
        
        # Obtém informações detalhadas do PostgreSQL
        result = db.execute(text(
            "SELECT version(), current_database(), current_user, inet_server_addr()"
        ))
        db_info = result.fetchone()

        # Conta conexões ativas
        active_connections = db.execute(
            text("SELECT COUNT(*) FROM pg_stat_activity")
        ).scalar()

        return {
            "status": "OK",
            "database": "connected",
            "database_info": {
                "version": db_info[0],
                "database_name": db_info[1],
                "current_user": db_info[2],
                "server_address": db_info[3],
                "active_connections": active_connections
            }
        }
        
    except Exception as e:
        return {
            "status": "Error",
            "database": "disconnected",
            "detail": str(e)
        }
