from AdicionarContato.AstreaAdditional import AstreaAdditional  # Certifique-se de que esta classe foi salva corretamente

# Script Principal de Teste
try:
    from AdicionarContato.LoginAstrea import LoginAstrea  # Classe responsável pelo login

    # Inicializa o WebDriver e realiza o login
    login_astrea = LoginAstrea()  # Certifique-se de que a classe LoginAstrea já inicializa corretamente o driver Selenium
    login_astrea.login()  # Realiza o login
    LoginAstrea.iniciar_driver()
    print("Login realizado com sucesso. Acessando página de teste...")

    # Usa o WebDriver obtido após o login para instanciar a classe AstreaAdditional
    formulario = AstreaAdditional(login_astrea.driver)

    # Configura os valores para os campos do formulário
    formulario.job = "Engenheiro de Software"
    formulario.economic_activity_code = "7540"
    formulario.marital_status = "Casado"
    formulario.birth_day = "12"
    formulario.birth_month = "Fevereiro"
    formulario.birth_year = "1990"

    # Preenche o formulário com os valores configurados
    formulario.preencher_formulario()
    print("Formulário preenchido e teste concluído. Verifique os dados no navegador.")

except Exception as e:
    print(f"Erro ao executar o script de teste: {e}")
finally:
    # Fecha o navegador após o teste, se necessário
    if 'login_astrea' in locals() and login_astrea.driver:
        login_astrea.driver.quit()
        print("Navegador fechado.")