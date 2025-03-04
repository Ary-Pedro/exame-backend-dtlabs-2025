import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
from typing import Generator, Optional

load_dotenv()

DATABASE_NAME = "api_server"
DEFAULT_DB = "postgres"
REQUIRED_ENV_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal: Optional[sessionmaker] = None
        self.is_initialized = False

    def validate_env_vars(self) -> bool:
        missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing:
            print(f"\n[ERRO] Variáveis ausentes: {', '.join(missing)}", file=sys.stderr)
            return False
        return True

    def get_db_url(self, db_name: str) -> str:
        return (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{db_name}"
        )

    def test_connection(self, db_url: str) -> bool:
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            print(f"\n[ERRO] Falha na conexão: {e}")
            return False

    def create_database(self) -> bool:
        default_url = self.get_db_url(DEFAULT_DB)
        if not self.test_connection(default_url):
            return False

        try:
            engine = create_engine(default_url, isolation_level="AUTOCOMMIT")
            with engine.connect() as conn:
                exists = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                    {"dbname": DATABASE_NAME}
                ).scalar()
                
                if not exists:
                    conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
                    print(f"\nBanco '{DATABASE_NAME}' criado.")
            return True
        except SQLAlchemyError as e:
            print(f"\n[ERRO] Criação do banco falhou: {e}")
            return False

    def initialize(self) -> None:
        if not self.validate_env_vars():
            sys.exit(1)

        if not self.create_database():
            print("\n[AVISO] Banco não foi criado.")
            return

        main_db_url = self.get_db_url(DATABASE_NAME)
        if not self.test_connection(main_db_url):
            print("\n[ERRO] Conexão com o banco principal falhou.")
            return

        try:
            self.engine = create_engine(main_db_url)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            SQLModel.metadata.create_all(self.engine)  # Cria todas as tabelas
            self.is_initialized = True
            print("\nBanco inicializado com sucesso.")
        except SQLAlchemyError as e:
            print(f"\n[ERRO] Inicialização falhou: {e}")

    def get_session(self) -> Generator:
        if not self.is_initialized or not self.SessionLocal:
            raise RuntimeError("Banco não inicializado.")
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseManager()

def init_database():
    db_manager.initialize()