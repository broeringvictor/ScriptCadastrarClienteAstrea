from AdicionarContato.LoginAstrea import LoginAstrea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CapturarInputs:
    def __init__(self, driver):
        """Recebe o driver existente."""
        self.driver = driver

    def capturar_inputs_com_seletores(self):
        """Espera até que a página seja carregada e captura todos os inputs com seus seletores CSS."""
        try:
            # Aguarda até que o campo #contactName esteja presente (indicando que estamos na página correta)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainDiv > div.au-app-access > div > div > main > div > div > div > div.page-wrapper.ng-scope > div > div > div.row.ng-scope > div > div > div:nth-child(1) > div > div > div > div > input"))
            )

            # Captura todos os elementos <input> no DOM
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            if not inputs:
                print("Nenhum elemento <input> encontrado na página.")
                return

            # Lista informações com seus CSS_SELECTORS
            print(f"Quantidade de inputs encontrados: {len(inputs)}\n")
            for index, input_element in enumerate(inputs, start=1):
                input_css_selector = self._get_css_selector(input_element)
                input_type = input_element.get_attribute("type") or "Não especificado"
                input_value = input_element.get_attribute("value") or "Sem valor"
                input_name = input_element.get_attribute("name") or "Sem nome"
                input_placeholder = input_element.get_attribute("placeholder") or "Sem placeholder"

                print(
                    f"Input {index}:\n"
                    f"  Selector: {input_css_selector}\n"
                    f"  Tipo: {input_type}\n"
                    f"  Nome: {input_name}\n"
                    f"  Placeholder: {input_placeholder}\n"
                    f"  Valor: {input_value}\n"
                )

        except Exception as e:
            print(f"Erro ao capturar inputs: {e}")

    def _get_css_selector(self, element):
        """
        Gera o seletor CSS completo de um elemento.
        """
        path = []
        while element is not None:
            tag = element.tag_name
            id_attr = element.get_attribute("id")
            class_attr = element.get_attribute("class")

            if id_attr:
                # Se o elemento tiver um ID, usamos isso diretamente
                path.append(f"{tag}#{id_attr}")
                break
            elif class_attr:
                # Caso tenha classes, usamos a primeira classe disponível no seletor
                main_class = class_attr.split()[0]
                path.append(f"{tag}.{main_class}")
            else:
                # Caso não tenha ID ou classe, usamos o índice do nó
                siblings = element.find_elements(By.XPATH, f"./parent::*/*[name()='{tag}']")
                index = siblings.index(element) + 1
                path.append(f"{tag}:nth-of-type({index})")

            element = element.find_element(By.XPATH, "./parent::*")

        return " > ".join(reversed(path))

    def informacoes_complementares(self):
        """Executa a navegação e interação necessária para acessar a seção de Informações Complementares."""
        try:
            # Rola para o topo da página
            self.driver.execute_script("window.scrollTo(0, 0);")
            print("Página rolada para o topo.")

            # Aguarda o elemento com a propriedade 'name' ficar visível
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )
            print("Elemento com atributo 'name' encontrado e visível.")

            # Aguarda e clica no elemento "Informações Complementares"
            informacoes_complementares = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@id="mainDiv"]/div[2]/div/div/main/div/div/div/div[3]/div/ul/li[2]'
                ))
            )
            informacoes_complementares.click()
            print("O elemento 'Informações Complementares' foi clicado com sucesso.")

        except Exception as e:
            print(f"Erro ao executar a função informacoes_complementares: {e}")


# Script Principal
try:
    # Inicializa e faz login
    login_astrea = LoginAstrea()
    login_astrea.login()

    # Acessar a URL de "Adicionar Contrato" (caso necessário)
    login_astrea.driver.get("https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/documentation")

    # Inicializa o capturador
    capturador = CapturarInputs(login_astrea.driver)

    # Capturar inputs na página de "Adicionar Contrato"
    print("Iniciando captura de inputs na tela inicial.")
    capturador.capturar_inputs_com_seletores()





    print("Processo concluído com sucesso!")

except Exception as e:
    print(f"Erro ao executar o script: {e}")