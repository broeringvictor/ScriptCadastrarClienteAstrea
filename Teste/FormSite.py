from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Configuração do WebDriver (use o caminho correto para o driver)
driver = uc.Chrome(options=options, use_subprocess=True)

# URL do formulário
url = "https://victorbroering.adv.br/cadastrar-pf/"
driver.get(url)

# Espera para garantir o carregamento da página
time.sleep(3)

# Preenchendo o formulário
try:
    # Nome do Contato
    driver.find_element(By.ID, "ff_6_ContactName").send_keys("João da Silva")

    # Apelido
    driver.find_element(By.ID, "ff_6_ContactNickname").send_keys("João")

    # Telefone
    driver.find_element(By.NAME, "telefone").send_keys("11987654321")

    # Email
    driver.find_element(By.ID, "ff_6_email").send_keys("joao.silva@email.com")

    # Website (opcional)
    driver.find_element(By.ID, "ff_6_website").send_keys("https://meusite.com")

    # Endereço
    driver.find_element(By.ID, "ff_6_ZipCode").send_keys("12345-678")
    driver.find_element(By.ID, "ff_6_Street").send_keys("Rua das Flores")
    driver.find_element(By.ID, "ff_6_Number").send_keys("123")
    driver.find_element(By.ID, "ff_6_Neighborhood").send_keys("Centro")
    driver.find_element(By.ID, "ff_6_Complement").send_keys("Apt 45")
    driver.find_element(By.ID, "ff_6_City").send_keys("São Paulo")

    # Estado
    estado_dropdown = Select(driver.find_element(By.ID, "ff_6_Estado"))
    estado_dropdown.select_by_value("SP")

    # País (opcional)
    driver.find_element(By.ID, "ff_6_Country").send_keys("Brasil")

    # Profissão
    driver.find_element(By.ID, "ff_6_Job").send_keys("Engenheiro")

    # Empresa (opcional)
    driver.find_element(By.ID, "ff_6_Company").send_keys("Empresa X")

    # Estado Civil
    estado_civil_dropdown = Select(driver.find_element(By.ID, "ff_6_MaritalStatus"))
    estado_civil_dropdown.select_by_visible_text("Solteiro(a)")

    # Data de Nascimento
    driver.find_element(By.ID, "ff_6_nascimento").send_keys("01/01/1990")

    # CPF
    driver.find_element(By.ID, "ff_6_cpf").send_keys("123.456.789-00")

    # Como conheceu o escritório
    lead_dropdown = Select(driver.find_element(By.ID, "ff_6_lead"))
    lead_dropdown.select_by_visible_text("Google")

    # Enviar o formulário
    driver.find_element(By.CSS_SELECTOR, "button.ff-btn-submit").click()

    # Mensagem de sucesso
    print("Formulário enviado com sucesso!")
except Exception as e:
    print(f"Erro ao preencher o formulário: {e}")
finally:
    # Fechar o navegador após 5 segundos
    time.sleep(5)
    driver.quit()
