from AdicionarContato.AstreaDocumentation import AstreaDocumentation
from AdicionarContato.LoginAstrea import LoginAstrea
from AdicionarContato.AstreaAdditional import AstreaAdditional
from AdicionarContato.AstreaPersonal import AstreaPersonal
import undetected_chromedriver as uc



driver = uc.Chrome(use_subprocess=True)
base_url = r"https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"
# Instanciar a classe e executar o login
try:
    login_astrea = LoginAstrea(driver=driver, base_url=base_url)
    login_astrea.login()
    print("Login realizado com sucesso. O navegador permanecerá aberto.")
except Exception as e:
    print(f"Erro ao executar o login: {e}")

try:
    astrea_personal = AstreaPersonal(driver)
    astrea_personal.verificar_e_navegar_para_url()
    astrea_personal.preencher_formulario()

except Exception as e:
    print(f"Erro ao instanciar AstreaPersonal: {e}")

    try:
        astrea_additional = AstreaAdditional(driver)
        astrea_additional.verificar_e_navegar_para_url()
        astrea_additional.preencher_formulario()
    except Exception as e:
        print(f"Erro ao instanciar AstreaAdditional: {e}")

try:
    astrea_documentation = AstreaDocumentation(driver)
    astrea_documentation.verificar_e_navegar_para_url()
    astrea_documentation.preencher_formulario()

except Exception as e:
    print(f"Erro ao instanciar AstreaDocumentation: {e}")

