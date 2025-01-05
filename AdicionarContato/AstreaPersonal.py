from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AstreaPersonal:
    def __init__(self, driver):
        """Inicializa o driver e os valores dos campos como atributos da classe."""
        self.driver = driver

        # Variáveis para os campos que serão preenchidos
        self.contact_name = ""
        self.contact_nickname = ""
        self.phone = ""
        self.operator = ""
        self.email = ""
        self.website = ""
        self.client_origin = ""
        self.zip_code = ""
        self.street = ""
        self.number = ""
        self.neighborhood = ""
        self.complement = ""
        self.city = ""
        self.state = ""
        self.country = ""

    def map_inputs(self):
        """Mapeia os campos do formulário associando seletores e valores."""
        return [
            {"selector": "input#contactName", "name": "contact_name", "type": "text", "value": self.contact_name},
            {"selector": "input#contactNickname", "name": "contact_nickname", "type": "text",
             "value": self.contact_nickname},
            {"selector": "input#ga-input-phone", "name": "phone", "type": "text", "value": self.phone},
            {"selector": "input#ga-input-operator", "name": "operator", "type": "text", "value": self.operator},
            {"selector": "input#ga-input-email", "name": "email", "type": "email", "value": self.email},
            {"selector": "input#ga-input-website", "name": "website", "type": "text", "value": self.website},
            {"selector": "input#ga-input-origin", "name": "client_origin", "type": "text", "value": self.client_origin},
            {"selector": "input#ga-input-cep", "name": "zip_code", "type": "text", "value": self.zip_code},
            {"selector": "input#ga-input-street", "name": "street", "type": "text", "value": self.street},
            {"selector": "input#ga-input-number", "name": "number", "type": "text", "value": self.number},
            {"selector": "input#ga-input-neighborhood", "name": "neighborhood", "type": "text",
             "value": self.neighborhood},
            {"selector": "input#ga-input-complement", "name": "complement", "type": "text", "value": self.complement},
            {"selector": "input#ga-input-city", "name": "city", "type": "text", "value": self.city},
            {"selector": "input#ga-input-state", "name": "state", "type": "text", "value": self.state},
            {"selector": "input#ga-input-country", "name": "country", "type": "text", "value": self.country},
        ]
    def verificar_e_navegar_para_url(self):
        """
        Verifica a URL atual e navega para a URL específica se necessário.
        """
        url_desejada = "https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"

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

    def preencher_formulario(self):
        """Preenche os campos de texto mapeados."""
        try:
            print("Aguarde enquanto os campos estão carregando...")

            # Verificar se a página foi carregada corretamente
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.map_inputs()[0]["selector"]))
            )
            print("Os campos do formulário foram carregados com sucesso.")

            # Itera pelos campos mapeados e os preenche
            for campo in self.map_inputs():
                try:
                    print(f"Preenchendo campo: {campo['name']} com o valor '{campo['value']}'")
                    elemento = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, campo["selector"]))
                    )
                    elemento.clear()  # Limpa o campo antes de inserir o valor
                    elemento.send_keys(campo["value"])
                    print(f"Campo '{campo['name']}' preenchido com sucesso.")

                except Exception as e:
                    print(f"Erro ao preencher o campo '{campo['name']}': {e}")

            print("Todos os campos foram preenchidos com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher o formulário: {e}")
            raise
