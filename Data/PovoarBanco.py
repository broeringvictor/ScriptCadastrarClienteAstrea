import pymysql
import Data.ConnectionMySql as MySql


def povoar_banco():
    """
    Povoa a tabela 'ClientesPF' com 10 registros fictícios.
    """

    # Dados fictícios para inserção
    dados = [
        ("João Silva", "João", "48991668808", "joao.silva@email.com", "www.joaosilva.com",
         "12345-678", "Rua das Flores", "123", "Centro", "Apto 45", "São Paulo", "SP", "Brasil",
         "Analista de Sistemas", "TechCorp", "Solteiro", "1990-06-15", "Brasil",
         "123.456.789-10", "123456789", "12345678", "345678910", "123456789123", "AB123456", "AB12345678"),
        ("Maria Oliveira", "Maria", "48991778899", "maria.oliveira@email.com", "www.mariaoliveira.com",
         "54321-987", "Avenida Central", "456", "Jardim América", "Casa 2", "Rio de Janeiro", "RJ", "Brasil",
         "Engenheira", "BuildTech", "Casada", "1985-02-20", "Brasil",
         "987.654.321-00", "987654321", "87654321", "123456789", "987654321123", "CD987654", "CD98765432"),
        ("Carlos Souza", "Carlão", "48991554433", "carlos.souza@email.com", "www.carlossouza.com",
         "11223-445", "Rua das Palmeiras", "789", "Vila Nova", "Bloco 3, Ap. 12", "Curitiba", "PR", "Brasil",
         "Advogado", "LegalTech", "Divorciado", "1978-11-30", "Brasil",
         "111.222.333-44", "111222333", "22334455", "123456788", "223344556677", "EF123456", "EF12345678"),
        ("Ana Lima", "Aninha", "48991442211", "ana.lima@email.com", "www.analima.com",
         "33445-667", "Rua do Sol", "321", "Centro Histórico", "Apto 101", "Florianópolis", "SC", "Brasil",
         "Designer", "CreativeLab", "Solteira", "1993-07-15", "Brasil",
         "222.333.444-55", "222333444", "33445566", "123456787", "334455667788", "GH987654", "GH98765432"),
        ("Pedro Almeida", "Pedrinho", "48991330022", "pedro.almeida@email.com", "www.pedroalmeida.com",
         "55667-889", "Rua da Paz", "654", "Bela Vista", "Casa", "Porto Alegre", "RS", "Brasil",
         "Professor", "EduTech", "Casado", "1980-03-25", "Brasil",
         "333.444.555-66", "333444555", "44556677", "123456786", "445566778899", "IJ123456", "IJ12345678"),
        ("Beatriz Santos", "Bia", "48991221133", "beatriz.santos@email.com", "www.beatrizsantos.com",
         "66778-990", "Rua do Campo", "987", "Jardim Botânico", "Bloco 1, Ap. 303", "Belo Horizonte", "MG", "Brasil",
         "Arquiteta", "ArqDesign", "Solteira", "1995-05-10", "Brasil",
         "444.555.666-77", "444555666", "55667788", "123456785", "556677889900", "KL987654", "KL98765432"),
        ("Lucas Martins", "Luquinha", "48991110044", "lucas.martins@email.com", "www.lucasmartins.com",
         "77889-001", "Rua do Mar", "111", "Praia Grande", "Casa", "Salvador", "BA", "Brasil",
         "Médico", "HealthCare", "Casado", "1988-09-05", "Brasil",
         "555.666.777-88", "555666777", "66778899", "123456784", "667788990011", "MN123456", "MN12345678"),
        ("Julia Ferreira", "Juju", "48991009955", "julia.ferreira@email.com", "www.juliaferreira.com",
         "88990-112", "Rua da Serra", "222", "Alto da Glória", "Bloco 2, Ap. 502", "Brasília", "DF", "Brasil",
         "Psicóloga", "MindCare", "Casada", "1992-12-01", "Brasil",
         "666.777.888-99", "666777888", "77889900", "123456783", "778899001122", "OP987654", "OP98765432"),
        ("Fernando Costa", "Nando", "48990998866", "fernando.costa@email.com", "www.fernandocosta.com",
         "99001-223", "Rua do Vento", "333", "Centro", "Sala 5", "Fortaleza", "CE", "Brasil",
         "Empresário", "BizSolutions", "Casado", "1975-08-18", "Brasil",
         "777.888.999-00", "777888999", "88990011", "123456782", "889900112233", "QR123456", "QR12345678"),
        ("Camila Rodrigues", "Cami", "48990887722", "camila.rodrigues@email.com", "www.camilarodrigues.com",
         "11223-334", "Rua das Árvores", "444", "Jardim Primavera", "Bloco 4, Ap. 601", "Recife", "PE", "Brasil",
         "Engenheira Civil", "BuildGroup", "Solteira", "1998-01-20", "Brasil",
         "888.999.000-11", "888999000", "99001122", "123456781", "990011223344", "ST987654", "ST98765432")
    ]

    # Script SQL para inserção
    insert_query = """
    INSERT INTO ClientesPF (
        ContactName, ContactNickname, Phone, Email, Website, ZipCode, Street, Number,
        Neighborhood, Complement, City, State, Country, Job, Company, MaritalStatus,
        BirthDate, Homeland, CPF, RG, CTPS, BenefitDocument, VoterDocument, DriverLicense, Passport
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    connection = None
    try:
        # Conectar ao banco de dados
        connection = MySql.get_mysql_connection()

        with connection.cursor() as cursor:
            # Inserir todos os dados
            cursor.executemany(insert_query, dados)
            connection.commit()
            print("Tabela 'ClientesPF' populada com sucesso!")

    except pymysql.MySQLError as e:
        print(f"Erro ao povoar o banco de dados: {e}")

    finally:
        # Fechar a conexão caso tenha sido aberta
        if connection:
            connection.close()
            print("Conexão com o banco de dados fechada.")


# Executar a função
if __name__ == "__main__":
    povoar_banco()