from AdicionarContato.LoginAstrea import LoginAstrea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome
import time
from bs4 import BeautifulSoup
import threading

class CapturarInputs:
    def __init__(self, driver, base_url=None):
        """
        Inicializa a classe com o WebDriver e uma URL base opcional.
        :param driver: Instância do WebDriver.
        :param base_url: URL padrão a ser carregada (opcional).
        """
        self.driver = driver
        self.base_url = (
                base_url
                or "https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"
        )

    def capturar_inputs_com_seletores(self):
        """
        Espera até que a página seja carregada e captura todos os <input> no DOM,
        mostrando seletor, type, name, placeholder, e value.
        """
        try:
            time.sleep(10)
            # Aguarda até que apareça pelo menos 1 <input>
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )

            # Captura todos os <input>
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            if not inputs:
                print("Nenhum elemento <input> encontrado na página.")
                return

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
        Tenta gerar um seletor CSS simples e curto baseado em:
         - id único
         - name único
         - placeholder único
         - ng-model único
        Se não encontrar, gera fallback simplificado.
        """
        from selenium.webdriver.common.by import By

        tag = element.tag_name.lower()
        attrs_to_try = ["id", "name", "placeholder", "ng-model"]

        # 1) Verifica se o elemento tem um desses atributos e se é único no DOM
        for attr in attrs_to_try:
            value = element.get_attribute(attr)
            if value:
                candidate = f'{tag}[{attr}="{value}"]'
                found = self.driver.find_elements(By.CSS_SELECTOR, candidate)
                if len(found) == 1:
                    return candidate

        # 2) Fallback se não achou nada único
        return self._get_dom_path(element)

    def _get_dom_path(self, element):
        """
        Fallback gerando caminho simples subindo no DOM até <html> ou <body>.
        """
        path = []
        current = element
        while current:
            tag = current.tag_name.lower()
            if tag in ["html", "body"]:
                break

            elem_id = current.get_attribute("id")
            if elem_id:
                path.append(f"{tag}#{elem_id}")
                break
            else:
                path.append(tag)

            try:
                current = current.find_element(By.XPATH, "./..")
            except:
                break

        return " > ".join(reversed(path))

    def get_url_with_timeout(self, prompt, timeout):
        """
        Captura entrada do usuário com timeout.
        Se o usuário não digitar nada no tempo limite,
        ou digitar espaços em branco, retorna self.base_url.
        """
        user_input = []

        def read_input():
            user_input.append(input(prompt))

        input_thread = threading.Thread(target=read_input)
        input_thread.daemon = True
        input_thread.start()
        input_thread.join(timeout)

        # Se acabou o tempo (ou o usuário apertou Enter sem digitar nada)
        if not user_input or not user_input[0].strip():
            return self.base_url.strip()
        else:
            return user_input[0].strip()


if __name__ == "__main__":
    # 1) Inicia o driver
    driver = Chrome(use_subprocess=True)

    # 2) Cria instância de CapturarInputs
    capturar = CapturarInputs(driver)

    # 3) Tenta obter URL do usuário ou usa base_url
    url = capturar.get_url_with_timeout(
        "Digite a URL desejada (ou ENTER p/ padrão): ", 10
    )
    print(f"URL escolhida: {url}")

    # 4) Faz login com classe LoginAstrea
    login_astrea = LoginAstrea(driver=driver, base_url=url)
    login_astrea.login()

    # 5) Carrega a URL
    driver.get(url)

    # 6) (Opcional) Captura e imprime os <input> usando Selenium
    #    Se não quiser, pode pular. Às vezes você só quer o BeautifulSoup
    capturar.capturar_inputs_com_seletores()

    # 7) Agora, obtemos o HTML **pós-login** para uso no BeautifulSoup
    html_logado = driver.page_source

    # 8) Usa BeautifulSoup no HTML obtido (já autenticado)
    soup = BeautifulSoup(html_logado, "html.parser")

    # Exemplo: encontrar e imprimir todos os <form> e seus <input>, <select>, etc.
    forms = soup.find_all("form")
    for i, form in enumerate(forms, start=1):
        print(f"--- Formulário {i} ---")

        form_method = form.get("method", "GET/POST não especificado")
        form_action = form.get("action", "Action não especificado")
        print(f"Método: {form_method}")
        print(f"Action: {form_action}")

        # Buscar <input> dentro do <form>
        inputs = form.find_all("input")
        for j, inp in enumerate(inputs, start=1):
            input_name = inp.get("name", "Sem nome")
            input_type = inp.get("type", "text")
            input_placeholder = inp.get("placeholder", "Sem placeholder")
            input_value = inp.get("value", "Sem valor")
            print(f"  Input {j}: name={input_name}, type={input_type}, "
                  f"placeholder={input_placeholder}, value={input_value}")

        # Se também quiser <select> e <textarea>, basta:
        selects = form.find_all("select")
        for sel in selects:
            print(f"  Select com name={sel.get('name')} e options:")
            for opt in sel.find_all("option"):
                print(f"    -> {opt.get('value')}, texto={opt.text.strip()}")

        textareas = form.find_all("textarea")
        for txt in textareas:
            print(f"  TextArea com name={txt.get('name')}, valor={txt.text}")

        print("\n")

    # 9) Fecha o driver
    try:
        driver.quit()
    except Exception as e:
        print(f"Erro ao encerrar o driver: {e}")
