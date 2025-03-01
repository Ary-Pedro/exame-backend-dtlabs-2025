import os
import psycopg2
from psycopg2 import sql

def get_db_connection(db_name):
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        database=db_name,
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "82001728")
    )

def create_database_if_not_exists(db_name):
    try:
        connection = get_db_connection("postgres")
        connection.autocommit = True
        cursor = connection.cursor()
        
        cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), [db_name])
        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"Banco de dados '{db_name}' já existe.")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Erro ao verificar/criar o banco de dados: {error}")

def connect_to_postgres():
    try:
        create_database_if_not_exists("API_SERVER")
        
        connection = get_db_connection("API_SERVER")
        cursor = connection.cursor()        
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")

def list_columns_and_fields(db_name):
    try:
        connection = get_db_connection(db_name)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        for table_name, column_name, data_type in columns:
            print(f"Tabela: {table_name}, Coluna: {column_name}, Tipo: {data_type}")
        
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Erro ao listar colunas e campos: {error}")

def list_table_data(db_name):
    try:
        connection = get_db_connection(db_name)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            print(f"\nDados da Tabela: {table_name}")
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Erro ao listar dados das tabelas: {error}")

if __name__ == "__main__":
    connect_to_postgres()
    list_columns_and_fields("API_SERVER")
    list_table_data("API_SERVER")