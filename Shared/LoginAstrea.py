import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


class LoginAstrea:
    def __init__(self, driver=None, base_url=None):
        """
        Inicializa o LoginAstrea com suporte para URL externa e WebDriver opcional.

        :param driver: Instância do WebDriver, opcional.
        :param base_url: URL base para login, opcional. Utiliza uma URL padrão se não for fornecida.
        """
        # Carrega variáveis do arquivo .env
        load_dotenv()

        # Inicializa atributos da classe
        self.driver = driver  # Driver externo opcional
        self.base_url = base_url or r"https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/documentation"
        self.senha = os.getenv("SENHA")  # Obtém a variável de ambiente 'SENHA' do .env
        self.usuario = os.getenv("USUARIO", "victor@victorbroering.adv.br")  # Obtém 'USUARIO', ou define padrão

        # Valida se credenciais foram configuradas corretamente
        if not self.senha or not self.usuario:
            raise ValueError("As variáveis 'USUARIO' ou 'SENHA' não foram definidas no arquivo .env.")

    def iniciar_driver(self):
        """Inicializa o WebDriver se ainda não foi fornecido."""
        if not self.driver:  # Inicializa o driver apenas se ele ainda não foi fornecido
            print("Inicializando o driver...")
            self.driver = uc.Chrome(use_subprocess=True)

        # Acessa a URL base
        self.driver.get(self.base_url)
        print(f"Driver iniciado e URL acessada: {self.base_url}")

    def preencher_formulario(self):
        """Localiza e preenche os campos do formulário de login."""
        if not self.driver:  # Garante que o driver foi inicializado
            raise ValueError("O driver precisa ser inicializado antes de preencher o formulário.")

        try:
            print("Preenchendo o formulário de login...")

            # Define o tempo de espera para carregar os elementos do DOM
            wait = WebDriverWait(self.driver, 10)

            # Localiza os elementos de usuário, senha e botão de envio
            input_user = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#refac > ui-view > div > main > div > react-login > div > div > div > div > div > form > div:nth-child(1) > div > input")
            ))
            input_password = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#refac > ui-view > div > main > div > react-login > div > div > div > div > div > form > div:nth-child(2) > div > input")
            ))
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "#refac > ui-view > div > main > div > react-login > div > div > div > div > div > form > div.css-skzzd6-WrapButton.enilzg65 > button")
            ))

            # Preenche os campos e envia as credenciais
            input_user.clear()
            input_user.send_keys(self.usuario)

            input_password.clear()
            input_password.send_keys(self.senha)

            submit_button.click()
            print("Formulário enviado com sucesso.")

        except Exception as e:
            print(f"Erro durante o preenchimento do formulário de login: {e}")
            raise  # Propaga o erro para facilitar a depuração

    def validar_login(self):
        """Valida se o login foi bem-sucedido."""
        try:
            # Use um elemento que aparece apenas quando a página principal é carregada após o login
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#mainDiv > div.au-app-access > div > div > main")  # Exemplo de seletor
                )
            )
            print("Login validado com sucesso.")
            return True
        except Exception as e:
            print(f"Falha ao validar o login: {e}")
            return False

    def login(self):
        """Executa o processo completo de login."""
        try:
            # Inicializa o driver (se necessário) e preenche o formulário
            self.iniciar_driver()
            self.preencher_formulario()

            # Valida se o login foi bem-sucedido
            if self.validar_login():
                print("Login concluído com sucesso.")
            else:
                raise Exception("Falha ao realizar o login. Verifique as credenciais ou o estado do sistema.")

        except Exception as e:
            print(f"Erro no processo de login: {e}")
            raise  # Propaga o erro para permitir tratamento externo