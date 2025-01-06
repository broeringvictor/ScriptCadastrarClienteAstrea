from UseCases.AdicionarContato import AstreaDocumentation
from Shared.LoginAstrea import LoginAstrea
from UseCases.AdicionarContato.AstreaAdditional import AstreaAdditional
from UseCases.AdicionarContato.AstreaPersonal import AstreaPersonal

from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# Configurar o modo headless
options = Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")  # Opcional, melhora a compatibilidade
options.add_argument("--no-sandbox")  # Recomendado para servidores Linux
options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória

# Iniciar o navegador com as opções configuradas
driver = uc.Chrome(options=options)
base_url = r"https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"


try:
    # Login
    login_astrea = LoginAstrea(driver=driver, base_url=base_url)
    login_astrea.login()
    print("Login realizado com sucesso.")

    # Preenchimento da seção "Pessoal"
    try:
        astrea_personal = AstreaPersonal(driver)
        astrea_personal.set_data_from_client(novo_cliente)  # Chamar o método para transferir os dados
        astrea_personal.verificar_e_navegar_para_url(5)
        astrea_personal.preencher_formulario()
        print("Formulário 'Pessoal' preenchido com sucesso.")
    except Exception as e:
        print(f"Erro ao preencher o formulário 'Pessoal': {e}")

    # Preenchimento da seção "Adicional"
    try:
        astrea_additional = AstreaAdditional(driver)
        astrea_additional.set_data_from_client(novo_cliente)  # Passa os dados centralizados para o preenchimento
        astrea_additional.verificar_e_navegar_para_url(5)
        astrea_additional.preencher_formulario()
        print("Formulário 'Adicional' preenchido com sucesso.")
    except Exception as e:
        print(f"Erro ao preencher o formulário 'Adicional': {e}")

    # Preenchimento da seção "Documentação"
    try:
        astrea_documentation = AstreaDocumentation(driver)
        astrea_documentation.set_data_from_client(novo_cliente)  # Passa os dados centralizados para o preenchimento
        astrea_documentation.verificar_e_navegar_para_url(5)
        astrea_documentation.preencher_formulario()
        print("Formulário 'Documentação' preenchido com sucesso.")
        astrea_documentation.enviar_formulario()

    except Exception as e:
        print(f"Erro ao preencher o formulário 'Documentação': {e}")

except Exception as e:
    print(f"Erro durante o processo principal: {e}")


