class AstreaNewClient:
    def __init__(
            self,
            contact_name="",
            contact_nickname="",
            phone="",

            email="",
            website="",

            zip_code="",
            street="",
            number="",
            neighborhood="",
            complement="",
            city="",
            state="",
            country="",
            job="",
            economic_activity_code="",
            marital_status="",
            birth_day="",
            birth_month="",
            birth_year="",
            homeland="",
            cpf="",
            rg="",
            ctps="",
            benefit_document="",
            voter_document="",
            driver_license="",
            passport=""
    ):
        # Atributos de dados pessoais
        self.contact_name = contact_name
        self.contact_nickname = contact_nickname
        self.phone = phone

        self.email = email
        self.website = website

        self.zip_code = zip_code
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement
        self.city = city
        self.state = state
        self.country = country

        # Atributos de dados adicionais
        self.job = job
        self.economic_activity_code = economic_activity_code
        self.marital_status = marital_status
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
        self.homeland = homeland

        # Atributos de documentação
        self.cpf = cpf
        self.rg = rg
        self.ctps = ctps
        self.benefit_document = benefit_document
        self.voter_document = voter_document
        self.driver_license = driver_license
        self.passport = passport