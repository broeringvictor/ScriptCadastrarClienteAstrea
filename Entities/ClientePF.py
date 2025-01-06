class ClientePF:
    def __init__(self,
                 id: str,
                 contact_name: str,
                 contact_nickname: str,
                 phone: str,
                 email: str,
                 website: str,
                 zip_code: str,
                 street: str,
                 number: str,
                 neighborhood: str,
                 complement: str,
                 city: str,
                 state: str,
                 country: str,
                 job: str,
                 company: str,
                 marital_status: str,
                 birth_date: str,  # Data de nascimento completa no formato YYYY-MM-DD
                 homeland: str,
                 cpf: str,
                 rg: str,
                 ctps: str,
                 benefit_document: str,
                 voter_document: str,
                 driver_license: str,
                 passport: str):
        # Informações de Contato
        self.id = id
        self.contact_name = contact_name
        self.contact_nickname = contact_nickname
        self.phone = phone
        self.email = email
        self.website = website

        # Endereço
        self.zip_code = zip_code
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement
        self.city = city
        self.state = state
        self.country = country

        # Dados Adicionais
        self.job = job
        self.company = company
        self.marital_status = marital_status
        self.birth_date = birth_date  # Armazena a data de nascimento completa no formato YYYY-MM-DD
        self.birth_day = None  # Será preenchido depois
        self.birth_month = None  # Será preenchido depois
        self.birth_year = None  # Será preenchido depois
        self.homeland = homeland

        # Documentos
        self.cpf = cpf
        self.rg = rg
        self.ctps = ctps
        self.benefit_document = benefit_document
        self.voter_document = voter_document
        self.driver_license = driver_license
        self.passport = passport

        # Processar a data de nascimento e preencher os atributos de dia, mês e ano
        self.process_birth_date()

    def process_birth_date(self):
        """
        Processa a data de nascimento no formato YYYY-MM-DD e atribui os valores de dia, mês e ano.
        """
        try:
            if self.birth_date:
                year, month, day = self.birth_date.split("-")
                self.birth_day = day.zfill(2)  # Garantir 2 dígitos no dia
                self.birth_month = month.zfill(2)  # Garantir 2 dígitos no mês
                self.birth_year = year
                print(
                    f"Data de nascimento processada: Dia={self.birth_day}, Mês={self.birth_month}, Ano={self.birth_year}")
            else:
                print("Data de nascimento está vazia ou inválida.")
        except Exception as e:
            print(f"Erro ao processar a data de nascimento: {e}")

    def __str__(self):
        """
        Retorna uma representação textual amigável do objeto ClientePessoaFisica.
        """
        return f"{self.contact_name} ({self.cpf}) - {self.city}, {self.state}"


if __name__ == "__main__":
    # Exemplo do método __str__ em ação:
    cliente = ClientePF(
        id=1,
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
        job="Analista de Sistemas",
        company="TechCorp",
        marital_status="Solteiro",
        birth_date="1990-06-15",  # Data no formato YYYY-MM-DD
        homeland="Brasil",
        cpf="123.456.789-10",
        rg="12.345.678-9",
        ctps="12345678",
        benefit_document="345678910",
        voter_document="123456789123",
        driver_license="AB123456",
        passport="AB12345678"
    )

    print(cliente)  # Resultado: João Silva (123.456.789-10) - São Paulo, SP