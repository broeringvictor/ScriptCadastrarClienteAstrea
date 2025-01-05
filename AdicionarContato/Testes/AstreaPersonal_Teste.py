from AdicionarContato.LoginAstrea import LoginAstrea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAstreaPersonal:
    def __init__(self, driver):
        """Inicializa com um driver Selenium."""
        self.driver = driver

    def preencher_formulario(self):
        """Preenche o formulário com dados fictícios."""
        try:
            print("Aguarde enquanto os campos estão carregando...")

            # Aguarda a presença de um dos campos do formulário para garantir que a página foi carregada
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#contactName"))
            )
            print("Os campos do formulário foram carregados com sucesso.")

            # Dados fictícios para teste
            dados_teste = {
                "Pesquisar contato, processo ou tarefa": "Contato teste",
                "Digite o nome": "João Fictício",
                "Digite o apelido": "Joãozinho",
                "Digite o telefone": "11999999999",
                "Operadora": "Vivo",
                "Digite o email": "joao.ficticio@example.com",
                "Digite o site": "www.exemplo.com",
                "Digite a origem do cliente": "Indicação",
                "Digite o CEP": "12345-678",
                "Digite a rua": "Rua dos Testes",
                "Digite o número": "123",
                "Digite o bairro": "Bairro Fictício",
                "Digite o complemento": "Casa 2",
                "Digite a cidade": "São Paulo",
                "Digite o estado": "SP",
                "Digite o país": "Brasil",
            }

            # Loop para preencher os campos com logs detalhados
            for placeholder, valor in dados_teste.items():
                try:
                    print(f"Tentando preencher o campo com placeholder: {placeholder}")
                    # Localiza o campo pelo placeholder e preenche com o valor fictício
                    campo = self.driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
                    campo.clear()  # Limpa o campo antes de preencher
                    campo.send_keys(valor)
                    print(f"Campo '{placeholder}' preenchido com: {valor}")
                except Exception as e_inner:
                    print(f"Erro ao preencher o campo '{placeholder}': {e_inner}")

            print("Todos os campos disponíveis foram processados.")
        except Exception as e_outer:
            print(f"Erro ao preencher o formulário: {e_outer}")


# Script Principal
try:
    # Instancia a classe de login e realiza o login
    login_astrea = LoginAstrea()
    login_astrea.login()

    print("Login realizado com sucesso. Acessando página de teste...")

    # Instancia a classe de teste com o driver do LoginAstrea
    tester = TestAstreaPersonal(login_astrea.driver)
    tester.preencher_formulario()

    print("Teste de preenchimento de formulário concluído. Verifique os dados no navegador.")
except Exception as e:
    print(f"Erro ao executar o script de teste: {e}")