from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .views_texts import global_texts, userarea_texts
from .models import UserProfile, get_member_upload_to, Message, CaptainProfile, CaptainExtraActivities, \
    CaptainLanguages, BoatImages, Boat
import datetime


class SignInForm(AuthenticationForm):
    data = {}
    data.update(global_texts())

    username = forms.CharField(max_length=200, required=True, widget=forms.EmailInput(attrs={
        'placeholder': data['Email'], 'class': 'form-control', 'autocomplete': 'email',
        'oninvalid': 'this.setCustomValidity('+"'"+data['EmailError']+"'"+')',
        "oninput": "this.setCustomValidity('')"}), label='')

    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': data['Password'], 'class': 'form-control', 'autocomplete': 'current-password',
        'oninvalid': 'this.setCustomValidity("'+data['CurrentPasswordError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    class Meta:
        model = User
        fields = ('username', 'password', )


class SignUpForm(UserCreationForm):
    data = {}
    data.update(global_texts())

    fishing_client = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Indicação de qual loja', 'class': 'form-control hideOnly'}), label='')

    first_name = forms.CharField(max_length=90, required=True, widget=forms.TextInput(attrs={
        'placeholder': data['FullName'], 'class': 'form-control', 'autocomplete': 'name',
        'oninvalid': 'this.setCustomValidity("'+data['FullNameError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    username = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={
        'placeholder': data['Email'], 'class': 'form-control', 'autocomplete': 'email',
        'oninvalid': 'this.setCustomValidity("'+data['EmailError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    mobile_country = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
        'placeholder': data['MobileCountry'], 'class': 'form-control onlyNumbers', 'maxlength': '4', 'value': '+55',
        'style': 'width: 20%;margin-right: 5%;float: left;', 'autocomplete': 'tel-country-code',
        'oninvalid': 'this.setCustomValidity("'+data['MobileCountryError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    mobile_area = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
        'placeholder': data['MobileArea'], 'class': 'form-control onlyNumbers', 'maxlength': '3',
        'style': 'width: 20%;margin-right: 5%;float: left;', 'autocomplete': 'tel-area-code',
        'oninvalid': 'this.setCustomValidity("'+data['MobileAreaError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    mobile_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
        'placeholder': data['Mobile'], 'class': 'form-control onlyNumbers', 'maxlength': '9',
        'style': 'float: left;width: 50%;', 'autocomplete': 'tel',
        'oninvalid': 'this.setCustomValidity("'+data['MobileError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': data['New_Password'], 'class': 'form-control', 'autocomplete': 'new-password',
        'oninvalid': 'this.setCustomValidity("'+data['PasswordError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': data['ConfirmPassword'], 'class': 'form-control', 'autocomplete': 'new-password',
        'oninvalid': 'this.setCustomValidity("'+data['ConfirmPasswordError']+'")',
        "oninput": "this.setCustomValidity('')"}), label='')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'mobile_country', 'mobile_area', 'mobile_number', 'password1', 'password2', 'fishing_client')


class UploadUserPhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'onchange': 'UploadPhoto()'}))

    class Meta:
        model = UserProfile
        fields = ('image', )


class UserareaUpdateUserForm(forms.ModelForm):
    texts = {}
    texts.update(global_texts())

    first_name = forms.CharField(label=texts['FullName'], required=True, widget=forms.TextInput(attrs={
        'placeholder': '', 'class': 'form-control', 'autofocus': '', 'autocomplete': 'name',
        'oninvalid': 'this.setCustomValidity("'+texts['FullNameError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    username = forms.EmailField(label=texts['Email'], widget=forms.EmailInput(attrs={
        'placeholder': '', 'class': 'form-control', 'autocomplete': 'email',
        'oninvalid': 'this.setCustomValidity("'+texts['EmailError']+'")',
        "oninput": "this.setCustomValidity('')"}))

    class Meta:
        model = User
        fields = ('first_name', 'username')


class UserareaUpdateProfileForm(forms.ModelForm):
    texts = {}
    texts.update(userarea_texts())
    texts.update(global_texts())

    now = datetime.datetime.now()
    last_year = now.year - 2
    first_year = now.year - 100

    GENDER_CHOICES = (('M', texts['Male']), ('F', texts['Female']), ('O', texts['Others']))
    DOC_TYPES = [('CPF', texts['CPF']), ('Passport', texts['Passport']), ('CNPJ', 'CNPJ')]
    DOB_MONTHS = (('01', texts['Jan']), ('02', texts['Feb']), ('03', texts['Mar']), ('04', texts['Apr']),
                ('05', texts['May']), ('06', texts['Jun']), ('07', texts['Jul']), ('08', texts['Aug']),
                ('09', texts['Sep']), ('10', texts['Oct']), ('11', texts['Nov']), ('12', texts['Dec']))
    BANKS_LIST = (('1','BANCO DO BRASIL S.A (BB)'),('237','BRADESCO S.A'),('260','NU PAGAMENTOS S.A (NUBANK)'),('290','Pagseguro Internet S.A'),('323','Mercado Pago - conta do Mercado Livre'),('237','NEXT BANK (UTILIZAR O MESMO CÓDIGO DO BRADESCO)'),('637','BANCO SOFISA S.A (SOFISA DIRETO)'),('77','BANCO INTER S.A'),('341','ITAÚ UNIBANCO S.A'),('104','CAIXA ECONÔMICA FEDERAL (CEF)'),('33','BANCO SANTANDER BRASIL S.A'),('212','BANCO ORIGINAL S.A'),('756','BANCOOB (BANCO COOPERATIVO DO BRASIL)'),('655','BANCO VOTORANTIM S.A'),('655','NEON PAGAMENTOS S.A (OS MESMOS DADOS DO BANCO VOTORANTIM)'),('41','BANRISUL – BANCO DO ESTADO DO RIO GRANDE DO SUL S.A'),('389','BANCO MERCANTIL DO BRASIL S.A'),('422','BANCO SAFRA S.A'),('70','BANCO DE BRASÍLIA (BRB)'),('136','UNICRED COOPERATIVA'),('741','BANCO RIBEIRÃO PRETO'),('739','BANCO CETELEM S.A'),('743','BANCO SEMEAR S.A'),('100','PLANNER CORRETORA DE VALORES S.A'),('96','BANCO B3 S.A'),('747','Banco RABOBANK INTERNACIONAL DO BRASIL S.A'),('748','SICREDI S.A'),('752','BNP PARIBAS BRASIL S.A'),('91','UNICRED CENTRAL RS'),('399','KIRTON BANK'),('108','PORTOCRED S.A'),('757','BANCO KEB HANA DO BRASIL S.A'),('102','XP INVESTIMENTOS S.A'),('84','UNIPRIME NORTE DO PARANÁ'),('180','CM CAPITAL MARKETS CCTVM LTDA'),('66','BANCO MORGAN STANLEY S.A'),('15','UBS BRASIL CCTVM S.A'),('143','TREVISO CC S.A'),('62','HIPERCARD BM S.A'),('74','BCO. J.SAFRA S.A'),('99','UNIPRIME CENTRAL CCC LTDA'),('25','BANCO ALFA S.A.'),('75','BCO ABN AMRO S.A'),('40','BANCO CARGILL S.A'),('190','SERVICOOP'),('63','BANCO BRADESCARD'),('191','NOVA FUTURA CTVM LTDA'),('64','GOLDMAN SACHS DO BRASIL BM S.A'),('97','CCC NOROESTE BRASILEIRO LTDA'),('16','CCM DESP TRÂNS SC E RS'),('12','BANCO INBURSA'),('3','BANCO DA AMAZONIA S.A'),('60','CONFIDENCE CC S.A'),('37','BANCO DO ESTADO DO PARÁ S.A'),('159','CASA CREDITO S.A'),('172','ALBATROSS CCV S.A'),('85','COOP CENTRAL AILOS'),('114','CENTRAL COOPERATIVA DE CRÉDITO NO ESTADO DO ESPÍRITO SANTO'),('36','BANCO BBI S.A'),('394','BANCO BRADESCO FINANCIAMENTOS S.A'),('4','BANCO DO NORDESTE DO BRASIL S.A.'),('320','BANCO CCB BRASIL S.A'),('189','HS FINANCEIRA'),('105','LECCA CFI S.A'),('76','BANCO KDB BRASIL S.A.'),('82','BANCO TOPÁZIO S.A'),('286','CCR DE OURO'),('93','PÓLOCRED SCMEPP LTDA'),('273','CCR DE SÃO MIGUEL DO OESTE'),('157','ICAP DO BRASIL CTVM LTDA'),('183','SOCRED S.A'),('14','NATIXIS BRASIL S.A'),('130','CARUANA SCFI'),('127','CODEPE CVC S.A'),('79','BANCO ORIGINAL DO AGRONEGÓCIO S.A'),('81','BBN BANCO BRASILEIRO DE NEGOCIOS S.A'),('118','STANDARD CHARTERED BI S.A'),('133','CRESOL CONFEDERAÇÃO'),('121','BANCO AGIBANK S.A'),('83','BANCO DA CHINA BRASIL S.A'),('138','GET MONEY CC LTDA'),('24','BCO BANDEPE S.A'),('95','BANCO CONFIDENCE DE CÂMBIO S.A'),('94','BANCO FINAXIS'),('276','SENFF S.A'),('137','MULTIMONEY CC LTDA'),('92','BRK S.A'),('47','BANCO BCO DO ESTADO DE SERGIPE S.A'),('144','BEXS BANCO DE CAMBIO S.A.'),('126','BR PARTNERS BI'),('301','BPP INSTITUIÇÃO DE PAGAMENTOS S.A'),('173','BRL TRUST DTVM SA'),('119','BANCO WESTERN UNION'),('254','PARANA BANCO S.A'),('268','BARIGUI CH'),('107','BANCO BOCOM BBM S.A'),('412','BANCO CAPITAL S.A'),('124','BANCO WOORI BANK DO BRASIL S.A'),('149','FACTA S.A. CFI'),('197','STONE PAGAMENTOS S.A'),('142','BROKER BRASIL CC LTDA'),('389','BANCO MERCANTIL DO BRASIL S.A.'),('184','BANCO ITAÚ BBA S.A'),('634','BANCO TRIANGULO S.A (BANCO TRIÂNGULO)'),('545','SENSO CCVM S.A'),('132','ICBC DO BRASIL BM S.A'),('298','VIPS CC LTDA'),('129','UBS BRASIL BI S.A'),('128','MS BANK S.A BANCO DE CÂMBIO'),('194','PARMETAL DTVM LTDA'),('310','VORTX DTVM LTDA'),('163','COMMERZBANK BRASIL S.A BANCO MÚLTIPLO'),('280','AVISTA S.A'),('146','GUITTA CC LTDA'),('279','CCR DE PRIMAVERA DO LESTE'),('182','DACASA FINANCEIRA S/A'),('278','GENIAL INVESTIMENTOS CVM S.A'),('271','IB CCTVM LTDA'),('21','BANCO BANESTES S.A'),('246','BANCO ABC BRASIL S.A'),('751','SCOTIABANK BRASIL'),('208','BANCO BTG PACTUAL S.A'),('746','BANCO MODAL S.A'),('241','BANCO CLASSICO S.A'),('612','BANCO GUANABARA S.A'),('604','BANCO INDUSTRIAL DO BRASIL S.A'),('505','BANCO CREDIT SUISSE (BRL) S.A'),('196','BANCO FAIR CC S.A'),('300','BANCO LA NACION ARGENTINA'),('477','CITIBANK N.A'),('266','BANCO CEDULA S.A'),('122','BANCO BRADESCO BERJ S.A'),('376','BANCO J.P. MORGAN S.A'),('473','BANCO CAIXA GERAL BRASIL S.A'),('745','BANCO CITIBANK S.A'),('120','BANCO RODOBENS S.A'),('265','BANCO FATOR S.A'),('7','BNDES (Banco Nacional do Desenvolvimento Social)'),('188','ATIVA S.A INVESTIMENTOS'),('134','BGC LIQUIDEZ DTVM LTDA'),('641','BANCO ALVORADA S.A'),('29','BANCO ITAÚ CONSIGNADO S.A'),('243','BANCO MÁXIMA S.A'),('78','HAITONG BI DO BRASIL S.A'),('111','BANCO OLIVEIRA TRUST DTVM S.A'),('17','BNY MELLON BANCO S.A'),('174','PERNAMBUCANAS FINANC S.A'),('495','LA PROVINCIA BUENOS AIRES BANCO'),('125','BRASIL PLURAL S.A BANCO'),('488','JPMORGAN CHASE BANK'),('65','BANCO ANDBANK S.A'),('492','ING BANK N.V'),('250','BANCO BCV'),('145','LEVYCAM CCV LTDA'),('494','BANCO REP ORIENTAL URUGUAY'),('253','BEXS CC S.A'),('269','HSBC BANCO DE INVESTIMENTO'),('213','BCO ARBI S.A'),('139','INTESA SANPAOLO BRASIL S.A'),('18','BANCO TRICURY S.A'),('630','BANCO INTERCAP S.A'),('224','BANCO FIBRA S.A'),('600','BANCO LUSO BRASILEIRO S.A'),('623','BANCO PAN'),('204','BANCO BRADESCO CARTOES S.A'),('479','BANCO ITAUBANK S.A'),('456','BANCO MUFG BRASIL S.A'),('464','BANCO SUMITOMO MITSUI BRASIL S.A'),('613','OMNI BANCO S.A'),('652','ITAÚ UNIBANCO HOLDING BM S.A'),('653','BANCO INDUSVAL S.A'),('69','BANCO CREFISA S.A'),('370','BANCO MIZUHO S.A'),('249','BANCO INVESTCRED UNIBANCO S.A'),('318','BANCO BMG S.A'),('626','BANCO FICSA S.A'),('270','SAGITUR CC LTDA'),('366','BANCO SOCIETE GENERALE BRASIL'),('113','MAGLIANO S.A'),('131','TULLETT PREBON BRASIL CVC LTDA'),('11','C.SUISSE HEDGING-GRIFFO CV S.A (Credit Suisse)'),('611','BANCO PAULISTA'),('755','BOFA MERRILL LYNCH BM S.A'),('89','CCR REG MOGIANA'),('643','BANCO PINE S.A'),('140','EASYNVEST - TÍTULO CV S.A'),('707','BANCO DAYCOVAL S.A'),('288','CAROL DTVM LTDA'),('101','RENASCENCA DTVM LTDA'),('487','DEUTSCHE BANK S.A BANCO ALEMÃO'),('233','BANCO CIFRA'),('177','GUIDE'),('633','BANCO RENDIMENTO S.A'),('218','BANCO BS2 S.A'),('292','BS2 DISTRIBUIDORA DE TÍTULOS E INVESTIMENTOS'),('169','BANCO OLÉ BONSUCESSO CONSIGNADO S.A'),('293','LASTRO RDV DTVM LTDA'),('285','FRENTE CC LTDA'),('80','B&T CC LTDA'),('753','NOVO BANCO CONTINENTAL S.A BM'),('222','BANCO CRÉDIT AGRICOLE BR S.A'),('754','BANCO SISTEMA'),('98','CREDIALIANÇA CCR'),('610','BANCO VR S.A'),('712','BANCO OURINVEST S.A'),('10','CREDICOAMO'),('283','RB CAPITAL INVESTIMENTOS DTVM LTDA'),('217','BANCO JOHN DEERE S.A'),('117','ADVANCED CC LTDA'),('336','BANCO C6 S.A - C6 BANK'),('654','BANCO A.J. RENNER S.A'))

    gender = forms.CharField(label=texts['Gender'], required=False, initial=GENDER_CHOICES[0],
                             widget=forms.RadioSelect(choices=GENDER_CHOICES, attrs={'class': 'radio_inp'}))
    dob_day = forms.ChoiceField(label=texts['Dob'], required=False, choices=[(x, x) for x in range(1, 32)], widget=forms.Select(attrs={
        'placeholder': texts['Dob_Day'], 'class': 'form-control'}))
    dob_month = forms.ChoiceField(label='', required=False, choices=DOB_MONTHS, widget=forms.Select(attrs={
        'placeholder': texts['Dob_Month'], 'class': 'form-control'}))
    dob_year = forms.ChoiceField(label='', required=False, choices=[(x, x) for x in range(first_year, last_year)], widget=
        forms.Select(attrs={'placeholder': texts['Dob_Year'], 'class': 'form-control'}))
    doc_type = forms.CharField(label=texts['Doc_Type'], required=False, initial=DOC_TYPES[0],
                               widget=forms.RadioSelect(choices=DOC_TYPES, attrs={'class': 'radio_inp'}))
    doc_number = forms.CharField(label=texts['Doc_Number'], required=False, widget=forms.TextInput(attrs={
        'placeholder': '', 'class': 'form-control', 'style': 'margin: auto;', 'maxlength': '18', 'autocomplete': 'document',
        'oninvalid': 'this.setCustomValidity("'+texts['CurrentCPFError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    mobile_country = forms.CharField(label=texts['Mobile'], required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['MobileCountry'], 'class': 'form-control', 'autocomplete': 'tel-country-code',
        'oninvalid': 'this.setCustomValidity("'+texts['MobileCountryError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    mobile_area = forms.IntegerField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['MobileArea'], 'class': 'form-control onlyNumbers', 'autocomplete': 'tel-area-code',
        'oninvalid': 'this.setCustomValidity("'+texts['MobileAreaError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    mobile_number = forms.IntegerField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Mobile'], 'class': 'form-control onlyNumbers', 'autocomplete': 'tel',
        'oninvalid': 'this.setCustomValidity("'+texts['MobileError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    address_postcode = forms.CharField(label=texts['Address'], required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Postcode'], 'class': 'form-control',
        'onfocusout': "SearchPostcode('id_address_postcode','id_address_street','id_address_area','id_address_city',"
                      "'id_address_state','id_address_additional','id_address_number')", 'autocomplete': 'postcode',
        'oninvalid': 'this.setCustomValidity("'+texts['CurrentCEPError']+'")',
        "oninput": "this.setCustomValidity('')"}))
    address_street = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Street'], 'class': 'form-control'}))
    address_number = forms.IntegerField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Number'], 'class': 'form-control onlyNumbers'}))
    address_additional = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Additional'], 'class': 'form-control'}))
    address_city = forms.CharField(label=texts['Address_City'], required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_City'], 'class': 'form-control'}))
    address_area = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Area'], 'class': 'form-control'}))
    address_state = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['Address_State'], 'class': 'form-control'}))
    address_country = forms.CharField(label='', required=False, initial='Brasil', widget=forms.TextInput(attrs={
        'placeholder': texts['Address_Country'], 'class': 'form-control'}))
    profile_desc = forms.CharField(label=texts['Profile_Desc'], required=False, widget=forms.Textarea(attrs={
        'placeholder': texts['Profile_Desc_pholder'], 'class': 'form-control'}))
    bank_name = forms.ChoiceField(label=texts['bank_details'], required=False, choices=BANKS_LIST, widget=forms.Select(attrs={
        'placeholder': texts['bank_name'], 'class': 'form-control'}))
    bank_branch = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['bank_branch'], 'class': 'form-control'}))
    bank_account = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['bank_account'], 'class': 'form-control'}))
    bank_owner = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={
        'placeholder': texts['bank_owner'], 'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('gender', 'dob_day', 'dob_month', 'dob_year', 'doc_type', 'doc_number',
                  'mobile_country', 'mobile_area', 'mobile_number', 'address_postcode', 'address_street',
                  'address_number', 'address_additional', 'address_city', 'address_state', 'address_country',
                  'profile_desc', 'address_area', 'bank_name', 'bank_branch', 'bank_account', 'bank_owner')


# class BoatForm(forms.ModelForm):
 #    texts = {}
 #    texts.update(userarea_texts())
  #   texts.update(global_texts())

   # class Meta:
    #    model = Boat
        # fields = ('boat_type', 'user', 'city', 'boat_amenities', 'images', 'fab_year', 'title', 'manufacturer', 'size',
          #         'capacity', 'overnight_capacity', 'bathrooms', 'rooms', '', '', '', '', '',)


class MessageForm(forms.ModelForm):
    # id_from = forms.IntegerField(widget=forms.NumberInput(), required=False)
    id_to = forms.CharField(widget=forms.TextInput(), required=False)
    message = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Message
        fields = ('msg_from', 'msg_to', 'message')


class CaptainForm(forms.ModelForm):
    texts = {}
    texts.update(global_texts())

    Q1_CHOICES = (('1', texts['Captain_Q1_opt1']), ('2', texts['Captain_Q1_opt2']))

    Q2_CHOICES = (('1', texts['Captain_Q2_opt1']), ('2', texts['Captain_Q2_opt2']), ('3', texts['Captain_Q2_opt3']),
                  ('4', texts['Captain_Q2_opt4']), ('5', texts['Captain_Q2_opt5']), ('6', texts['Captain_Q2_opt6']))

    Q3_CHOICES = (('1', texts['Captain_Q3_opt1']), ('2', texts['Captain_Q3_opt2']), ('3', texts['Captain_Q3_opt3']),
                  ('4', texts['Captain_Q3_opt4']), ('5', texts['Captain_Q3_opt5']))

    is_captaion = forms.CharField(label='', initial=Q1_CHOICES[0], required=False, widget=forms.RadioSelect(
        choices=Q1_CHOICES, attrs={'class': 'radio_inp'}))

    license_type = forms.CharField(label='', initial=Q2_CHOICES[0], required=False, widget=forms.RadioSelect(
        choices=Q2_CHOICES, attrs={'class': 'radio_inp', 'onchange': 'CheckSkipperLicense()'}))

    lt_professional = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'style': 'max-width: 250px;'}))

    experience = forms.CharField(label='', initial=Q3_CHOICES[0], required=False, widget=forms.RadioSelect(
        choices=Q3_CHOICES, attrs={'class': 'radio_inp'}))

    extra_activities = forms.ModelMultipleChoiceField(queryset=CaptainExtraActivities.objects.all(), label='',
        required=False, widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'radio_inp', 'style': 'width:15px;height:15px;float: left;'}))

    languages = forms.ModelMultipleChoiceField(queryset=CaptainLanguages.objects.all(), label='',
        required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'radio_inp'}))

    class Meta:
        model = CaptainProfile
        fields = ('is_captaion', 'license_type', 'lt_professional', 'experience', 'extra_activities', 'languages')
