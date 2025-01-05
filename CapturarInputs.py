import time
import threading
from bs4 import BeautifulSoup
import atexit

from AdicionarContato.LoginAstrea import LoginAstrea
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome


class CapturarInputs:
    def __init__(self, driver, base_url=None):
        """
        Inicializa a classe com o WebDriver e uma URL base opcional.

        :param driver: Instância do WebDriver (undetected_chromedriver).
        :param base_url: URL padrão a ser carregada (opcional).
        """
        self.driver = driver
        self.base_url = base_url or (
            "https://astrea.net.br/#/main/contacts/add-edit-merge/%5B,,false,%5B%5D,%5D/personal"
        )

    def capturar_inputs_com_seletores(self, extra_delay=10):
        """
        Espera até que a página seja carregada e captura todos os <input> com seletores.

        :param extra_delay: segundos extras de espera após o WebDriverWait.
        """
        try:

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )

            # Se desejar, acrescente um delay adicional para JS/Angular (opcional)
            if extra_delay:
                print(f"Aguardando {extra_delay} segundos...")
                time.sleep(extra_delay)

            # Captura todos os <input> no DOM
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            if not inputs:
                print("Nenhum elemento <input> encontrado na página.")
                return

            print(f"Quantidade de inputs encontrados: {len(inputs)}\n")

            for index, input_element in enumerate(inputs, start=1):
                # Gera os seletores (CSS e XPath)
                css_selector = self._get_css_selector(input_element)
                xpath_selector = self._get_xpath_selector(input_element)

                # Captura atributos úteis
                input_type = input_element.get_attribute("type") or "Não especificado"
                input_value = input_element.get_attribute("value") or "Sem valor"
                input_name = input_element.get_attribute("name") or "Sem nome"
                input_placeholder = input_element.get_attribute("placeholder") or "Sem placeholder"

                print(
                    f"Input {index}:\n"
                    f"  CSS:  {css_selector}\n"
                    f"  XPATH: {xpath_selector}\n"
                    f"  Tipo: {input_type}\n"
                    f"  Nome: {input_name}\n"
                    f"  Placeholder: {input_placeholder}\n"
                    f"  Valor: {input_value}\n"
                )

        except Exception as e:
            print(f"Erro ao capturar inputs: {e}")

    def _get_css_selector(self, element):
        """
        Gera um seletor CSS bem mais estável e curto:
        1) Se tiver id único -> ex.: input#contactName
        2) Se tiver name único -> ex.: input[name="contactName"]
        3) Se tiver placeholder único -> ex.: input[placeholder="Digite o nome"]
        4) Se tiver ng-model único -> ex.: input[ng-model="contact.name"]
        5) Caso nada disso seja único, usa _get_dom_path (fallback).
        """
        tag = element.tag_name.lower()
        attrs_to_try = ["id", "name", "placeholder", "ng-model"]

        for attr in attrs_to_try:
            val = element.get_attribute(attr)
            if val:
                candidate = f'{tag}[{attr}="{val}"]'
                found = self.driver.find_elements(By.CSS_SELECTOR, candidate)
                if len(found) == 1:
                    return candidate

        # fallback (DOM path)
        return self._get_dom_path_css(element)

    def _get_dom_path_css(self, element):
        """
        Fallback gerando um caminho simples no DOM (CSS).
        Sobe até <html> ou <body>, parando se encontrar #id.
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

    def _get_xpath_selector(self, element):
        """
        Gera um seletor XPATH alternativo.
        1) Se tiver id -> //*[@id='xxx']
        2) Se tiver name -> //tag[@name='xxx']
        3) Se tiver placeholder -> //tag[@placeholder='xxx']
        4) Se tiver ng-model -> //tag[@ng-model='xxx']
        5) Fallback, subindo na árvore, gerando algo simplificado.
        """
        tag = element.tag_name.lower()
        attrs_to_try = ["id", "name", "placeholder", "ng-model"]

        for attr in attrs_to_try:
            val = element.get_attribute(attr)
            if val:
                # ex.: //input[@id='contactName']
                return f"//{tag}[@{attr}='{val}']"

        # fallback
        return self._get_dom_path_xpath(element)

    def _get_dom_path_xpath(self, element):
        """
        Fallback para gerar XPATH subindo na árvore até body/html.
        Ex.: //body/div/div/input (forma bem simples).
        Pode ficar mais elaborado se desejar nth-child, etc.
        """
        path_segments = []
        current = element
        while current:
            tag = current.tag_name.lower()
            if tag in ["html", "body"]:
                path_segments.insert(0, tag)
                break

            # Se tiver id, paramos e usamos id
            elem_id = current.get_attribute("id")
            if elem_id:
                # ex.: //*[@id='meuId']
                path_segments.insert(0, f"*[@id='{elem_id}']")
                return f"//{'/'.join(path_segments)}"

            # senão, só põe o nome da tag
            path_segments.insert(0, tag)
            try:
                current = current.find_element(By.XPATH, "./..")
            except:
                break

        # Exemplo final: //html/body/div/div/input
        return "//" + "/".join(path_segments)

    def get_url_with_timeout(self, prompt, timeout):
        """
        Captura entrada do usuário com timeout.
        Se o usuário não digitar nada no tempo limite,
        ou digitar só espaços, retorna self.base_url.
        """
        user_input = []

        def read_input():
            user_input.append(input(prompt))

        input_thread = threading.Thread(target=read_input)
        input_thread.daemon = True
        input_thread.start()
        input_thread.join(timeout)

        if not user_input or not user_input[0].strip():
            return self.base_url.strip()
        else:
            return user_input[0].strip()


if __name__ == "__main__":
    from selenium.webdriver.chrome.options import Options
    import undetected_chromedriver as uc


    def cleanup():
        print("Liberando recursos...")
        try:
            driver.quit()
        except Exception:
            pass

    # Configurar o modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Opcional, melhora a compatibilidade
    options.add_argument("--no-sandbox")  # Recomendado para servidores Linux
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    # 2) Cria instância da classe CapturarInputs
    capturar_inputs = CapturarInputs(driver)

    # 3) Pergunta ao usuário a URL (ou usa base_url se vazio)
    url = capturar_inputs.get_url_with_timeout(
        "Digite a URL desejada (ou pressione ENTER para usar o padrão): ", 10
    )
    print(f"URL escolhida: {url}")

    # 4) Faz login com a classe LoginAstrea
    login_astrea = LoginAstrea(driver=driver, base_url=url)
    login_astrea.login()

    # 5) Carrega a URL (pós-login)
    driver.get(url)

    # 6) Captura os inputs (CSS e XPath, placeholders, etc.)
    capturar_inputs.capturar_inputs_com_seletores(extra_delay=7)

    # 7) (Exemplo) Se quiser extrair <form> com BeautifulSoup, pegue o HTML
    html_logado = driver.page_source
    soup = BeautifulSoup(html_logado, "html.parser")

    # Exemplo rápido: listar todos os <form> e seus <input>
    forms = soup.find_all("form")
    for i, form in enumerate(forms, start=1):
        print(f"\n--- Formulário {i} ---")
        method = form.get("method", "GET/POST não especificado")
        action = form.get("action", "Action não especificado")
        print(f"Método: {method}\nAction: {action}")

        form_inputs = form.find_all("input")
        for j, inp in enumerate(form_inputs, start=1):
            nm = inp.get("name", "Sem nome")
            tp = inp.get("type", "text")
            ph = inp.get("placeholder", "Sem placeholder")
            vl = inp.get("value", "Sem valor")
            print(f"  Input {j}: name={nm}, type={tp}, placeholder={ph}, value={vl}")
    print("aguardando 3 segundos")
    time.sleep(3)
    # 8) Fecha o driver
    try:
        time.sleep(3)
        atexit.register(cleanup)
    except Exception as e:
        print(f"Erro ao encerrar o driver: {e}")
