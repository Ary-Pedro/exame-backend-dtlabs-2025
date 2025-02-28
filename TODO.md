# 🏆 Impact

- Desenvolvimento de APIs.
- Desenvolvimento de testes.
- Lógica de programação.
- Engenharia de Software.

---

# 🚀 Steps

### **Formato de Entrega**

1. Crie uma conta no GitHub, caso você não tenha.
2. Crie um repositório chamado `exame-backend-dtlabs-2025`. O repositório deve ser **público**.
3. Desenvolva o exame neste repositório, ele será utilizado para avaliação.
4. O `README.md` do repositório deve conter as instruções necessárias para testar a aplicação.
5. Fique à vontade para usar arquivos `Makefile`, por exemplo, para automatizar alguns processos. Use quaisquer outras ferramentas que julgar necessário.
6. Serão avaliados a aplicação, os testes desenvolvidos, padrões de projeto aplicados e se os requisitos foram atendidos.

---

# ⚠️ Note

### **Requisitos**

1. O case deve ser desenvolvido em **Python** utilizando **FastAPI**.

   - ❌ Outras linguagens ou frameworks não serão aceitos.
   - ✅ Bibliotecas adicionais podem ser usadas livremente.

2. O banco de dados deve ser **PostgreSQL**.

   - ❌ Outros bancos não serão aceitos.
   - ✅ Deve ser executado via **Docker**.

3. O repositório do GitHub deve ser **público**.

   - O `README.md` precisa detalhar como executar o projeto.

4. Recomenda-se uso de **Docker** para a aplicação final.

5. **Testes são obrigatórios**.

   - ✅ Deve-se utilizar **PyTest**.
   - ✅ Pode ser criado um `docker-compose.yaml` para subir toda a aplicação.

6. **Nomenclatura** e **comentários** devem estar em **inglês**.

7. Pode-se escolher qualquer ORM ou Query Builder, ou criar queries manualmente.

8. Caso seja chamado para entrevista técnica, será necessário explicar toda a aplicação.

9. Opcionalmente, pode-se utilizar:

   - 📌 **Sistema de Caching** (Redis, MemCached, etc.)
   - 📌 **Serviço de Fila** (RabbitMQ, Kafka, etc.)
   - 📌 **Plugins do PostgreSQL** (TimescaleDB, Pgcrypto, etc.)

10. \*\*RESTFul obrigatório (Case deve ser 100% RESTFul).

- ❌ Não será aceita outra estrutura.
- ✅ Utilize corretamente os verbos HTTP e Headers.

11. As variáveis de ambiente devem estar em um arquivo configurável (`.env`).
12. &#x20;Não se preocupe com migration

---

# 🎯 Value

### **O que será analisado?**

- 📌 **Velocidade** de entrega do teste resolvido.
- 📌 **Qualidade dos testes**.
- 📌 **Estrutura da aplicação**.
- 📌 **Coerência com os requisitos**.
- 📌 **Tratamento de erros** adequado.
- 📌 **Status Codes** bem definidos.
- 📌 **Documentação da API**.
- 📌 **Uso correto de Design Patterns**.
- 📌 **Uso adequado de verbos HTTP e Headers**.
- 📌 **Modelagem eficiente do Banco de Dados**.
- 📌 **Documentação clara do repositório**.

---

---

# CASE
Você irá desenvolver o backend de uma aplicação de IoT. Seu produto consiste em um
servidor que está localizado on-premise no seu cliente. Este servidor coleta dados de
diversos sensores. Os servidores enviam para um único banco de dados. Cada servidor
comporta até 4 (quatro) sensores diferentes:

- Sensor de Temperatura.
  - Valores são medidos em graus celsius.
- Sensor de Umidade.
  - Valores são medidos em %, de 0 a 100.
- Sensor de Tensão Elétrica.
  - Valores são medidos em Volts.
- Sensor de Corrente Elétrica.
  - Valores são medidos em Ampère.

É possível que um servidor tenha um sensor de temperatura e um sensor de umidade.
Portanto, eles enviam os dois valores na mesma requisição. Cada servidor vai possuir
apenas 1 (um) sensor de cada. Logo, não existem servidores que possuem 3 (três)
sensores de temperatura e 1 (um) sensor de corrente elétrica.

Os servidores podem enviar dados com uma frequência de, no mínimo, 1 Hz, e, no
máximo, 10 Hz.

A seguir, serão descritos os endpoints necessários para serem implementados e
descritivo do que eles devem fazer.

## Funcionalidades

### 1️⃣ Autenticação (JWT)
O sistema deve ter um mecanismo de autenticação baseado em JWT para proteger endpoints
privados. Os servidores e usuários autenticados devem utilizar um token para acessar as
funcionalidades restritas.

#### 🔹 Endpoints
- `POST /auth/register` → Criar um novo usuário.
- `POST /auth/login` → Autenticar usuário e retornar um token JWT.

### 2️⃣ Registro de Dados dos Sensores
Os servidores on-premise devem ser capazes de enviar leituras dos sensores para a API.

#### 🔹 Endpoint
- `POST /data`
  - **Não requer autenticação por JWT**.
  - **Payload esperado:**
    ```json
    {
      "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
      "timestamp": "2024-02-19T12:34:56Z",
      "temperature": 25.5,
      "humidity": 60.2,
      "voltage": 220.0,
      "current": 1.5
    }
    ```
  - **Regras:**
    - Pelo menos um valor de sensor deve ser enviado.
    - O `server_ulid` deve existir antes de registrar os dados.
    - O `timestamp` deve estar no formato ISO 8601.

### 3️⃣ Consulta de Dados
O sistema deve permitir a consulta de dados armazenados, filtrando por intervalo de tempo,
servidor e tipo de sensor. Além disso, o usuário pode solicitar dados agregados por minuto,
hora ou dia, onde a agregação é feita calculando a média dos valores dentro do intervalo
especificado.

#### 🔹 Endpoint
- `GET /data`
  - **Query Parameters:**
    - `server_ulid` (opcional) → Filtra por um servidor específico.
    - `start_time` e `end_time` (opcional) → Intervalo de tempo.
    - `sensor_type` (opcional) → Exemplo: `temperature`, `humidity`.
    - `aggregation` (opcional) → Define a granularidade da agregação (`minute`, `hour`, `day`).
  - **Requer autenticação por JWT**.
  - **Resposta esperada:**
    ```json
    [
      { "timestamp": "2024-02-19T12:34:00Z", "temperature": 25.3 },
      { "timestamp": "2024-02-19T12:35:00Z", "temperature": 24.9 }
    ]
    ```
  - **Regras:**
    - Se `aggregation` for informado, retorna a média dos valores dentro do período.
    - Caso contrário, retorna os dados brutos.
    - **Paginação não é necessária**.

### 4️⃣ Monitoramento da Saúde do Servidor
O sistema deve permitir verificar se um servidor está online ou não. Além disso, deve ter um
outro endpoint para listar todos os servidores.

#### 🔹 Endpoints
- `GET /health/{server_id}` → Retorna um status baseado no último dado recebido do servidor.
  - Um servidor é **offline** se não enviar dados há mais de 10 segundos.
  - **Requer autenticação por JWT**.
  - **Resposta esperada:**
    ```json
    {
      "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
      "status": "online",
      "server_name": "Dolly #1"
    }
    ```

- `GET /health/all` → Retorna a lista de todos os servidores cadastrados para aquele usuário.
  - **Requer autenticação por JWT**.
  - **Resposta esperada:**
    ```json
    [
      {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        "status": "online",
        "server_name": "Dolly #1"
      },
      {
        "server_ulid": "01JMG3HQZPWQV0MN8GBSM9QDHZ",
        "status": "offline",
        "server_name": "Dolly #2"
      }
    ]
    ```

### 5️⃣ Registro de Servidores
Os servidores on-premise devem ser capazes de enviar leituras dos sensores para a API.

#### 🔹 Endpoint
- `POST /servers`
  - **Requer autenticação por JWT**.
  - **Payload esperado:**
    ```json
    {
      "server_name": "Dolly #1"
    }
    ```
  - **Regras:**
    - A criação do `ULID` do servidor deve ser feita pelo backend.



