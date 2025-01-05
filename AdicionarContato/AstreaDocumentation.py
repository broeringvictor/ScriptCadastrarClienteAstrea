from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class AstreaDocumentation:
    def __init__(self, driver):
        # Passar o driver diretamente como argumento reduz a dependência de importação circular
        self.driver = driver
        self.cpf = ""
        self.rg = ""
        self.ctps = ""
        self.benefit_document = ""
        self.voter_document = ""
        self.driver_license = ""
        self.passport = ""

    def verificar_e_navegar_para_url(self):
        """
        Verifica a URL atual e navega para a URL específica se necessário.
        """
        url_desejada = "https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/documentation"

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
        """Mapeia os campos de entrada com seletores e suas informações."""
        return [
            {
                "selector": "#mainDiv > div.au-app-access > div > div > main > div > div > div > div.page-wrapper.ng-scope > div > div > div.row.ng-scope > div > div > div:nth-child(1) > div > div > div > div > input",
                "name": "CPF", "type": "text", "value": self.cpf},
            {"selector": "#contactIdDocumentNumber", "name": "RG", "type": "text", "value": self.rg},
            {"selector": "#contactJobDocumentNumber", "name": "Carteira de Trabalho", "type": "text",
             "value": self.ctps},
            {"selector": "#contactJobBenefitDocumentNumber", "name": "Benefício", "type": "text",
             "value": self.benefit_document},
            {"selector": "#contactVoterDocumentNumber", "name": "Título de Eleitor", "type": "text",
             "value": self.voter_document},
            {"selector": "#contactDriverDocumentNumber", "name": "Carteira de Motorista", "type": "text",
             "value": self.driver_license},
            {"selector": "#contactPassportNumber", "name": "Passaporte", "type": "text", "value": self.passport}
        ]

    def preencher_formulario(self):
        """Preenche os campos de texto mapeados."""
        try:
            print("Aguarde enquanto os campos estão carregando...")

            # Aguarda o primeiro campo da página estar disponível
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.map_inputs()[0]["selector"]))
            )
            print("Os campos do formulário foram carregados com sucesso.")

            # Itera pelos campos mapeados
            for campo in self.map_inputs():
                try:
                    print(f"Preenchendo campo: {campo['name']}")

                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, campo["selector"]))
                    )
                    element.clear()
                    element.send_keys(campo["value"])
                    print(f"Campo '{campo['name']}' preenchido com sucesso.")
                except Exception as e:
                    print(f"Erro ao preencher o campo '{campo['name']}': {e}")

            print("Todos os campos foram preenchidos com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher o formulário: {e}")

        def enviar_formulario(self):
            """Função para enviar o formulário clicando no botão de envio."""
            try:
                print("Tentando localizar o botão de envio do formulário...")

                # Aguarda até que o botão esteja presente e clicável
                button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        "#mainDiv > div.au-app-access > div > div > main > div > div > div > "
                        "div.page-wrapper.ng-scope > div > div > "
                        "div.col-xs-12.nix-display_flex.end-xs.nix-flex-direction_column--xs.middle-xs > button"
                    ))
                )

                # Realiza o clique no botão de envio
                print("Botão localizado. Preparando para clicar...")
                ActionChains(self.driver).move_to_element(button).click(button).perform()
                print("Formulário enviado com sucesso!")

            except Exception as e:
                print(f"Erro ao tentar enviar o formulário: {e}")
                raise  # Propaga o erro para depuração