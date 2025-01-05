import undetected_chromedriver as uc

class WebDriverManager:
    def __init__(self, options=None):
        """Inicializa o WebDriver com opções configuráveis."""
        self.options = options
        self.driver = None

    def start_driver(self):
        """Inicializa o driver com as opções fornecidas."""
        try:
            self.driver = uc.Chrome(options=self.options)
            print("Driver iniciado com sucesso!")
        except Exception as e:
            print(f"Erro ao iniciar o driver: {e}")
            self.driver = None

    def get_driver(self):
        """Retorna o driver atual."""
        if not self.driver:
            raise RuntimeError("Driver não foi inicializado. Use start_driver primeiro.")
        return self.driver

    def cleanup(self):
        """Garante que o driver seja encerrado corretamente."""
        if self.driver:
            try:
                print("Encerrando o WebDriver...")
                self.driver.quit()
            except Exception as e:
                print(f"Erro ao encerrar o WebDriver: {e}")
            finally:
                self.driver = None
        else:
            print("Nenhum driver ativo para encerrar.")

    def __del__(self):
        """Chama o cleanup automaticamente ao destruir a instância."""
        self.cleanup()
