from django.conf import settings

lang = settings.LANGUAGE_CODE


def global_texts():
    global lang
    switcher = {
        "pt-br": {
            "Fish_Header_Welcome": "Reserve sua",
            "Fish_Header_SecondPhrase": "Pesca Embarcada",
            "Fishing_Places": "Destinos de pesca",
            "Fishing_Places_2": "mais procurados",
            "Header_Welcome": "Alugar barco",
            "Header_SecondPhrase": "é fácil",
            "Home_cities": "Lugares para navegar mais procurados",
            "Search_Placeholder": "Em qual cidade você quer navegar?",
            "Login_User": "Nome de usuário ou e-mail",
            "Login_Pass": "Senha",
            "Login_Btn": "Entrar",
            "Login_CreateAcc": "Não tem cadastro?",
            "Login_Register": "Cadastre-se",
            "Login_ForgotPass": "Esqueceu a senha?",
            "Login_HasAcc": "Já tem conta?",
            "Login_ClickToLogin": "Clique aqui para entrar",
            "Login_RegisterButton": "Cadastrar",
            "Login_AuthError": "E-mail ou senha incorretos, por favor, tente novamente.",
            "BoatMate_Title": "Temos barcos com saídas programadas para diversos dias, que tal aproveitar a carona?",
            "BoatMate_SubTitle": "Nossos proprietários fazem travessias diariamente com seus barcos, você sabia que pode embarcar em uma delas?",
            "BoatMate_Button": "Confira os destinos",
            "BoatMate_BelowButtonText": "Se você é proprietário e deseja cadastrar sua travessia, ",
            "ClickHere": "clique aqui",
            "NewBoats_Title": "Confira os novos barcos adicionados",
            "Capacity": "Capacidade",
            "CharterPrice": "Diária a partir de R$",
            "People": " por pessoa",
            "Reviews_Title": "Veja os relatos de quem já passou por aqui",
            "AllCities_Title": "Temos barcos em mais de 20 cidades, confira a lista a baixo",
            "boats_view_btitle_partOne": "para até",
            "boats_view_btitle_partTwo": "pessoas",
            "Title": "Bnboats - alugar barcos nunca foi tão fácil",
            "RegisterBoat": "Anuncie seu barco",
            "RegisterBoat_LCase": "Anuncie",
            "Help": "Como funciona",
            "RegisterUser": "Cadastre-se",
            "Login": "Entrar",
            "Guests": "Passageiros",
            "Owners": "Proprietários",
            "Profile": "PERFIL",
            "Profile_full": "MEU PERFIL",
            "Messages": "MENSAGENS",
            "MyBookingsShort": "PASSEIOS",
            "MyBookings_full": "MEUS PASSEIOS",
            "Favorites": "FAVORITOS",
            "MyBoatsShort": "ANÚNCIOS",
            "BookingRequestsShort": "RESERVAS",
            "Exit": "SAIR",
            "Terms": "Termos e condições",
            "FAQ": "Perguntas frequentes",
            "HowItWorks": "Como funciona?",
            "Boatmate": "Travessias/Boatmate",
            "RentABoat": "Alugue um barco",
            "HasLogin": "Já tem conta? Entre aqui",
            "Help_LeftMenu": "AJUDA",
            "RegisterBoat_LeftMenu": "ANUNCIE SEU BARCO",
            "Email": "E-mail",
            "Password": "Entre sua Senha",
            "New_Password": "Crie uma Senha",
            "ConfirmPassword": "Confirme sua senha",
            "UpdatePassword": "Troque sua senha",
            "EmailError": "Por favor, entre seu e-mail",
            "FullName": "Nome completo",
            "MobileCountry": "País",
            "MobileArea": "Área",
            "Mobile": "Celular",
            "FullNameError": "Por favor, entre seu nome completo",
            "MobileCountryError": "Por favor, entre o código do seu país. Ex. +55 para Brasil",
            "MobileAreaError": "Por favor, entre o código de área do seu celular. Ex. 11 para São Paulo",
            "MobileError": "Por favor, entre o seu número de celular",
            "PasswordError": "Por favor, defina uma senha para o seu acesso",
            "ConfirmPasswordError": "Por favor, confirme sua senha digitando-a novamente",
            "CurrentPasswordError": "Por favor, entre sua senha",
            "GenderCheckError": "Por favor, defina seu sexo",
            "CurrentCPFError": "Por favor, entre seu CPF ou Passaporte se for estrangeiro",
            "CurrentCEPError": "Por favor, entre seu CEP e endereço",
            "MobileConfirm_Title": "Enviamos um código de acesso para o número de celular [mobileNo]. Por favor, "
                                   "insira este código abaixo para seguirmos com o cadastro: ",
            "MobileConfirm_Button": "Confirmar",
            "MobileConfirm_SendAgain": "Não recebeu o código? Para enviar novamente ",
            "MobileConfirm_Validated": "Código validado com sucesso.",
            "MobileConfirm_ValidationError": "O código inserido não confere com o enviado. Por favor, tente novamente.",
            "BookingPrice_Single": "Avulso (2 horas)",
            "BookingPrice_HDay": "Meia Diária (4 horas)",
            "BookingPrice_Day": "Diária (8 horas)",
            "BookingPrice_Overnight": "Pernoite (24 horas)",
            "BookNow": "RESERVAR",
            "BoatSize": "Tamanho (em pés)",
            "BoatCapacity": "Capacidade",
            "BoatNoOfRooms": "Quartos",
            "BoatNoOfToilets": "Banheiros",
            "BoatPetAllowed": "Permite PET",
            "BoatSmokeAllowed": "Permite fumar a bordo",
            "BoatFishingId": "Possui registro de pesca",
            "BoatAcessability": "Acessibilidade para PCD",
            "BoatPetrol": "Combustível",
            "BoatSkipper": "Marinheiro",
            "Yes": "Sim",
            "No": "Não",
            "Details": "Detalhes",
            "Amenities": "Comodidades",
            "Captain_Q1": "Qual é a sua relação com o barco que irá anunciar?",
            "Captain_Q2": "Qual é a sua habilitação náutica?",
            "Captain_Q2b": "Defina sua carteira profissional",
            "Captain_Q3": "Quantas milhas já navegou nesse marzão?",
            "Captain_Q4": "Além de navegar, tem mais alguma atividade que desenvolve nas águas?",
            "Captain_Q5": "Em qual(is) dessas línguas você consegue se comunicar?",
            "Captain_Q5a": "(Obs.: Tá valendo aquele inglês de beira de cais)",
            "Captain_Q1_opt1": "Proprietário e capitão",
            "Captain_Q1_opt2": "Apenas proprietário",
            "Captain_Q2_opt1": "Arrais Amador",
            "Captain_Q2_opt2": "Mestre Amador",
            "Captain_Q2_opt3": "Capitão Amador",
            "Captain_Q2_opt4": "Motonauta",
            "Captain_Q2_opt5": "Veleiro",
            "Captain_Q2_opt6": "Carteira Profissional Marítima",
            "Captain_Q3_opt1": "0-100",
            "Captain_Q3_opt2": "101-500",
            "Captain_Q3_opt3": "501-2500",
            "Captain_Q3_opt4": "2501-10.000",
            "Captain_Q3_opt5": "10.000+",
            "BoatType_1": "Veleiro",
            "BoatType_2": "Lancha",
            "BoatType_3": "Pesca",
            "BoatType_4": "Escuna",
            "BoatType_5": "Bote",
            "BoatType_6": "Outros",
            "BoatType_all": "Todos",
            "BoatStatus_10": "Em revisão",
            "BoatStatus_20": "Publicado",
            "BoatStatus_30": "Rejeitado",
            "BoatStatus_40": "Fora do Ar",
            "CaptainSetupMsg": "Capitão, seu cadastro está sendo realizado, por favor aguarde uns instantes...",
            "Next": "Avançar",
            "BookingSingle": "Avulso (2 horas)",
            "BookingHDay": "Meia Diária (4 horas)",
            "BookingDay": "Diária (8 horas)",
            "BookingOvernight": "Pernoite (24 horas)",
        },
        "en": {
        },
    }
    return switcher.get(lang, "Language not found.")


def home_texts():
    global lang
    switcher = {
        "pt-br": {
        },
        "en": {
        },
    }
    return switcher.get(lang, "Language not found.")


def userarea_texts():
    global lang
    switcher = {
        "pt-br": {
            "Male": "Masculino",
            "Female": "Feminino",
            "Others": "Outros",
            "CPF": "CPF",
            "Passport": "Passaporte",
            "Gender": "Eu sou",
            "Dob": "Data de nascimento",
            "Dob_Day": "Dia",
            "Dob_Month": "Mês",
            "Dob_Year": "Ano",
            "Doc_Type": "Documento",
            "Doc_Number": "Número do documento",
            "Address": "Endereço",
            "Address_Street": "Rua",
            "Address_Number": "n°",
            "Address_Postcode": "CEP",
            "Address_Additional": "Compl.",
            "Address_Area": "Bairro",
            "Address_City": "Cidade",
            "Address_State": "Estado",
            "Address_Country": "País",
            "Profile_Desc": "Descreva-se",
            "bank_details": "Conta para Recebimento",
            "bank_name": "Banco",
            "bank_branch": "Ag.",
            "bank_account": "Conta",
            "bank_owner": "Títular da conta",
            "Profile_Desc_pholder": "Tá faltando inspiração? Tudo bem, a gente ajuda! Quais são seus hobbies? "
                                    "Você tem um lema de vida? O que não pode faltar na sua vida?",
            "Jan": "Janeiro",
            "Feb": "Fevereiro",
            "Mar": "Março",
            "Apr": "Abril",
            "May": "Maio",
            "Jun": "Junho",
            "Jul": "Julho",
            "Aug": "Agosto",
            "Sep": "Setembro",
            "Oct": "Outubro",
            "Nov": "Novembro",
            "Dec": "Dezembro",
            "UploadPhotoLink": "Alterar foto",
            "UploadPhotoSuccessfully": "Foto atualizada com sucesso",
            "ProfileUpdatedSuccessfully": "Perfil atualizado com sucesso",
            "Save": "Salvar",
            "Hello": "Olá",
            "Send": "Enviar",
            "TypeMsg": "Digite aqui sua mensagem",
            "CompareFavorites": "Comparar favoritos",
            "Status_10": "Criado",
            "Status_20": "Em processamento",
            "Status_30": "Aguardando pagamento",
            "Status_40": "Aguardando confirmação do proprietário",
            "Status_50": "Confirmado",
            "Status_60": "Cancelado",
            "Status_10a": "Em revisão",
            "Status_20a": "Publicado",
            "Status_30a": "Pausado",
            "Status_40a": "Apagado",
            "Boarding_Place": "Local de embarque",
            "Boarding_Date": "Data",
            "Boarding_Period": "Período",
            "Boarding_PeopleQry": "No de Pessoas",
            "Boarding_Total": "Valor Total",
            "OwnerInfo": "Proprietário",
            "SkipperLicense": "Habilitação náutica",
            "ProfessionalSkipperLicense": "Carteira profissional",
            "Experience": "Experiência (em milhas)",
            "ExtraActivities": "Atividades extras",
            "Languages": "Línguas que fala",
            "BoatReg_Q1": "Capitão, em qual categoria o seu barco se enquadra?",
            "BoatReg_Q2": "Qual o ano de fabricação da embarcação?",
            "BoatReg_Q3": "Qual o nome do fabricante?",
            "BoatReg_Q4": "Qual o tamanho do barco? (em pés)",
            "BoatReg_Q4a": "(1 metro equivale aproximadamente 3 pés)",
            "BoatReg_Q5": "Quantas pessoas está autorizado a levar?",
            "BoatReg_Q5a": "(sem contar com o comandante)",
            "BoatReg_Q6": "Quantas pessoas podem pernoitar?",
            "BoatReg_Q7": "Quantos quartos (camarotes) o barco possui?",
            "BoatReg_Q8": "Aceita animais de estimação?",
            "BoatReg_Q9": "Permite fumar a bordo?",
            "BoatReg_Q10": "Embarcação possui acessibilidade para cadeirantes?",
            "BoatReg_Q11": "Quais comodidades seu barco oferece?",
            "BoatReg_Q12": "Qual endereço de embarque?",
            "BoatReg_Q13": "Adicione até 6 fotos do barco",
            "BoatReg_Q13a": "Fotos que valorizam o barco fazem toda a diferença para seus passageiros. Capriche e terá mais chances de fechar uma reserva! Seguem algumas dicas:",
            "BoatReg_Q13b": "1 - Tire fotos horizontalmente.",
            "BoatReg_Q13c": "2 - Aproveite a luz natural do sol, quando for ambientes internos ligue as luzes para iluminar, evitando usar o Flash.",
            "BoatReg_Q13d": "3 - Valorize a decoração interna da embarcação e a vista do local.",
            "BoatReg_Q13e": "4 - De preferência por fotos onde apareça somente o barco e sua estrutura sem a presença de indivíduos.",
            "BoatReg_Q14": "Título da experiência",
            "BoatReg_Q14b": "Um bom título faz toda a diferença no anúncio (50 caracteres)",
            "BoatReg_Q15": "Descrição da experiência",
            "BoatReg_Q15a": "Diga aos usuários da Bnboats o porquê seu barco é a opção preferida para eles desfrutarem "
                            "de um dia a bordo. Que elementos agregam valor ao seu barco?",
            "BoatReg_Q15b": "Aqui vale tudo, pode contar um pouco da história dele, por onde normalmente navega, "
                            "quais são os lugares incríveis que podem visitar...",
            "BoatReg_Q16": "Preço",
            "BoatReg_Q16a": "Atribua valores aos pacotes de horas que deseja oferecer para aluguel.",
            "BoatReg_Q16b": "Lembre-se que no valor deve ser incluído o custo com marinheiro e combustível.",
            "BoatReg_Q16c": "O valor inserido, será o valor recebido pela experiência. Nenhum desconto de comissionamento será feito sobre este valor.",
            "BoatReg_Q17": "Preços definidos, o que está incluso em cada um deles?",
            "BoatReg_Q18": "Cupom",
            "BoatReg_Q18a": "Você gostaria de oferecer um cupom de ",
            "BoatReg_Q18b": "20% ",
            "BoatReg_Q18c": "de desconto para a ",
            "BoatReg_Q18d": "primeira locação ",
            "BoatReg_Q18e": "que fizer a reserva do seu barco? Isso atrai atenção para o seu barco e aumenta as chances de fazer sua primeira reserva!",
            "BoatReg_Q19": "Bem-vindo a Bnboats!",
            "MultipleChoice": "Mantenha pressionado o 'Control', ou 'Command' no Mac, para selecionar mais de uma opção.",
            "BoatReg_2hours": "2 horas",
            "BoatReg_4hours": "4 horas",
            "BoatReg_8hours": "8 horas",
            "BoatReg_24hours": "Pernoite",
            "BoatReg_final": "Em breve seu barco estará visível para a maior comunidade náutica do Brasil.",
            "BoatReg_finish": "Concluir",
            "BoatReg_Fishing_Q1": "Vimos que sua embarcação tem DNA de pesca. Ajude os pescadores a alugarem seu barco preenchendo essas últimas perguntas referentes a pescaria que você oferece.",
            "BoatReg_Fishing_Q2": "Quais são as regras da pescaria?",
            "BoatReg_Fishing_Q2_opt1": "Permitido somente pesque e solte",
            "BoatReg_Fishing_Q2_opt2": "Permite o abate do peixe para levar",
            "BoatReg_Fishing_Q2_opt3": "Permitido o abate do peixe para consumo no local",
            "BoatReg_Fishing_Q3": "Quais espécies de peixes tem maior probabilidade de serem capturados?",
            "BoatReg_Fishing_Q3_opt1": "Cavala",
            "BoatReg_Fishing_Q3_opt2": "Corvina",
            "BoatReg_Fishing_Q3_opt3": "Dourado",
            "BoatReg_Fishing_Q3_opt4": "Dourado do Mar",
            "BoatReg_Fishing_Q3_opt5": "Esturjão",
            "BoatReg_Fishing_Q3_opt6": "Variado",
            "BoatReg_Fishing_Q3_opts": "Espécies de peixes",
            "BoatReg_Fishing_Q4": "Quais técnicas você usa?",
            "BoatReg_Fishing_Q4_opt1": "Isca Artificial",
            "BoatReg_Fishing_Q4_opt2": "Corrico",
            "BoatReg_Fishing_Q4_opt3": "Fundo",
            "BoatReg_Fishing_Q4_opt4": "Fly",
            "BoatReg_Fishing_Q4_opt5": "Cevadeira",
            "BoatReg_Fishing_Q4_opt6": "Vertical",
            "BoatReg_Fishing_Q5": "Quais são os locais de pesca?",
            "BoatReg_Fishing_Q5_opt1": "Costeira (Inshore)",
            "BoatReg_Fishing_Q5_opt2": "Oceânica (Offshore)",
            "BoatReg_Fishing_Q5_opt3": "Manguezal",
            "BoatReg_Fishing_Q5_opt4": "Parcéis e Arrecifes",
            "BoatReg_Fishing_Q5_opt5": "Naufrágios",
            "BoatReg_Fishing_Q5_opt6": "Rios e Lagos",
            "BoatReg_BoatType_Error": "Por favor, selecione o tipo de embarção antes de seguir",
            "BoatReg_Pet_Error": "Por favor, selecione se você autoriza seus passageiros a leverem seus PETs antes de seguir",
            "BoatReg_Smoke_Error": "Por favor, selecione se é permitido fumar em sua embarcação antes de seguir",
            "BoatReg_Acessability_Error": "Por favor, selecione se sua embarcação possui acessibilidade para cadeirantes antes de seguir",
            "BoatReg_Address_Error": "Por favor, entre o endereço completo onde se encontra sua embarcação antes de seguir",
            "BoatReg_Image_Error": "Por favor, inclua pelo menos 5 fotos da embarcação antes de seguir",
            "BoatReg_Title_Error": "Por favor, inclua o título do anúncio antes de seguir",
            "BoatReg_Description_Error": "Por favor, inclua uma descrição da embarcação antes de seguir",
            "BoatReg_DayPrice_Error": "O preço do aluguel de 8 horas é obrigatório, favor preencher antes de seguir.",
            "BoatReg_Amenities_T1": "Eletrodomésticos",
            "BoatReg_Amenities_T2": "Comodidades",
            "BoatReg_Amenities_T3": "Atividades Aquáticas",
            "BoatReg_Amenities_T4": "Lazer",
            "BoatReg_Amenities_T5": "Acessórios de Pesca",
            "Booking_Review": "Avalie seu passeio",
            "Booking_Grade": "Nota",
            "Booking_Grade_1": "Péssimo",
            "Booking_Grade_2": "Ruim",
            "Booking_Grade_3": "Médio",
            "Booking_Grade_4": "Bom",
            "Booking_Grade_5": "Ótimo",
            "Booking_Comments": "Comentários",
            "MyBoats": "Meus Anúncios",
            "MyBookings": "Meus Passeios",
            "MyBookingRequests": "Reservas",
            "Edit": "Editar",
            "Pause": "Pausar",
            "Delete": "Apagar",
            "People": "pessoas",
        },
        "en": {
        },
    }
    return switcher.get(lang, "Language not found.")


def results_texts():
    global lang
    switcher = {
        "pt-br": {
            "Date": "DATAS",
            "Capacity": "CAPACIDADE",
            "Category": "CATEGORIA",
            "BoatType": "TIPO",
            "More_Filter": "MAIS FILTROS",
            "Nearby_Boats_Call": "Barcos em cidades próximas à ",
            "Filter_Capacity": "Quantas pessoas vão embarcar?",
            "Filter_Dates": "Que dia quer embarcar?",
            "Filter": "Filtrar",
            "Filter_Price": "Quais valores está procurando?",
            "Filter_Price_Single": "Avulso (2 horas)",
            "Filter_Price_Hday": "Meia Diária (4 horas)",
            "Filter_Price_Day": "Preço diária (8 horas)",
            "Filter_Price_Overnight": "Pernoite (24 horas)",
            "Filter_Period_Single": "Avulso",
            "Filter_Period_Hday": "Meia Diária",
            "Filter_Period_Day": "Diária",
            "Filter_Period_Overnight": "Pernoite",
            "Filter_Category": "Quais tipos de embarcações deseja procurar?"
        },
        "en": {
        },
    }
    return switcher.get(lang, "Language not found.")


def how_it_works_texts():
    global lang
    switcher = {
        "pt-br": {
            "How_can_we_help": "Como podemos ajudar?",
            "Tab_owner": "Ajuda para os proprietários",
            "Tab_passengers": "Ajuda para os passageiros",
            "Infos_free_announcement_title": "Anuncie Grátis",
            "Infos_free_announcement_text": "Na Bnboats você poderá anunciar quantos barcos quiser sem nenhum custo. Após aprovação os barcos estarão sempre visíveis para todos os usuários.",
            "Infos_tax_title": "Taxa Zero",
            "Infos_tax_text": "Não cobramos nenhuma taxa de administração do proprietário ou porcentagem do valor sobre seu aluguel",
            "Infos_payment_title": "Pagamento Seguro",
            "Infos_payment_text": "O pagamento é feito em até 5 dias úteis após o passeio pela nossa plataforma. Isso garante a sua segurança e a certeza do recebimento.",
            "Questions_title": "Perguntas frequentes",
            "Questions_owners": [
                {
                    "title": "Seu Anúncio",
                    "img": "media/admin/megafone4.png",
                    "doubts": [
                        {
                            "text": "Como anunciar meu barco?",
                            "answer": "Você pode criar um anúncio clicando em Anuncie seu Barco no canto direito superior ou dentro do seu perfil. Depois que você publicar seu anúncio, pode demorar alguns dias para que ele apareça nos resultados de busca."
                        },
                        {
                            "text": "Quanto custa para anunciar o seu barco?",
                            "answer": "O anúncio de barco na Bnboats é gratuito."
                        },
                        {
                            "text": "Quais fotos devo escolher?",
                            "answer": "As que ajudaram os passageiros a criarem as expectativas certas antes de fazerem uma reserva. <br> Segue algumas dicas para tirar fotos de alta qualidade:",
                            "topics": [
                                "Adicione o número máximo de fotos (ajude os passageiros a entenderem como seria a estadia a bordo)",
                                "Resolução é importante (1024 x 683 px mínimo - na dúvida, as maiores são sempre melhores)",
                                "Tire suas fotos no formato paisagem (horizontal)",
                                "Arrume o ambiente",
                                "Tire fotos durante o dia (acenda as luzes para iluminar seu espaço e evite flashs)",
                                "Destaque comodidades únicas (wakeboard, churrasqueira, equipamento de pesca)"
                            ]
                        },
                        {
                            "text": "O que devo incluir no valor do aluguel?",
                            "answer": "Para tornar o processo mais dinâmico e evitar troca de dinheiro na beira do cais. O valor do aluguel deve incluir marinheiro e combustível."
                        },
                        {
                            "text": "É preciso contabilizar o combustível no valor do aluguel?",
                            "answer": "Sim."
                        },
                        {
                            "text": "Em quanto tempo o anúncio estará no ar?",
                            "answer": "Em média até 5 dias."
                        },
                        {
                            "text": "Já cadastrei meu barco, mas o anúncio ainda não está no ar. Quanto tempo leva?",
                            "answer": "Entre o cadastro e a publicação levamos em média até 5 dias para validar as informações."
                        },
                        {
                            "text": "Como oferecer um desconto?",
                            "answer": "Para enviar uma oferta especial a um passageiro:",
                            "topics": [
                                "Acesse Seu Anúncio na página bnboats.com",
                                "Entre em Anúncios",
                                "Clique no botão Editar embaixo da foto do seu anúncio",
                                "No campo preço altere o valor do charter para o dia em que gostaria de oferecer o desconto.",
                            ]
                        },
                        {
                            "text": "Posso alugar meu barco somente por algumas horas?",
                            "answer": "Sim. Indicamos a todos proprietários de barcos oferecer além do aluguel de 8 horas, o aluguel de 2 e 4 horas."
                        },
                        {
                            "text": "Vale a pena alugar o barco por horas?",
                            "answer": "Sim. Barcos com a modalidade de aluguel por horas têm 92% mais chances de serem reservados"
                        },
                        {
                            "text": "Posso disponibilizar meu barco para aluguel por uma semana inteira?",
                            "answer": "Sim."
                        },
                        {
                            "text": "Posso alterar o preço do meu barco depois da intenção de aluguel de um usuario?",
                            "answer": "Você tem total liberadade de alterar o preço do aluguel na plataforma quando quiser."
                        },
                        {
                            "text": "Como fazer o cancelamento de uma reserva confirmada?",
                            "answer": "Conecte-se a sua conta, clicando em 'Entrar' no canto direito superior. Depois clique em 'Solicitações de Reserva'. Procure a reserva e clique no botão 'Cancelar Reserva'.<br> O usuário interessado irá receber uma notificação a respeito do cancelamento.",
                        },
                        {
                            "text": "Recebi um SMS, dizendo que tem um interessado em alugar minha embarcação, que me fez uma pergunta. Como eu respondo?",
                            "answer": "Ao clicar no link enviado pelo SMS, você será direcionado para a página de Mensagens. Responda aos questionamentos do interessado e depois clique em Enviar. Quanto mais detalhes maiores são as chances dele fechar a reserva no seu barco."
                        },
                        {
                            "text": "Por que não consigo visualizar meu barco anunciado?",
                            "answer": "Verifique se preencheu corretamente tudo no formulário de inscrição e se enviou pelo menos uma foto. <br> Quando estiver na sua conta, clique em 'Meus anúncios' e verifique se está escrito 'Publicado' ou 'Aguardando Aprovação'.<br> Seu barco é publicado quando:",
                            "topics": [
                                "Seu endereço de e-mail é validado ",
                                "O seu perfil está completo: nome, sobrenome, número de telefone, data de nascimento ",
                                "Você enviou pelo menos uma foto da sua embarcação",
                                "E o valor pelo serviço foi indicado",
                            ],
                            "postopics": "Se você verificou que todos esses dados foram inseridos corretamente e o status do seu barco ainda está na condição “Aguardando Aprovação”, envie-nos um e-mail para contato@bnboats.com. Um membro da nossa equipe entrará em contato com você o mais breve possível."
                        },
                        {
                            "text": "Tenho uma operadora de turismo, posso registrar meus barcos mesmo assim?",
                            "answer": "Sim. Aceitamos barcos de operadoras se as seguintes condições forem respeitadas:",
                            "topics": [
                                "Os preços exibidos na Bnboats forem menores ou iguais aos preços exibidos em seu website ou em sua agência / escritório",
                                "Sua empresa ou site não pode ser mencionado em nenhum momento: seja na descrição, fotos ou na troca de mensagens com potencias locatários."
                            ]

                        },
                        {
                            "text": "Como faço a verificação do meu número de telefone?",
                            "answer": "Ao clicar em cadastrar na página inicial, digite seu número de telefone no campo indicado.<br>Digite seu código de país (e.g. +55) área (e.g. 11) e número de telefone<br>Clique em Cadastrar  Vamos enviar um código por SMS.<br>Cadastre seu código e clique em Confirmar.  *Seu número só será compartilhado com proprietário de barco quando você tiver uma reserva confirmada."
                        },
                        {
                            "text": "Como fazer a verificação do meu email?",
                            "answer": "Ao clicar em cadastrar na página inicial, digite seu email no campo indicado.<br>Clique em Cadastrar  . Vamos enviar um email de confirmação para seu email.  Entre no seu email, abra a mensagem da Bnboats e clique em confirmar."
                        },
                    ]
                },
                {
                    "title": "A Bordo",
                    "img": "media/admin/boat.png",
                    "doubts": [
                        {
                            "text": "O que será apresentado pelo passageiro na hora de embarcar?",
                            "answer": "Quando você confirma uma reserva, o passageiro recebe um email com todos os detalhes da compra: número da reserva, nome do barco, data do passeio, etc. Ele vai imprimir e levar ou mostrar na tela do celular na hora do embarque."
                        },
                        {
                            "text": "O que fazer caso os passageiros não apareçam no dia e hora reservados?",
                            "answer": "Enviar um email para contato@bnboats.com com o título 'Cancelamento por não Comparecimento' e no corpo de texto apresentar a hora e local combinado."
                        },

                    ]
                },
                {
                    "title": "Pagamento",
                    "img": "media/admin/cartao1.png",
                    "doubts": [
                        {
                            "text": "Quais são as comissões cobradas pela BnBoats?",
                            "answer": "Nenhum desconto de comissionamento será feito sobre o proprietário. <br>"
                                      "Para ajudar com a operação da plataforma, uma taxa de 13,5% serviço é cobrada "
                                      "apenas do usuário quando uma reserva é confirmada."
                        },
                        {
                            "text": "Quando vou receber o dinheiro pelos serviços vendidos aqui?",
                            "answer": "Em até 5 dias úteis após a realização do passeio."
                        },
                        {
                            "text": "Como vou receber o dinheiro pelos serviços vendidos através do BnBoats?",
                            "answer": "Na conta corrente cadastrada em seu perfil."
                        },
                        {
                            "text": "Se o locatário cancelar o aluguel, eu ainda receberei o valor?",
                            "answer": "Se o locatário não comparecer ou cancelar no dia do passeio, você ainda receberá o pagamento integral.  <br> Se o mesmo cancelar uma reserva antecipadamente, as políticas de cancelamento selecionadas serão aplicadas:  <br>",
                            "topics": [
                                "Em até 5 dias corridos antes do passeio, não irá haver nenhuma penalidade.",
                                "Dentro dos 5 dias antes do passeio, além do valor integral do passeio ele pagará multa de 10% sobre o valor do aluguel a você"
                            ],
                            "postopics": "Um cancelamento de reserva devido a condições meteorológicas permitirá que o locatário receba o valor total pago pela reserva, excluindo a taxa de serviço Bnboats."
                        },

                    ]
                },
                {
                    "title": "Sua Conta",
                    "img": "media/admin/navigate.jpg",
                    "doubts": [
                        {
                            "text": "Como faço para reclamar por danos na embarcação ou utilização incorreta de produtos ou serviços não descritos no meu anúncio, produzidos pelos passageiros?",
                            "answer": "Antes do desembarque dos usuários, o dono e o marinheiro deve conferir o estado da embarcação, e, se foi o combinado, fazer as contas das despesas com combustível, marinas, ancoradouros, restaurantes, marinheiros, alimentação e bebidas a bordo, dentre outros. Se entender que precisa solicitar algum tipo de reembolso ou ressarcimento, deve tentar chegar a um acordo diretamente com o usuário. Se o proprietário percebe algum problema após o desembarque dos usuários, a Bnboats oferece um sistema de Disputas para atender essas reclamações. O prazo para abrir uma Disputa é de até 3 dias (72 horas) após o desembarque dos usuários. Depois desse prazo, o comportamento dos usuários, seu cuidado com o barco e consumação de produtos e serviços a bordo, dentre outros, serão considerados satisfatórios e não será mais possível fazer reclamação sobre o mesmo charter, viagem ou passeio. Para iniciar uma Disputa, o dono ou operador da embarcação deve enviar um e-mail para contato@bnboats.com, com todas as informações disponíveis sobre o problema, número da reserva, nome do usuário e titular da compra, descrição da situação, fotos e vídeos, dentre outros. Assim que a reclamação for enviada, a Bnboats será o “mediador” entre o dono e o usuário, atendendo aos argumentos das duas partes. Após análise, Bnboats tomará uma decisão e comunicará o resultado às partes envolvidas, solicitando um ressarcimento em dinheiro ao usuário (anexando orçamentos) ou não solicitando indenização nenhuma, segundo a decisão, que é inapelável e tomada atendendo aos preceitos de imparcialidade, exaustivo processamento das informações disponíveis, argumentos, senso comum e justiça."
                        },
                        {
                            "text": "É preciso colocar foto no perfil?",
                            "answer": "Não é obrigatório, mas aumentam as chances de reserva, quanto mais completo é um cadastro mais confiança o usuário tem no anuncio."
                        },
                        {
                            "text": "Como faço para cancelar uma reserva já confirmada?",
                            "answer": "Conecte-se a sua conta, clicando em “Entrar” no canto direito superior. Depois clique em “Solicitações de Reserva”. <br> Procure a reserva e clique no botão “Cancelar Reserva”. O usuário que estava interessado no aluguel vai receber uma notificação via email com a informação do cancelamento. As Políticas de Cancelamento serão aplicadas segundo o prazo em que o usuário ou o anunciante do barco cancela a reserva realizada. Elas valem para todas as embarcações cadastradas e existem para proteger tanto os usuários quanto o proprietário do barco. Confira nossas políticas de cancelamento aqui."
                        },
                        {
                            "text": "O que fazer em caso de mau tempo?",
                            "answer": "Em caso de condições climáticas que não permitam uma navegação com segurança, cancele a reserva em até 2 horas antes do início do aluguel em Solicitações de Reservas. E depois clique em 'Cancelar minha Reserva'. O proprietário deverá reagendar nova data com o usuário para realização do passeio, sem alteração nas condições ajustadas."
                        },
                        {
                            "text": "Eu posso trocar telefone com o interessado em alugar meu barco?",
                            "answer": "O sistema de mensagens Bnboats permite apenas discutir questões e detalhes da reserva.<br> Assim que sua reserva for confirmada, você poderá compartilhar as informações de contato com o locatário (e-mail e número de telefone)."
                        },
                        {
                            "text": "Meu barco foi alugado, mas eu não recebi nenhum comentário. O que eu faço?",
                            "answer": "Convidamos você a enviar uma mensagem para o locatário através do sistema de mensagens do Bnboats, solicitando que ele envie um comentário. Para fazer isso, acesse sua conta e clique em “Mensagens”, selecione a conversa com o usuário em questão e faça a solicitação."
                        },
                        {
                            "text": "Como posso deixar minha avaliação sobre um passageiro?",
                            "answer": "Você pode deixar um comentário e dar uma avaliação sobre um locatário acessando dentro da sua conta o link “Passeios”. Depois é só clicar em “Você pode avaliar agora” e escrever seu comentário."
                        },
                        {
                            "text": "O que fazer caso um passageiro danifique meu barco?",
                            "answer": ""
                        },
                        {
                            "text": "Por que eu devo pagar e me comunicar somente via a plataforma da Bnboats?",
                            "answer": "Pagar e se comunicar através da Bnboats ajuda a garantir que você "
                                      "esteja protegido pelos nossos Termos de Serviço, Políticas de Privacidade, "
                                      "cancelamento e reembolso e outros recursos de segurança. Isso também facilita "
                                      "encontrar e consultar detalhes importantes de uma reserva e outras informações "
                                      "úteis. Nós não temos como oferecer esses benefícios quando as reservas não são "
                                      "feitas e pagas diretamente através da Bnboats. <br>Fazer pagamentos ou se "
                                      "comunicar fora da Bnboats também dificulta a proteção das suas informações, "
                                      "aumentando seu risco de ser vítima de fraude e de outros problemas de segurança."
                        },

                    ]
                }
            ],
            "Questions_passengers": [
                {
                    "title": "Sua Reserva",
                    "img": "media/admin/megafone4.png",
                    "doubts": [
                        {
                            "text": "Como eu reservo um barco?",
                            "answer": "Você pode reservar computador, celular ou tablet para reservar uma embarcação.",
                            "topics": [
                                "Ao abrir a página inicial, digite a cidade em que quer realizar o aluguel.",
                                "Escolha um barco entre a série de opções disponíveis na região.",
                                "Na página do barco clique em reserva."
                            ],
                            "postopics": "Obs: Se tiver alguma dúvida com relação ao barco, você pode encaminhar seu questionamento clicando no botão “Fale com o Capitão”."
                        },
                        {
                            "text": "Como faço para saber se o barco está disponível?",
                            "answer": "Ao inserir seu destino e a data de interesse para o aluguel, todos os barcos que surgirem como resultado da busca devem estar disponíveis para sua viagem.<br>Embora incentivemos fortemente todos os capitães a manterem seus calendários atualizados, recomendamos enviar uma mensagem ao capitão do barco em questão para se certificar da disponibilidade. Você também pode enviar uma mensagem ao capitão para perguntar outros detalhes sobre a embarcação."
                        },
                        {
                            "text": "Qual a idade mínima para fazer uma reserva?",
                            "answer": "18 anos.",
                        },
                        {
                            "text": "O que está incluso no valor do aluguel do barco?",
                            "answer": "Combustível e os o serviços do capitão."
                        },
                        {
                            "text": "Todos os barcos incluem combustível e o serviços do capitão?",
                            "answer": "Sim."
                        },
                        {
                            "text": "Como saber se minha reserva foi aceita e está confirmada?",
                            "answer": "Você receberá notificação pelo email e pelo celular. Outra forma é entrando em sua conta e acesso o menu Minhas Reservas."
                        },
                        {
                            "text": "Como fazer quando a embarcação não tem capacidade para o número de pessoas que irão no passeio?",
                            "answer": "Alugar duas embarcações menores. Por questões de segurança o capitão não pode lotar o barco com um número maior de pessoas."
                        },
                        {
                            "text": "Eu tenho carteira de habilitação, posso alugar um barco sem marinheiro?",
                            "answer": "Não."
                        },
                        {
                            "text": "Não quero passar o dia inteiro a bordo, posso alugar só por algumas horas?",
                            "answer": "Sim.<br> Boa parte das embarcações realizam aluguéis por horas, para saber se o barco que você tem interesse em alugar oferece esta opção basta checá-la se está disponível na página da embarcação."
                        },
                        {
                            "text": "É possível passar uma semana a bordo?",
                            "answer": "Sim, desde que as datas estejam disponíveis."
                        },
                        {
                            "text": "Como consigo me conectar diretamente com o capitão?",
                            "answer": "Dentro da página do barco, ao clicar 'Fale com o capitão' você poderá enviar seus questionamentos. Depois de efetuada a reserva você receberá um email com o telefone dele para agilizar a comunicação."
                        },
                        {
                            "text": "Como funcionam os comentários?",
                            "answer": "Todos os comentários na Bnboats são escritos por capitães e passageiros da nossa comunidade.<br>Os comentários são publicados depois do capitão e passageiro concluirem suas avaliações e escreverem seus comentários.",
                        },
                        {
                            "text": "Posso pegar a lancha numa cidade e desembarcar em outra?",
                            "answer": "Sim, para se certificar se a embarcação que tem interesse em alugar realiza travessias, pergunte ao Capitão, clicando no botão 'Fale com o Capitão' descrevendo o itinerário que gostaria de realizar."
                        },
                        {   "text": "Posso dormir a bordo?",
                            "answer": "Sim. Para se certificar se a embarcação que tem interesse em alugar oferece pernoite, cheque no campo da reserva se mostra a opção 'Pernoite'.",
                        },
                        {
                            "text": "Posso levar crianças?",
                            "answer": "Consulte o capitão.",
                        },
                        {
                            "text": "Posso levar meu animal de estimação?",
                            "answer": "Verificar se o capitão da embarcação permite pets a bordo.",
                        },
                        {
                            "text": "Como posso fazer um cancelamento da minha reserva?",
                            "answer": "Entre em sua conta, clique em menu 'Minhas Reservas' e clique em 'Cancelar Reserva'.",
                        },
                    ]
                },
                {
                    "title": "Meu Passeio",
                    "img": "media/admin/boat.png",
                    "doubts": [
                        {
                            "text": "Como faço para embarcar?",
                            "answer": "Após a confirmação da reserva, você receberá um email com as informações referente ao local de embarque e contato do capitão. Assim que possível entre em contato com ele para organizar a hora do embarque e sanar qualquer dúvida que possa ter com relação ao passeio."
                        },
                        {
                            "text": "O que eu preciso levar no dia do passeio?",
                            "answer": "Documento com foto e voucher (impresso ou no celular) com o número da reserva para apresentar ao capitão."
                        },
                        {
                            "text": "O acesso a marina é tranquilo?",
                            "answer": "Por questões de segurança, as marinas só permitem o acesso de pessoas, que tiveram seus seus nomes e RG encaminhados pelo proprietário da embarcação. Para evitar complicações na entrada, responda prontamente as perguntas do capitão, depois de fechar a reserva."
                        },
                        {
                            "text": "Posso fazer churrasco a bordo?",
                            "answer": "Se certificar com o proprietário."
                        },
                        {
                            "text": "O que acontece em caso de condições climáticas severas (tempestades, ventania) no  dia do embarque?",
                            "answer": "Qualquer condição climática que não comprometa o passeio, não será motivo para cancelamento.<br>Em caso de condições climáticas severas, segundo os padrões internacionais de navegação e meteorologia, o capitão será obrigado a agendar nova data com o usuário para realização do passeio, sem alteração nas condições ajustadas, salvo desistência do usuário, neste caso as taxas de transação não serão reembolsadas.<br>Se as condições meteorológicas não permitirem navegar com segurança, converse com o proprietário do barco, você pode cancelar a reserva até 1 hora antes do início do contrato de aluguel acessando “Passeios”. Depois clique em “Cancelar minha reserva”. Pediremos ao proprietário do barco para confirmar e realizaremos o reembolso do valor da reserva, excluindo a taxa de serviço da Bnboats. O reembolso estará na forma de crédito em nosso site, válido por um ano. Você também pode acordar com o proprietário do barco e alterar a data do aluguel."
                        },
                        {
                            "text": "Como escrevo um comentário sobre o capitão?",
                            "answer": "Para deixar um comentário sobre uma saída recente, acesse seu Perfil e depois Minhas Reservas."
                        },

                    ]
                },
                {
                    "title": "Pagamento",
                    "img": "media/admin/cartao1.png",
                    "doubts": [
                        {
                            "text": "Posso parcelar o valor da minha reserva?",
                            "answer": "Sim"
                        },
                        {
                            "text": "Quais são as formas de pagamento?",
                            "answer": "Cartão de Crédito<br>Boleto Bancário"
                        },
                        {
                            "text": "Qual é a taxa de serviço cobrada pela Bnboats? ",
                            "answer": "Para ajudar com a operação da plataforma, uma taxa de 13,5% serviço é cobrada de quem aluga quando uma reserva é confirmada.",
                        },

                    ]
                },
                {
                    "title": "Sua Conta",
                    "img": "media/admin/navigate.jpg",
                    "doubts": [
                        {
                            "text": "Como fazer meu cadastro?",
                            "answer": "Clique em Cadastrar na canto direito superior da página inicial. Digite o seu Nome, Email, Telefone, Senha. Valide seu telefone com o código que será enviado via SMS para seu celular.   pronto você está cadastrado."
                        },
                        {
                            "text": "Por que preciso verificar o telefone e o email?",
                            "answer": "Ter o email e o telefone confirmado é importante para garantir uma comunicação segura com você."
                        },
                        {
                            "text": "Como faço a verificação do meu número de telefone?",
                            "answer": "Ao clicar em cadastrar na página inicial, digite seu número de telefone no campo indicado.<br>Digite seu código de país (e.g. +55) área (e.g. 11) e número de telefone<br>Clique em Cadastrar  Vamos enviar um código por SMS.<br>Cadastre seu código e clique em Confirmar.  *Seu número só será compartilhado com proprietário de barco quando você tiver uma reserva confirmada."
                        },
                        {
                            "text": "Como fazer a verificação do meu email?",
                            "answer": "Ao clicar em cadastrar na página inicial, digite seu email no campo indicado.<br>Clique em Cadastrar  . Vamos enviar um email de confirmação para seu email.  Entre no seu email, abra a mensagem da Bnboats e clique em confirmar."
                        },
                        {
                            "text": "Por que eu não recebi um email de confirmação?",
                            "answer": "Caso não tenha recebido uma notificação que enviamos por email, você pode tentar algumas coisas para tentar resolver o problema.",
                            "topics": [
                                "Verifique se o seu endereço de email está correto",
                                "Busque por todas as mensagens na sua caixa de entrada",
                                "Verifique sua caixa de spam e outros filtros de email (É possível que seu provedor de email tenha enviado nossas mensagens para sua caixa de spam ou lixeira por engano. Para evitar que isso aconteça remova as mensagens da Bnboats da sua lista de spam."
                            ]
                        },
                        {
                            "text": "Como funcionam os comentários?",
                            "answer": "Todos os comentários são escritos por capitães e passageiros da comunidade Bnboats.<br>Os comentários são publicados depois do capitão e passageiro concluirem suas avaliações e escrevem seus comentários."
                        },
                        {
                            "text": "Como fazer uma reclamação?",
                            "answer": "Envie um email para contato@bnboats.com"
                        },
                        {
                            "text": "Por que eu devo pagar e me comunicar somente via a plataforma da Bnboats?",
                            "answer": "Pagar e se comunicar através da Bnboats ajuda a garantir que você "
                                      "esteja protegido pelos nossos Termos de Serviço, Políticas de Privacidade, "
                                      "cancelamento e reembolso e outros recursos de segurança. Isso também facilita "
                                      "encontrar e consultar detalhes importantes de uma reserva e outras informações "
                                      "úteis. Nós não temos como oferecer esses benefícios quando as reservas não são "
                                      "feitas e pagas diretamente através da Bnboats. <br>Fazer pagamentos ou se "
                                      "comunicar fora da Bnboats também dificulta a proteção das suas informações, "
                                      "aumentando seu risco de ser vítima de fraude e de outros problemas de segurança."
                        },

                    ]
                }
            ]
        },
        "en": {
        }
    }
    return switcher.get(lang, "Language not found.")


def bview_texts():
    global lang
    switcher = {
        "pt-br": {
            "People": "pessoas",
            "Bathroom": "banheiro(s)",
            "Cabin": "cabine(s)",
            "Description": "Descrição",
            "Amenities": "Comodidades",
            "SpeakWithCaptain": "Clique e fale com o Capitão",
            "PricePDay": "por diária (aprox. 8 horas)",
            "GasSkipperIncluded": "*Combustível e marinheiro inclusos",
            "BookingTypePriod": "Tempo de passeio",
            "BookingDates": "Escolha a data",
            "BookingPassengers": "Passageiros",
            "BookingPassengers_lc": "passageiros",
            "BookingPassenger_lc": "passageiro",
            "Continue": "Continuar",
            "BookingStartMsg": "Você ainda não será cobrado",
            "Availability": "Disponibilidade",
            "Comments": "comentários",
            "Total": "TOTAL:",
            "PaymentChoice": "Escolha o método de pagamento",
            "PrintBoleto": "Imprimir Boleto",
            "SendBoletoEmail": "Enviar por e-mail",
            "Send": "Enviar",
            "TypeEmail": "Entre seu e-mail e clique enviar",
            "Card_Name": "Nome impresso no cartão",
            "Card_No": "Número do cartão",
            "Card_MM": "Mês",
            "Card_YY": "Ano",
            "Card_Code": "CVV",
            "Pay": "Finalizar",
            "CaptainChat": "Está com dúvidas sobre a embarcação? Sem problemas, envie agora uma mensagem para o "
                           "proprietário e em seguida acompanhe a resposta no menu MENSAGENS.",
        },
        "en": {
        },
    }
    return switcher.get(lang, "Language not found.")

