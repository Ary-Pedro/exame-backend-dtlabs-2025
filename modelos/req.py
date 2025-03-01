
import requests
'''
url = "http://localhost:8000/login"
payload = {
    "username": "test",
    "password": "test"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
'''

# test_api.py
# test_api.py
import requests

# Configurações
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_health_check():
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        health_data = response.json()
        
        print("\n=== Relatório de Saúde do Sistema ===")
        print(f"Status Geral: {health_data.get('status', 'unknown')}")
        
        if health_data.get("database") == "connected":
            print("✅ Banco de Dados: Conectado")
            db_info = health_data.get("database_info", {})
            print(f"🔍 Detalhes do PostgreSQL:")
            print(f"   Versão: {db_info.get('version', 'N/A')}")
            print(f"   Banco: {db_info.get('database_name', 'N/A')}")
            print(f"   Usuário: {db_info.get('current_user', 'N/A')}")
            print(f"   Conexões Ativas: {db_info.get('active_connections', 'N/A')}")
        else:
            print("❌ Banco de Dados: Desconectado")
            print(f"Erro: {health_data.get('detail', 'Detalhes não disponíveis')}")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ Erro HTTP {http_err.response.status_code}:")
        print(http_err.response.json())
    except Exception as e:
        print(f"\n🚨 Erro inesperado: {str(e)}")

def test_register(username: str, password: str):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 201:
            print("\n✅ Registro bem-sucedido!")
            print(response.json())
        else:
            print(f"\n❌ Erro no registro (Código {response.status_code}):")
            print(response.json())
    except Exception as e:
        print(f"\n🚨 Erro na requisição de registro: {str(e)}")

def test_login(username: str, password: str):
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 200:
            print("\n✅ Login bem-sucedido!")
            print("Token JWT:", response.json()["access_token"])
        else:
            print(f"\n❌ Erro no login (Código {response.status_code}):")
            print(response.json())
    except Exception as e:
        print(f"\n🚨 Erro na requisição de login: {str(e)}")

if __name__ == "__main__":
    print("=== Testando Health Check ===")
    test_health_check()
    
    # Dados de teste
    test_user = "AAA"
    test_password = "NNNN"
    
    print("\n=== Testando registro ===")
    test_register(test_user, test_password)
    
    print("\n=== Testando login ===")
    test_login(test_user, test_password)