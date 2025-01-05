from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class AstreaAdditional:
    def __init__(self, driver):
        """Inicializa com o driver do Selenium e define variáveis para os campos."""
        self.driver = driver

        # Variáveis para valores que serão preenchidos no formulário
        self.job = ""  # Profissão
        self.economic_activity_code = ""  # Código da atividade econômica
        self.marital_status = ""  # Estado civil
        self.birth_day = ""  # Dia de nascimento
        self.birth_month = ""  # Mês de nascimento
        self.birth_year = ""  # Ano de nascimento
        self.homeland = ""  # Naturalidade

    def verificar_e_navegar_para_url(self):
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
            else:
                print("Já está na URL desejada.")

        except Exception as e:
            print(f"Erro ao verificar ou navegar para a URL: {e}")
            raise  # Lança o erro para depuração em um nível mais alto

    def map_inputs(self):
        """Realiza o mapeamento dos inputs e os associa às variáveis correspondentes."""
        return [
            {"selector": "input#contactJob", "name": "job", "type": "text", "value": self.job},
            {"selector": "input#contactEconomicActivityCode", "name": "economic_activity_code", "type": "text",
             "value": self.economic_activity_code},
            {"selector": "input#contactMaritalStatus", "name": "marital_status", "type": "text",
             "value": self.marital_status},
            {
                "selector": "//*[@id='mainDiv']/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div/select",
                "name": "birth_day", "type": "select", "value": self.birth_day},
            {
                "selector": "//*[@id='mainDiv']/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div/select",
                "name": "birth_month", "type": "select", "value": self.birth_month},
            {
                "selector": "//*[@id='mainDiv']/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[1]/div/div[3]/div/div/select",
                "name": "birth_year", "type": "select", "value": self.birth_year},
            {"selector": "#contactHomeland", "name": "homeland", "type": "select", "value": self.homeland}
        ]

    def preencher_formulario(self):
        """Preenche os campos de texto e seleções mapeados."""
        try:
            print("Aguarde enquanto os campos estão carregando...")

            # Aguarda o elemento principal do formulário carregar (utilizando o seletor do primeiro campo)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#contactJob"))
            )
            print("Os campos do formulário foram carregados com sucesso.")

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
                        select.select_by_visible_text(campo['value'])
                        print(f"Campo de seleção '{campo['name']}' preenchido com: {campo['value']}")
                except Exception as e:
                    print(f"Erro ao preencher o campo '{campo['name']}': {e}")

            print("Todos os campos foram preenchidos com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher o formulário: {e}")