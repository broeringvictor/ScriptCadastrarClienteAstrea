import pymysql
import Data.ConnectionMySql as MySql
from Entities.ClientePF import ClientePF  # Importa a classe do cliente


class BuscarClientesPF:
    """
    Classe para buscar dados da tabela 'ClientesPF' no banco de dados.
    """

    @staticmethod
    def obter_ultimos_clientes():
        """
        Retorna os dados dos 10 últimos clientes cadastrados na tabela 'ClientesPF' como objetos do tipo ClientePessoaFisica.

        Retorno:
            list: Lista de objetos ClientePessoaFisica contendo os dados dos clientes.
        """
        query = """
        SELECT * 
        FROM ClientesPF
        ORDER BY CreatedAt DESC
        LIMIT 10;
        """

        try:
            # Conectar ao banco de dados
            connection = MySql.get_mysql_connection()

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()

            connection.close()

            # Converte cada resultado em um objeto ClientePessoaFisica
            clientes = [
                ClientePF(
                    id=cliente["Id"],
                    contact_name=cliente["ContactName"],
                    contact_nickname=cliente["ContactNickname"],
                    phone=cliente["Phone"],
                    email=cliente["Email"],
                    website=cliente["Website"],
                    zip_code=cliente["ZipCode"],
                    street=cliente["Street"],
                    number=cliente["Number"],
                    neighborhood=cliente["Neighborhood"],
                    complement=cliente["Complement"],
                    city=cliente["City"],
                    state=cliente["State"],
                    country=cliente["Country"],
                    job=cliente["Job"],
                    company=cliente["Company"],
                    marital_status=cliente["MaritalStatus"],
                    birth_date=cliente["BirthDate"],  # Data no formato recebido
                    homeland=cliente["Homeland"],
                    cpf=cliente["CPF"],
                    rg=cliente["RG"],
                    ctps=cliente["CTPS"],
                    benefit_document=cliente["BenefitDocument"],
                    voter_document=cliente["VoterDocument"],
                    driver_license=cliente["DriverLicense"],
                    passport=cliente["Passport"],
                )
                for cliente in resultados
            ]

            return clientes

        except pymysql.MySQLError as e:
            print(f"Erro ao consultar os clientes: {e}")
            return []

    @staticmethod
    def selecionar_cliente():
        """
        Permite ao usuário selecionar um cliente a partir da lista dos 10 últimos cadastrados.

        Retorno:
            ClientePessoaFisica: O cliente selecionado pelo usuário.
        """
        # Obter os últimos 10 clientes
        clientes = BuscarClientesPF.obter_ultimos_clientes()

        if not clientes:
            print("Nenhum cliente encontrado.")
            return None

        # Exibir a lista de clientes com numeração
        print("\nSelecione um cliente:\n")
        for idx, cliente in enumerate(clientes, start=1):
            print(f"{idx}. {cliente}")  # Exibe a posição e a representação do cliente

        while True:
            try:
                # Solicitar que o usuário selecione um cliente
                opcao = int(input("\nDigite o número do cliente desejado: "))

                if 1 <= opcao <= len(clientes):
                    return clientes[opcao - 1]  # Retorna o cliente selecionado
                else:
                    print(f"Por favor, escolha um número entre 1 e {len(clientes)}.")
            except ValueError:
                print("Entrada inválida. Por favor, digite apenas o número correspondente ao cliente.")


# Exemplo de uso da classe
if __name__ == "__main__":
    cliente_selecionado = BuscarClientesPF.selecionar_cliente()

    if cliente_selecionado:
        print("\nCliente selecionado:")
        print(cliente_selecionado)  # Exibe os detalhes do cliente usando o método __str__ da classe ClientePessoaFisica