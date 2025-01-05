from AdicionarContato.AstreaDocumentation import AstreaDocumentation
from AdicionarContato.LoginAstrea import LoginAstrea
from AdicionarContato.AstreaAdditional import AstreaAdditional
from AdicionarContato.AstreaPersonal import AstreaPersonal
from AdicionarContato.AstreaNewClient import AstreaNewClient
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

# Dados do cliente centralizados em uma instância da classe AstreaNewClient
novo_cliente = AstreaNewClient(
    # Dados pessoais
    contact_name="João Silva",
    contact_nickname="João",
    phone="48991668808",

    email="joaosilva@email.com",
    website="www.joaosilva.com",

    zip_code="12345-678",
    street="Rua das Flores",
    number="123",
    neighborhood="Centro",
    complement="Apto. 45",
    city="São Paulo",
    state="SP",
    country="Brasil",
    # Dados adicionais
    job="Analista de Sistemas",
    economic_activity_code="6201-5/01",
    marital_status="Solteiro",
    birth_day="15",
    birth_month="Junho",
    birth_year="1990",
    homeland="Brasil",
    # Documentos
    cpf="123.456.789-10",
    rg="12.345.678-9",
    ctps="12345678",
    benefit_document="345678910",
    voter_document="123456789123",
    driver_license="AB123456",
    passport="AB12345678"
)

# Fluxo principal para preencher os formulários no Astrea
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


