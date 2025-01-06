import os

import pymysql
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()


def get_mysql_connection():
    """
    Estabelece uma conexão com o banco de dados MySQL usando as variáveis de ambiente do arquivo .env.

    Retorna:
        connection (pymysql.connections.Connection): Objeto de conexão com o MySQL.
    Lança:
        pymysql.MySQLError: Em caso de erro na conexão.
    """
    try:
        # Configurações de conexão usando variáveis de ambiente
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        port = int(os.getenv("DB_PORT", 3306))  # Define um valor padrão caso a variável não exista

        # Conectar ao MySQL
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        print("Conexão bem-sucedida!")
        return connection

    except pymysql.MySQLError as e:
        print(f"Erro na conexão: {e}")
        raise


# Exemplo de uso da função
if __name__ == "__main__":
    try:
        conn = get_mysql_connection()
        # Faça algo com a conexão, como executar consultas
        conn.close()
        print("Conexão fechada.")
    except Exception as e:
        print(f"Erro ao usar a conexão: {e}")
