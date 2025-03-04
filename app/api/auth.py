from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..core.security import get_password_hash, verify_password, create_access_token
from ..models.model import User, UserBase
from ..models.session import SessionDep

router = APIRouter()

@router.post("/register")
async def register(user: UserBase, db: Session = SessionDep):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Gera token apenas para resposta (não armazena no banco)
    token = create_access_token({"sub": user.name})
    return {"token": token}

@router.post("/login")
async def login(user: UserBase, db: Session = SessionDep):
    db_user = db.query(User).filter(User.name == user.name).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    
    token = create_access_token({"sub": user.name})
    return {"token": token}

@router.get("/health")
async def health_check():
    return {"status": "online"}