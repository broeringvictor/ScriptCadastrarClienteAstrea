import pymysql
from dotenv import load_dotenv
import os
from Data import ConnectionMySql

# Carregar variáveis do arquivo .env
load_dotenv()

def create_clientes_pf_table():
    """
    Cria a tabela 'ClientesPF' no banco de dados configurado na conexão.
    """

    # Script SQL para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ClientesPF (
        Id INT AUTO_INCREMENT PRIMARY KEY, -- ID único para cada contato
        ContactName VARCHAR(255) NOT NULL, -- Nome completo
        ContactNickname VARCHAR(255), -- Apelido
        Phone VARCHAR(20), -- Telefone

        Email VARCHAR(255), -- Email
        Website VARCHAR(255), -- Website

        ZipCode VARCHAR(10), -- CEP
        Street VARCHAR(255), -- Rua
        Number VARCHAR(10), -- Número
        Neighborhood VARCHAR(255), -- Bairro
        Complement VARCHAR(255), -- Complemento
        City VARCHAR(255), -- Cidade
        State VARCHAR(2), -- Estado (UF)
        Country VARCHAR(255), -- País

        Job VARCHAR(255), -- Profissão
        Company VARCHAR(255), -- Empresa
        MaritalStatus VARCHAR(50), -- Estado civil
        BirthDate DATE, -- Data de nascimento
        Homeland VARCHAR(255), -- Naturalidade

        CPF VARCHAR(14) UNIQUE, -- CPF (formato 123.456.789-10)
        RG VARCHAR(20), -- RG
        CTPS VARCHAR(20), -- CTPS (Carteira de trabalho)
        BenefitDocument VARCHAR(20), -- Documento de benefício
        VoterDocument VARCHAR(20), -- Título de eleitor
        DriverLicense VARCHAR(20), -- Carteira de habilitação
        Passport VARCHAR(20), -- Passaporte

        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação do registro
        UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Data de atualização do registro
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """

    try:
        # Conectar ao banco de dados
        connection = ConnectionMySql.get_mysql_connection()

        print("Conexão com o banco de dados bem-sucedida!")

        # Executar o comando para criar a tabela
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Tabela 'ClientesPF' criada com sucesso!")

        # Fechar a conexão
        connection.close()
        print("Conexão fechada.")

    except pymysql.MySQLError as e:
        print(f"Erro ao criar a tabela: {e}")


# Executar a função
if __name__ == "__main__":
    create_clientes_pf_table()
