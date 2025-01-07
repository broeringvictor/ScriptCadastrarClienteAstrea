import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


class AstreaAdditional:
    def __init__(self, driver):
        """Inicializa com o driver do Selenium e define variáveis para os campos."""
        self.driver = driver


        # Variáveis para valores que serão preenchidos no formulário.
        self.job = ""  # Profissão
        self.company = ""  # Código da atividade econômica
        self.marital_status = ""  # Estado civil
        self.birth_day = ""  # Dia de nascimento
        self.birth_month = ""  # Mês de nascimento
        self.birth_year = ""  # Ano de nascimento
        self.homeland = ""  # Naturalidade

    def set_data_from_client(self, client):
        """Configura os dados do cliente nos atributos do objeto."""
        self.job = client.job
        self.company = client.company  # Corrigido para utilizar `client.company`
        self.marital_status = client.marital_status
        self.homeland = client.homeland

        self.birth_day = client.birth_day
        # Configurar os valores de nascimento
        self.set_birth_date(client.birth_date)
        client.birth_day = self.birth_day
        client.birth_month = self.birth_month
        client.birth_year = self.birth_year


        # Configura a data de nascimento utilizando a função de conversão.

    def set_birth_date(self, birth_date):
        """
        Converte uma data de nascimento do tipo datetime.date ou string no formato yyyy-mm-dd
        para os atributos dia, mês e ano.

        Args:
            birth_date (date or str): Data de nascimento no formato datetime.date ou yyyy-mm-dd.
        """
        try:
            if isinstance(birth_date, date):
                # Caso a entrada já seja um objeto datetime.date
                self.birth_year = str(birth_date.year)
                self.birth_month = str(birth_date.month)  # Sem zero à esquerda
                self.birth_day = str(birth_date.day)  # Sem zero à esquerda
            elif isinstance(birth_date, str):
                # Caso a entrada seja uma string
                year, month, day = birth_date.split("-")
                self.birth_year = year
                self.birth_month = str(int(month))  # Remove zero à esquerda ao converter para int
                self.birth_day = str(int(day))  # Remove zero à esquerda ao converter para int

            print(f"Data de nascimento convertida: Dia={self.birth_day}, Mês={self.birth_month}, Ano={self.birth_year}")
        except Exception as e:
            print(f"Erro ao processar a data de nascimento '{birth_date}': {e}")

    def verificar_e_navegar_para_url(self, extra_delay=5):
        """
        Verifica a URL atual e navega para a URL específica se necessário.
        """
        url_desejada = r"https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/additional"

        try:
            # Recupera a URL atual aberta no navegador
            url_atual = self.driver.current_url
            print(f"URL atual: {url_atual}")

            # Verifica se a URL atual é diferente da URL desejada
            if url_atual != url_desejada:
                print(f"URL diferente da esperada. Navegando para {url_desejada}...")
                self.driver.get(url_desejada)  # Navega até a URL desejada
                print("Navegou para a URL desejada com sucesso.")

                if extra_delay:
                    print(f"Extra delay --> Aguardando {extra_delay} segundos...")
                    time.sleep(extra_delay)
            else:
                print("Já está na URL desejada.")

        except Exception as e:
            print(f"Erro ao verificar ou navegar para a URL: {e}")
            raise  # Lança o erro para depuração em um nível mais alto

    def map_inputs(self):
        """Realiza o mapeamento dos inputs e os associa às variáveis correspondentes."""
        return [
            {"selector": "input#contactJob", "name": "job", "type": "text", "value": self.job},
            {"selector": "#contactCompanyName", "name": "economic_activity_code", "type": "text",
             "value": self.company},
            {"selector": "input#contactMaritalStatus", "name": "marital_status", "type": "text",
             "value": self.marital_status},
            {
                "selector": "//*[@id='mainDiv']/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div/select",
                "name": "birth_day", "type": "select", "value": self.birth_day},
            {
                "selector": "//*[@id='mainDiv']/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div/select",
                "name": "birth_month", "type": "select", "value": self.birth_month},
            {
                "selector": '//*[@id="mainDiv"]/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[3]/div/div/select',
                "name": "birth_year", "type": "select", "value": self.birth_year},
            {"selector": "input#contactHomeland", "name": "homeland", "type": "text", "value": self.homeland}
        ]

    def preencher_formulario(self):
        """Preenche os campos de texto e seleções mapeados."""
        try:
            print("Data de nascimento processada antes de preencher o formulário.")

            print("Aguarde enquanto os campos estão carregando...")


            # Itera pelos campos mapeados no método map_inputs
            for campo in self.map_inputs():
                try:
                    if campo["type"] == "text":
                        # Campos de texto
                        print(f"Preenchendo campo de texto: {campo['name']}")
                        elemento = self.driver.find_element(By.CSS_SELECTOR, campo["selector"])
                        elemento.clear()  # Limpa o campo antes de inserir o valor
                        elemento.send_keys(campo['value'])
                        print(f"Campo '{campo['name']}' preenchido com: {campo['value']}")

                    elif campo["type"] == "select":
                        # Campos de seleção (dropdown)
                        print(f"Selecionando valor no campo: {campo['name']}")
                        elemento = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, campo["selector"]))
                        )
                        select = Select(elemento)
                        try:
                            select.select_by_visible_text(campo['value'])
                        except:
                            select.select_by_index(str(campo['value']))
                        print(f"Campo de seleção '{campo['name']}' preenchido com: {campo['value']}")
                except Exception as e:
                    print(f"Erro ao preencher o campo '{campo['name']}': {e}")

            print("Todos os campos foram preenchidos com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher o formulário: {e}")