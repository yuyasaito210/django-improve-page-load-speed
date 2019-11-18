from django.contrib import admin
from django.urls import path
from .views import home, logout_view, user_profile, user_messages, user_favorites, user_bookings, \
    create_extra_activity, search_results, add_to_favorities, user_boats, how_it_works, boat_view, create_booking, \
    create_invoice, send_message, user_book_requests, forgot_password, home_fishing, get_boat_details, \
    upload_boat_picture, terms_page, privacy_policy, boat_block_dates
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # HOME
    path('', home, name="home"),

    # PESCA
    path('pesca', home_fishing, name="home_fishing"),
    path('pesca/loja-de-pesca', home_fishing, name="home_fishing_lojas"),

    # USERAREA - MEU PERFIL
    path('meu-perfil', user_profile, name="user_profile"),

    # USERAREA - MINHAS MENSAGENS
    path('minhas-mensagens', user_messages, name="user_messages"),
    path('mensagens', user_messages, name="mensagens"),

    # USERAREA - MEUS FAVOTIROS
    path('barcos-favoritos', user_favorites, name="user_favorites"),

    # USERAREA - MEUS PASSEIOS
    path('meus-passeios', user_bookings, name="user_bookings"),
    path('minhas-reservas', user_bookings, name="minhas-reservas"),

    # USERAREA - MEUS BARCOS
    path('meus-barcos', user_boats, name="user_boats"),
    path('meus-anuncios/<str:add_boat>', user_boats, name="user_boats"),

    # USERAREA - SOLICITACOES DE RESERVAS RECEBIDAS
    path('solicitacoes-de-reservas', user_book_requests, name="user_book_requests"),
    path('reservas-recebidas', user_book_requests, name="reservas-recebidas"),

    # BUSCA
    path('procurar/<str:city>', search_results, name="search_results"),

    # PÁGINA BARCO
    path('embarcacao/<str:boat_city>/<int:boat_id>', boat_view, name="boat_view_city"),
    path('embarcacao/<int:boat_id>', boat_view, name="boat_view"),
    path('barco/<int:boat_id>', boat_view, name="barco"),
    path('barco/<str:boat_city>/<str:boat_name>', boat_view, name="barco_nome"),

    # PÁGINA COMO FUNCIONA
    path('como-funciona', how_it_works, name="how_it_works"),

    # TERMOS DE ADESÃO
    path('termos-de-adesao', terms_page, name="terms_page"),

    # POLÍTICAS DE PRIVACIDADE
    path('politicas-de-privacidade', privacy_policy, name="privacy_policy"),

    # FUNCTION - ESQUECI A SENHA
    path('esqueci-a-senha', forgot_password, name="forgot-password"),

    # FUNCTION - CRIACAO DE NOVA ATIVIDADE
    path('criacao-atividade-extra', create_extra_activity, name="create_extra_activity"),

    # FUNCTION - CRIAÇÃO DE RESERVA
    path('criacao-de-reserva', create_booking, name="create_booking"),
    path('barco/criacao-de-reserva', create_booking, name="create_booking_boat"),
    path('barco/create_booking', create_booking, name="barco_create_booking"),

    # FUNCTION - CRIAÇÃO DE FATURA
    path('criacao-de-fatura', create_invoice, name="create_invoice"),
    path('barco/create_invoice', create_invoice, name="barco_create_invoice"),

    # FUNCTION - ENVIO DE MENSAGEM NA PÁG. DO BARCO
    path('barco/enviar-mensagem', send_message, name="barco_send_message"),
    path('enviar-mensagem', send_message, name="barco_send_message"),

    # FUNCTION - ADICIONAR BARCO AOS FAVORITOS
    path('adicionar-favorito', add_to_favorities, name="add_to_favorities"),

    # FUNCTION - LER DADOS DO BARCO
    path('meus-barcos/ler-barco', get_boat_details, name="get_boat_details"),

    # FUNCTION - SALVAR IMAGEM DO BARCO
    path('salvar-imagem-barco', upload_boat_picture, name="upload_boat_picture"),

    # FUNCTION - CHANGE BOATS BLOCKED DATES
    path('bloquear-datas', boat_block_dates, name="boat_block_dates"),

    # FUNCTION - SAIR
    path('sair', logout_view, name="logout"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
