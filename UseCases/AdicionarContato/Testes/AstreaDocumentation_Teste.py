from UseCases.AdicionarContato.AstreaDocumentation import AstreaDocumentation
from Shared.LoginAstrea import LoginAstrea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def executar_teste(driver):
    """Executa o fluxo de teste utilizando um driver fornecido externamente."""
    if driver is None:
        raise ValueError("O driver não foi fornecido. Certifique-se de inicializá-lo antes de executar o teste.")

    try:
        print("Iniciando o processo de login...")

        # Instancia a classe LoginAstrea
        login_astrea = LoginAstrea(driver)
        login_astrea.login()  # Realiza o login

        print("Login realizado com sucesso. Aguardando o carregamento da página principal...")

        # Aguarda o DOM carregar completamente após o login
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#mainDiv > div.au-app-access > div > div > main > div > div > div > div.page-wrapper.ng-scope > div > div > div.row.ng-scope > div > div > div:nth-child(1) > div > div > div > div > input"
            ))
        )
        print("Página principal carregada com sucesso.")

        # Instancia a classe para preenchimento do formulário
        print("Iniciando o preenchimento do formulário...")
        formulario = AstreaDocumentation()

        # Configurando valores para os campos
        formulario.cpf = "123.456.789-00"
        formulario.rg = "12.345.678-9"
        formulario.ctps = "54321 / 2020 / SP"
        formulario.benefit_document = "987654321"
        formulario.voter_document = "23456789 / 123 / 456"
        formulario.driver_license = "654321 / AB / 2030-12-31"
        formulario.passport = "P1234567 / Comum / PF / Brasil / 2025-06-15"

        # Preenche o formulário utilizando o driver
        formulario.preencher_formulario(driver)
        print("Formulário preenchido com sucesso. Verifique os dados no navegador.")

    except Exception as e:
        print(f"Erro ao executar o script de teste: {e}")
        raise  # Propaga o erro para facilitar depuração externa


if __name__ == "__main__":
    try:
        # Inicializa o driver antes de passar para a função
        print("Inicializando o driver...")
        driver = uc.Chrome()

        # Executa o teste com o driver inicializado
        executar_teste(driver)

    except Exception as e:
        print(f"Erro durante a execução do teste principal: {e}")

    finally:
        # Feche o navegador corretamente após a execução
        if driver:
            # Aguarda o usuário digitar algo no console antes de fechar o navegador
            input("Pressione Enter para fechar o navegador...")

            # Fecha o navegador
            driver.quit()
            print("Navegador fechado com sucesso.")

