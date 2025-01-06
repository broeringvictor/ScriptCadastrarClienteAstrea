from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class AstreaPersonal:
    def __init__(self, driver):
        """Inicializa o driver e os valores dos campos como atributos da classe."""
        self.driver = driver

        # Variáveis para os campos que serão preenchidos
        self.contact_name = ""
        self.contact_nickname = ""
        self.phone = ""
        self.email = ""
        self.website = ""
        self.zip_code = ""
        self.street = ""
        self.number = ""
        self.neighborhood = ""
        self.complement = ""
        self.city = ""
        self.state = ""
        self.country = ""
    def set_data_from_client(self, client):
        self.contact_name = client.contact_name
        self.contact_nickname = client.contact_nickname
        self.phone = client.phone
        self.email = client.email
        self.website = client.website
        self.zip_code = client.zip_code
        self.street = client.street
        self.number = client.number
        self.neighborhood = client.neighborhood
        self.complement = client.complement
        self.city = client.city
        self.state = client.state
        self.country = client.country
    def map_inputs(self):
        """Mapeia os campos do formulário associando seletores e valores."""
        return [
            {"selector": "input#contactName", "name": "contact_name", "type": "text", "value": self.contact_name},
            {"selector": "input#contactNickname", "name": "contact_nickname", "type": "text",
             "value": self.contact_nickname},
            {"selector": "#mainDiv > div.au-app-access > div > div > main > div > div > div > div.page-wrapper.ng-scope > div > div > div.ng-scope > div > div > div:nth-child(5) > div > div > div.row.middle-xs > div.col-xs.col-sm.nix-margin-top_10--xs > div > input", "name": "email", "type": "email", "value": self.email},
            {"selector": "#mainDiv > div.au-app-access > div > div > main > div > div > div > div.page-wrapper.ng-scope > div > div > div.ng-scope > div > div > div.ga-field.ng-scope > div > div > div > input", "name": "website", "type": "text", "value": self.website},
            {"selector": "input[placeholder='Digite o CEP']", "name": "zip_code", "type": "text", "value": self.zip_code},

            {"selector": "input[placeholder='Digite a rua']", "name": "street", "type": "text", "value": self.street},

            {"selector": "input[placeholder='Digite o número']", "name": "number", "type": "text", "value": self.number},

            {"selector": "input[placeholder='Digite o bairro']", "name": "neighborhood", "type": "text", "value": self.neighborhood},

            {"selector": "input[placeholder='Digite o complemento']", "name": "complement", "type": "text", "value": self.complement},

            {"selector": "input[placeholder='Digite a cidade']", "name": "city", "type": "text", "value": self.city},

            {"selector": "input[placeholder='Digite o estado']", "name": "state", "type": "text", "value": self.state},

            {"selector": "input[placeholder='Digite o país']", "name": "country", "type": "text", "value": self.country},

        ]
    def verificar_e_navegar_para_url(self, extra_delay=5):
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

            if extra_delay:
                print(f"Extra_delay --> Aguardando {extra_delay} segundos...")
                time.sleep(extra_delay)

        except Exception as e:
            print(f"Erro ao verificar ou navegar para a URL: {e}")
            raise  # Lança o erro para depuração em um nível mais alto

    def preencher_formulario(self):
        """Preenche os campos do formulário utilizando os valores configurados."""
        try:
            print("Aguarde enquanto os campos estão carregando...")

            # Aguarda a página carregar e o formulário ficar disponível
            print("Preenchendo o campo de telefone...")

            # Localiza o campo do telefone (antes de alterar o tipo para WhatsApp)
            phone = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="mainDiv"]/div[2]/div/div/main/div/div/div/div[4]/div/div/div[1]/div/div/div[4]/div/div/div/div[2]/div/input'))
            )
            phone.clear()
            phone.send_keys(self.phone)
            print(f"Telefone '{self.phone}' preenchido com sucesso.")

            # Altera o tipo do telefone para WhatsApp
            selector_path = (
                "#mainDiv > div.au-app-access > div > div > main > div > div > div > "
                "div.page-wrapper.ng-scope > div > div > div.ng-scope > div > div > "
                "div:nth-child(4) > div > div > div > div.col-sm-4.col-xs-12.ng-scope > "
                "div > div > select"
            )


            # Preenche os demais campos do formulário
            print("Preenchendo os campos restantes...")
            for campo in self.map_inputs():
                if campo["name"] == "phone":  # Ignora o campo de telefone, pois já foi preenchido
                    continue

                try:
                    print(f"Preenchendo o campo: {campo['name']} com o valor '{campo['value']}'")

                    elemento = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, campo["selector"]))
                    )
                    elemento.clear()  # Limpa o conteúdo do campo
                    elemento.send_keys(campo["value"])  # Insere o valor no campo
                    print(f"Campo '{campo['name']}' preenchido com sucesso.")

                except Exception as e:
                    print(f"Erro ao preencher o campo '{campo['name']}': {e}")

            print("Todos os campos foram preenchidos com sucesso.")

            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_path))
            )
            select = Select(select_element)
            select.select_by_visible_text("WhatsApp")
            print("Opção 'WhatsApp' selecionada com sucesso.")

        except Exception as e:
            print(f"Erro ao preencher o formulário: {e}")
            raise  # Lança o erro para análise
