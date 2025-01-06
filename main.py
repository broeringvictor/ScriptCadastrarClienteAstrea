from UseCases.AdicionarContato import AstreaDocumentation
from Shared.LoginAstrea import LoginAstrea
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
from UseCases.BuscarContato.BuscarClientesPF import BuscarClientesPF
from UseCases.AdicionarContato.AstreaAdditional import AstreaAdditional
from UseCases.AdicionarContato.AstreaPersonal import AstreaPersonal
from UseCases.AdicionarContato.AstreaDocumentation import AstreaDocumentation


def main():
    # Configurar as opções do Chrome
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Descomente para o modo "headless" se necessário
    # options.add_argument("--headless")

    try:
        # Inicializar o driver com as opções corrigidas
        driver = uc.Chrome(options=options, use_subprocess=True)
        base_url = r"https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"

        # Passo 1: Selecionar um cliente no terminal
        cliente_selecionado = BuscarClientesPF.selecionar_cliente()

        if not cliente_selecionado:
            print("Nenhum cliente foi selecionado.")
            return

        print(f"\nCliente selecionado: {cliente_selecionado}")

        # Passo 2: Realizar login
        login_astrea = LoginAstrea(driver=driver, base_url=base_url)
        login_astrea.login()
        print("Login realizado com sucesso.")

        # Passo 3: Preenchimento da seção Personal
        personal_section = AstreaPersonal(driver)
        personal_section.set_data_from_client(cliente_selecionado)

        print("---------- Navegando para a seção 'Personal' ----------")
        personal_section.verificar_e_navegar_para_url()
        personal_section.preencher_formulario()

        # Passo 4: Preenchimento da seção Additional
        additional_section = AstreaAdditional(driver)
        additional_section.set_data_from_client(cliente_selecionado)

        print("Navegando para a seção 'Additional'...")
        additional_section.verificar_e_navegar_para_url(extra_delay=5)
        additional_section.preencher_formulario()

        # Passo 5: Preenchimento da seção Documentation
        documentation_section = AstreaDocumentation(driver)
        documentation_section.set_data_from_client(cliente_selecionado)

        print("Navegando para a seção 'Documentation'...")
        documentation_section.verificar_e_navegar_para_url(extra_delay=5)
        documentation_section.preencher_formulario()

        # Passo 6: Revisar e enviar o formulário
        documentation_section.enviar_formulario()
        print("Formulário preenchido e enviado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")

    finally:
        # Encerrar o driver com segurança
        try:
            time.sleep(5)
           # driver.quit()
        except Exception as driver_error:
            print(f"Erro ao encerrar o driver: {driver_error}")


if __name__ == "__main__":
    main()