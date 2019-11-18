from django.shortcuts import render, HttpResponse, redirect
from .views_texts import global_texts, userarea_texts, results_texts, how_it_works_texts, bview_texts
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import City, Review, UserProfile, Message, BoatFavorite, Booking, CaptainProfile, BoatAmenities, \
    BoatType, BoatImages, Boat, State, BoatPriceIncludes, BoatFishingSpecies, IBGECityCodes, Invoice, BoatBlockedDates
from .forms import SignUpForm, SignInForm, UploadUserPhotoForm, UserareaUpdateProfileForm, UserareaUpdateUserForm, \
    MessageForm, CaptainForm, CaptainExtraActivities
from collections import defaultdict
from django.db.models import ExpressionWrapper, F, IntegerField, Count, Q, ObjectDoesNotExist, Min, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
import datetime, random, string
from datetime import date
from totalvoice.cliente import Cliente
from django.core.mail import send_mail
import requests, json
from decouple import config
from bnboats_webproject.settings import BNBOATS_TAX, FISHING_STORES_DISCOUNT, STATIC_MEDIA_URL
from django.core import serializers
from django.forms.models import model_to_dict
from bnboats_webproject.settings import STATIC_URL
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def paggcerto_gettoken():

    if config("ENVIRONMENT") != "PROD":
        return

    data = {
        'login': 'lucas@bnboats.com',
        'password': config('PAGGCERTO_PASS')
    }
    json_data = json.dumps(data)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response_str = requests.post('https://account.paggcerto.com.br/api/v2/qA/signin/', data=json_data, headers=headers)
    response = response_str.json()

    return response['token']


def logout_view(request):
    logout(request)
    return redirect("home")


    # for s in range(100, 200):
    #    user_query = User.objects.filter(pk=s)
    #    user_pass_count = user_query.count()
    #    if user_pass_count == 1:
    #        user_pass = user_query[0]
    #        user_pass.set_password(user_pass.password)
    #        user_pass.save()


def home(request):
    data = {}

    # get boat sizes
    boat_sizes = []

    # get page texts
    data.update(global_texts())

    # city search
    if request.POST:
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

    # Sign in and Sign up function
    # data.update()
    signin_signup_func(request, data)
    if "next" in data:
        return redirect(data['next'], data['next_param'])

    if data['sms_error'] == "error":
        return redirect('user_profile')

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    # get boats reviews from db
    reviews = Review.objects.select_related('author')
    data['reviews'] = reviews

    # get last added 4 boats
    new_boats = Boat.objects.filter(images__isnull=False).annotate(
        price_pperson=ExpressionWrapper(F('price_day') / F('capacity'), output_field=IntegerField()),
        reviews_counting=Count('review')).order_by('-reviews_counting')[:4]
    data['newBoats'] = new_boats

    # if login was requested
    if 'signin' in request.GET and request.user.is_anonymous:
        data['signin'] = "True"
    else:
        if 'next' in request.GET:
            return redirect(request.GET['next'])

    # data['testing'] = randomDigits(6)
    data['static_media_url'] = STATIC_MEDIA_URL

    return render(request, "home.html", data)


def home_fishing(request):
    data = {}

    # get page texts
    data.update(global_texts())
    request.session['default_page'] = "PES;"
    data['home_type'] = request.session['default_page']

    # city search
    if request.POST:
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

    # Sign in and Sign up function
    data.update(signin_signup_func(request, data))
    if data['sms_error'] == "error":
        return redirect('user_profile')

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    # get boats reviews from db
    reviews = Review.objects.select_related('author')
    data['reviews'] = reviews

    # get last added 4 boats
    new_boats = Boat.objects.filter(images__isnull=False).annotate(
        price_pperson=ExpressionWrapper(F('price_day') / F('capacity'), output_field=IntegerField()),
        reviews_counting=Count('review')).order_by('-reviews_counting')[:4]
    data['newBoats'] = new_boats

    return render(request, "home_fishing.html", data)


@login_required
def user_profile(request):
    data = {}

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(userarea_texts())
    data.update(global_texts())

    data['upload_photo'] = UploadUserPhotoForm()
    data['alert_classes'] = 'hideOnly'

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:
        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

        # Send SMS code again
        if "resend_sms_code" in request.POST:
            #data['aaa'] = "bbb"
            req_user = request.user.userprofile
            req_user.mobile_country = request.POST['resend_sms_mcountry']
            req_user.mobile_area = request.POST['resend_sms_marea']
            req_user.mobile_number = request.POST['resend_sms_mnumber']
            req_user.save()
            data['user_created'] = "true"
            send_sms(request.user, 1)

        # if mobile sms is sent to be confirmed, here is the validation
        if 'mobile_code' in request.POST:
            userprofile = UserProfile.objects.get(user=request.user)
            if str(request.POST['mobile_code']).lower() == str(userprofile.mobile_code).lower():
                userprofile.mobile_confirmed = True
                userprofile.save()
                if request.user is not None and request.POST['add_boat'] == 'true':
                    return redirect(user_boats, add_boat="add")
            else:
                data['SignInFormVisibilityClass'] = ""
                data['SignUpFormVisibilityClass'] = "hideOnly"
                data.update({"LogonFormMsg": "Código inválido. Por favor, tente novamente."})
                data.update({"LogonFormMsgClass": "alert-danger"})

        # update user details
        if 'first_name' in request.POST:
            user_form = UserareaUpdateUserForm(request.POST, instance=request.user)
            profile_form = UserareaUpdateProfileForm(request.POST, instance=request.user.userprofile)
            password_form = PasswordChangeForm(request.user, request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                data['alert_message'] = data['ProfileUpdatedSuccessfully']
                data['alert_classes'] = 'alert-success'
            else:
                error_dict = user_form.errors
                error_dict.update(profile_form.errors)
                if 'first_name' in error_dict:
                    error_dict[data['FullName']] = error_dict.pop("first_name")
                if 'username' in error_dict:
                    error_dict[data['Email']] = error_dict.pop("username")
                if 'mobile_country' in error_dict:
                    error_dict[data['MobileCountry']] = error_dict.pop("mobile_country")
                if 'mobile_area' in error_dict:
                    error_dict[data['MobileArea']] = error_dict.pop("mobile_area")
                if 'mobile_number' in error_dict:
                    error_dict[data['Mobile']] = error_dict.pop("mobile_number")
                if 'gender' in error_dict:
                    error_dict[data['Gender']] = error_dict.pop("gender")
                if 'doc_type' in error_dict:
                    error_dict[data['Doc_Type']] = error_dict.pop("doc_type")
                if 'doc_number' in error_dict:
                    error_dict[data['Doc_Number']] = error_dict.pop("doc_number")
                if 'address_postcode' in error_dict:
                    error_dict[data['Address_Postcode']] = error_dict.pop("address_postcode")
                if 'address_street' in error_dict:
                    error_dict[data['Address_Street']] = error_dict.pop("address_street")
                if 'address_number' in error_dict:
                    error_dict[data['Address_Number']] = error_dict.pop("address_number")
                if 'address_city' in error_dict:
                    error_dict[data['Address_City']] = error_dict.pop("address_city")
                if 'address_state' in error_dict:
                    error_dict[data['Address_State']] = error_dict.pop("address_state")
                if 'address_area' in error_dict:
                    error_dict[data['Address_Area']] = error_dict.pop("address_area")
                data.update({"alert_message": error_dict})
                data['alert_classes'] = 'alert-danger'

            if request.POST['new_password1'] != "":
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    data['alert_message'] = data['ProfileUpdatedSuccessfully']
                    data['alert_classes'] = 'alert-success'
                    send_sms(request.user, 12, "")
                else:
                    try:
                        error_dict
                    except NameError:
                        error_dict = None
                    if error_dict is None:
                        error_dict = password_form.errors
                    else:
                        error_dict.update(password_form.errors)
                    if 'new_password1' in error_dict:
                        error_dict[data['Password']] = error_dict.pop("new_password1")
                    if 'new_password2' in error_dict:
                        error_dict[data['Password']] = error_dict.pop("new_password2")
                    data.update({"alert_message": error_dict})
                    data['alert_classes'] = 'alert-danger'

    user_profile_qry = UserProfile.objects.get(user=request.user.pk)
    profile_form = UserareaUpdateProfileForm(instance=user_profile_qry)
    data['profile_form'] = profile_form

    user_qry = User.objects.get(id=request.user.pk)
    user_form = UserareaUpdateUserForm(instance=user_qry)
    # password_form = UpdatePasswordForm(instance=user_qry)
    data['user_form'] = user_form
    PasswordChangeForm.use_required_attribute = False
    data['password_form'] = PasswordChangeForm(request.user)

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    if data['IsOwner']:
        user_captain_qry = CaptainProfile.objects.get(user=request.user.pk)
        data['CaptainForm'] = CaptainForm(instance=user_captain_qry)

    if user_qry.userprofile.mobile_confirmed == False:
        data['mobile_confirmed'] = "False"
    else:
        data['mobile_confirmed'] = "True"

    return render(request, "userarea_profile.html", data)


@login_required
def user_messages(request):
    data = {}

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(userarea_texts())

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:
        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

        if 'id_to' in request.POST:
            msg_to_post = User.objects.get(pk=request.POST['id_to'])
            form = Message.objects.create(msg_from=request.user, msg_to=msg_to_post,
                                          message=request.POST['message'])
            form.save()
            data['msg_focus'] = request.POST['id_to']
            msg_arr = {
                "from_user": request.user.first_name,
                "to_user": msg_to_post.first_name,
                "msg": request.POST['message']
            }
            send_sms(msg_to_post, 2)
            sendEmail(msg_to_post, 2, msg_arr)

    # forms
    data['upload_photo'] = UploadUserPhotoForm()
    data['msg_form'] = MessageForm()

    messages = Message.objects.filter(Q(msg_from__pk=request.user.pk) | Q(msg_to__pk=request.user.pk))
    res_messages = defaultdict(dict)
    msg_contacts = {}
    for msg in messages:
        if request.user.pk == msg.msg_from.pk:
            dest_user = msg.msg_to.first_name
            dest_user_id = msg.msg_to.pk
            dest_user_photo = msg.msg_to.userprofile.image
            msg_type = "from"
        else:
            dest_user = msg.msg_from.first_name
            msg_type = "to"
            dest_user_id = msg.msg_from.pk
            dest_user_photo = msg.msg_from.userprofile.image
        msg_item = {msg.pk: [dest_user, msg_type, msg.message, msg.is_read, dest_user_photo]}
        res_messages[dest_user_id].update(msg_item)
        msg_contacts.update({dest_user_id: [dest_user, dest_user_photo]})

    data['all_contacts'] = msg_contacts
    data['messages'] = dict(res_messages)
    data['IsOwner'] = is_user_owner(request.user.pk)
    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    return render(request, "userarea_messages.html", data)


@login_required
def user_favorites(request):
    data = {}

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(userarea_texts())
    data['upload_photo'] = UploadUserPhotoForm()

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:
        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

        if 'ua_fav_to_remove' in request.POST:
            BoatFavorite.objects.get(pk=request.POST['ua_fav_to_remove']).delete()

    data['boat_favorities'] = BoatFavorite.objects.filter(user=request.user.pk)
    data['IsOwner'] = is_user_owner(request.user.pk)
    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    return render(request, "userarea_favorites.html", data)


@login_required
def user_bookings(request):
    data = {}

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    data['msg_class'] = "hideOnly"

    # Update profile picture
    data.update(update_profile_pic(request))
    if request.POST:
        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))
        # Cancel booking
        if 'cancel_booking_id' in request.POST:
            booking_cancel = Booking.objects.get(pk=request.POST['cancel_booking_id'])
            booking_cancel.status="Cancelled"
            booking_cancel.save()
            sendEmail(booking_cancel.boat.user, 11, {"customer": request.user.first_name})
        # Review a boat
        if 'booking_review_id' in request.POST:
            booking_id = request.POST['booking_review_id']
            review_score = request.POST['review_score']
            review_text = request.POST['booking_review_text']
            booking = Booking.objects.get(pk=booking_id)
            Review.objects.create(boat=booking.boat, author=request.user.userprofile, score=review_score, review=review_text, status='Published')
            booked_boat = Boat.objects.get(pk=booking.boat.pk)
            new_score = (float(booked_boat.review_score) + float(review_score)) / (int(booked_boat.reviews_count) + 1)
            booked_boat.review_score = new_score
            booked_boat.reviews_count = booked_boat.reviews_count + 1
            booked_boat.save()
            data['message'] = "Avaliação realizada com sucesso!"
            data['msg_class'] = "alert-success"

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(userarea_texts())
    data['upload_photo'] = UploadUserPhotoForm()

    qry_bookings = Booking.objects.filter(customer=request.user.pk)
    for booking in qry_bookings:
        booking_date = booking.date_to.strftime("%d/%m/%Y")
        if booking_date > today:
            booking.hideBeforeBookingDay = "hideOnly"
        if booking_date < today:
            booking.hideAfterBookingDay = "hideOnly"
        booking.status_id = booking.status
        booking.status = convert_status_id(booking.status)
        if booking.booking_period == "2":
            booking.booking_period = "Avulso (2 horas)"
        if booking.booking_period == "4":
            booking.booking_period = "Meia Diária (4 horas)"
        if booking.booking_period == "8":
            booking.booking_period = "Diária (8 horas)"
        if booking.booking_period == "24":
            booking.booking_period = "Pernoite (24 horas)"

    data['bookings'] = qry_bookings
    data['IsOwner'] = is_user_owner(request.user.pk)
    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))
    data['page'] = "bookings"

    return render(request, "userarea_bookings.html", data)


@login_required
def user_book_requests(request):
    data = {}

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    data['msg_class'] = "hideOnly"

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:
        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))
        # Cancel booking
        if 'cancel_booking_id' in request.POST:
            booking_cancel = Booking.objects.get(pk=request.POST['cancel_booking_id'])
            booking_cancel.status="Cancelled"
            booking_cancel.save()
            sendEmail(request.user, 11, {"customer": booking_cancel.boat.user.first_name})
        # Review a boat
        if 'booking_review_id' in request.POST:
            booking_id = request.POST['booking_review_id']
            review_score = request.POST['review_score']
            review_text = request.POST['booking_review_text']
            booking = Booking.objects.get(pk=booking_id)
            Review.objects.create(boat=booking.boat, author=request.user.userprofile, score=review_score, review=review_text, status='Published')
            booked_boat = Boat.objects.get(pk=booking.boat.pk)
            new_score = (float(booked_boat.review_score) + float(review_score)) / (int(booked_boat.reviews_count) + 1)
            booked_boat.review_score = new_score
            booked_boat.reviews_count = booked_boat.reviews_count + 1
            booked_boat.save()
            data['message'] = "Avaliação realizada com sucesso!"
            data['msg_class'] = "alert-success"
        # Review a boat
        if 'passenger_review_id' in request.POST:
            notowner_user = User.objects.get(pk=request.POST['passenger_review_id'])
            review_score = request.POST['review_score']
            review_text = request.POST['booking_review_text']
            Review.objects.create(notowner_user=notowner_user.userprofile, author=request.user.userprofile, score=review_score, review=review_text, status='Published')
            data['message'] = "Avaliação realizada com sucesso!"
            data['msg_class'] = "alert-success"
        # Approve or Reject a booking
        if 'approve_booking_id' in request.POST:
            booking_id = request.POST['approve_booking_id']
            booking_to_approve = request.POST['approve_booking_action']
            booking = Booking.objects.get(pk=booking_id)
            booking_data = {
                "owner": booking.boat.user.first_name,
                "date_from": booking.date_from,
                "date_to": booking.date_to,
                "city": booking.boat.city,
                "no_passangers": booking.no_passengers,
                "booking_id": booking_id,
                "boat_name": booking.boat.title,
                "boat_id": booking.boat.pk,
                "cust_mobile": str(booking.boat.user.userprofile.mobile_area) + " " + str(booking.boat.user.userprofile.mobile_number),
                "customer": str(booking.customer.first_name)
            }
            if booking_to_approve == "true":
                booking.status = "Confirmed"
                sendEmail(booking.customer, 5, booking_data)
                sendEmail(booking.boat.user, 8, booking_data)
                cust_mobile = str(request.user.userprofile.mobile_area) + " " + str(request.user.userprofile.mobile_number)
                owner_mobile = str(booking.boat.user.userprofile.mobile_area) + " " + str(booking.boat.user.userprofile.mobile_number)
                send_sms(request.user, 4, {"mobile": owner_mobile})
                send_sms(request.user, 9, {"mobile": cust_mobile, "customer_name": request.user.first_name})
            else:
                booking.status = "Cancelled"
                sendEmail(booking.customer, 6, booking_data)
                sendEmail(booking.boat.user, 9, booking_data)
                send_sms(request.user, 5, "")

            booking.save()

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(global_texts())
    data.update(userarea_texts())
    data['upload_photo'] = UploadUserPhotoForm()

    booking = Booking.objects.all()
    booking_list = []
    qry_boats = Boat.objects.filter(user=request.user.pk).exclude(status="New")
    for boat in qry_boats:
        booking_list.extend(list(booking.filter(boat=boat)))

    qry_bookings = booking_list # Booking.objects.filter(customer=request.user.pk)
    for booking in qry_bookings:
        booking_date = booking.date_to.strftime("%d/%m/%Y")
        if booking_date > today:
            booking.hideBeforeBookingDay = "hideOnly"
        if booking_date < today:
            booking.hideAfterBookingDay = "hideOnly"
        booking.status_id = booking.status
        booking.status = convert_status_id(booking.status)
        if booking.booking_period == "2":
            booking.booking_period = "Avulso (2 horas)"
        if booking.booking_period == "4":
            booking.booking_period = "Meia Diária (4 horas)"
        if booking.booking_period == "8":
            booking.booking_period = "Diária (8 horas)"
        if booking.booking_period == "24":
            booking.booking_period = "Pernoite (24 horas)"

    data['bookings'] = qry_bookings
    data['IsOwner'] = is_user_owner(request.user.pk)
    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))
    data['page'] = "booking_requests"

    return render(request, "userarea_bookings.html", data)


@login_required
def user_boats(request, add_boat=""):
    data = {}
    add_boat_params = {}
    data['boat_message_class'] = "hideOnly"

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    # get all cities from db
    data.update(load_allcities(request))

    # page texts
    data.update(userarea_texts())
    data.update(global_texts())
    data['upload_photo'] = UploadUserPhotoForm()

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:

        # Boats search request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = "0"
            return redirect('search_results', city=(city_name))

        # create Boat
        if 'boat_type_inp' in request.POST:

            add_boat = ""

            # get city
            state_db = State.objects.get_or_create(name=request.POST.get('address_state', 'SP'))
            city_db = City.objects.get_or_create(city__icontains=request.POST.get('address_city', 'Guarujá'), state=state_db[0])

            # get boat type
            boat_type = BoatType.objects.get(sid_bt=request.POST.get('boat_type_inp', 'LAN'))

            # create boat args
            add_boat_params = {"boat_type": boat_type}
            add_boat_params.update({"user": request.user})
            add_boat_params.update({"fab_year": request.POST.get('boat_fab_year', 2000)})
            add_boat_params.update({"manufacturer": request.POST.get('boat_manufactor', 'Fabricante desconhecido')})
            add_boat_params.update({"size": request.POST.get('boat_size', 10)})
            add_boat_params.update({"capacity": request.POST.get('boat_capacity', 2)})
            add_boat_params.update({"overnight_capacity": request.POST.get('boat_overnight_capacity', 2)})
            add_boat_params.update({"rooms": request.POST.get('boat_rooms', 1)})
            add_boat_params.update({"bathrooms": request.POST.get('boat_bathrooms', 1)})
            add_boat_params.update({"animals": request.POST.get('pet_inp', 'No')})
            add_boat_params.update({"smoke": request.POST.get('smoking_inp', 'No')})
            add_boat_params.update({"wheelchair": request.POST.get('accessibility_inp', 'No')})
            # add_boat_params.update({"postcode": request.POST.get('address_postcode')})
            add_boat_params.update({"address": request.POST.get('address_street', '')})
            # add_boat_params.update({"additional": request.POST.get('address_additional')})
            add_boat_params.update({"city": city_db[0]})
            add_boat_params.update({"title": request.POST.get('boat_reg_title','Título em branco')})
            add_boat_params.update({"description": request.POST.get('boat_reg_description','')})
            add_boat_params.update({"has_discount": request.POST.get('disc_inp', 'No')})
            if 'fish_type' in request.POST:
                add_boat_params.update({"fish_rules": request.POST.get('fish_type')})
            if request.POST['fish_bait_inp']:
                add_boat_params.update({"fish_bait": request.POST.get('fish_bait_inp')})
            add_boat_params.update({"fish_places": request.POST.get('fish_place_inp')})
            add_boat_params.update({"status": "InReview"})

            # update prices
            bnboats_tax = BNBOATS_TAX # 1.185
            if request.POST.get('disc_inp', 'No') == "Yes":
                discount = 0.80
            else:
                discount = 1.00

            # SINGLE PRICE
            try:
                single_price = float((request.POST.get('price_item_single','0')).replace(",", "."))
            except ValueError:
                single_price = 0
            price_item_single = float(single_price) * bnboats_tax * discount
            add_boat_params.update({"owner_price_single": single_price})
            add_boat_params.update({"price_single": price_item_single})

            # HALF DAY PRICE
            try:
                hday_price = float((request.POST.get('price_item_hday','0')).replace(",", "."))
            except ValueError:
                hday_price = 0
            price_item_hday = float(hday_price) * bnboats_tax * discount
            add_boat_params.update({"owner_price_half_day": hday_price})
            add_boat_params.update({"price_half_day": price_item_hday})

            # DAY PRICE
            try:
                day_price = float((request.POST.get('price_item_day','0')).replace(",", "."))
            except ValueError:
                day_price = 0
            price_item_day = float(day_price) * bnboats_tax * discount
            add_boat_params.update({"owner_price_day": day_price})
            add_boat_params.update({"price_day": price_item_day})

            # OVERNIGHT PRICE
            try:
                overnight_price = float((request.POST.get('price_item_overnight','0')).replace(",", "."))
            except ValueError:
                overnight_price = 0
            price_item_overnight = float(overnight_price) * bnboats_tax * discount
            add_boat_params.update({"owner_price_overnight": overnight_price})
            add_boat_params.update({"price_overnight": price_item_overnight})

            if request.POST['updated_boat'] != "":
                # update boat
                # add_boat_params.update({"pk": request.POST.get('updated_boat')})
                added_boat = Boat.objects.filter(pk=request.POST.get('updated_boat'), user=request.user).update(**add_boat_params)
                added_boat = Boat.objects.get(pk=request.POST.get('updated_boat'), user=request.user)
                sendEmail(request.user, "admin", {"subject": "Barco atualizado no site", "message": "O "
                    "barco " + str(added_boat.pk) + " - " + str(added_boat.title) + " foi atualizado, favor aprovar."})
            else:
                # create boat
                added_boat = Boat.objects.create(**add_boat_params)
                sendEmail(request.user, "admin", {"subject": "Novo barco criado no site", "message": "Um novo "
                    "barco " + str(added_boat.pk) + " - " + str(added_boat.title) + " foi criado, favor aprovar."})

            # add fish species
            boat_fspecies_array_1 = (request.POST.get('boat_fspecies_inp')).split(',')
            added_boat.fish_species.clear()
            added_boat.save()
            for fish in boat_fspecies_array_1:
                if fish:
                    fish_obj = BoatFishingSpecies.objects.get(sid_bfs=fish)
                    added_boat.fish_species.add(fish_obj)

            # add price includes
            boat_pincludes_array_1 = (request.POST.get('boat_pincludes_inp_1')).split(',')
            added_boat.p_single_includes.clear()
            added_boat.save()
            for pinclude in boat_pincludes_array_1:
                if pinclude:
                    pinclude_obj = BoatPriceIncludes.objects.get(sid_bpi=pinclude)
                    added_boat.p_single_includes.add(pinclude_obj)

            boat_pincludes_array_2 = (request.POST.get('boat_pincludes_inp_2')).split(',')
            added_boat.p_hday_includes.clear()
            added_boat.save()
            for pinclude in boat_pincludes_array_2:
                if pinclude:
                    pinclude_obj = BoatPriceIncludes.objects.get(sid_bpi=pinclude)
                    added_boat.p_hday_includes.add(pinclude_obj)

            boat_pincludes_array_3 = (request.POST.get('boat_pincludes_inp_3')).split(',')
            added_boat.p_day_includes.clear()
            added_boat.save()
            for pinclude in boat_pincludes_array_3:
                if pinclude:
                    pinclude_obj = BoatPriceIncludes.objects.get(sid_bpi=pinclude)
                    added_boat.p_day_includes.add(pinclude_obj)

            boat_pincludes_array_4 = (request.POST.get('boat_pincludes_inp_4')).split(',')
            added_boat.p_overnight_includes.clear()
            added_boat.save()
            for pinclude in boat_pincludes_array_4:
                if pinclude:
                    pinclude_obj = BoatPriceIncludes.objects.get(sid_bpi=pinclude)
                    added_boat.p_overnight_includes.add(pinclude_obj)

            # add amenities
            boat_amenities_array = (request.POST.get('boat_amenities')).split(',')
            added_boat.boat_amenities.clear()
            added_boat.save()
            for amenity in boat_amenities_array:
                if amenity:
                    amenity_obj = BoatAmenities.objects.get(sid_ba=amenity)
                    added_boat.boat_amenities.add(amenity_obj)

            # for img_del in added_boat.images.all():
                # data["debug_tests"] = str(img_del.boat_image).split("/")[-1]

            if 'inp_pic_id' in request.POST:
                for new_img in request.POST.getlist('inp_pic_id'):
                    if new_img != "":
                        added_boat.images.add(BoatImages.objects.get(pk=new_img))

            # delete images - OK
            if "photos_to_del" in request.POST:
                photos_to_del = request.POST['photos_to_del']
                if photos_to_del != "":
                    photos_to_del = photos_to_del.split(",")
                    # loop all images requested to be deleted
                    for del_img in photos_to_del:
                        # loop all images in db
                        for db_img in added_boat.images.all():
                            # delele image from db if it matces with the requested ones
                            if del_img == str(db_img).split("/")[-1]:
                                db_img.delete()

            # get all remaining images, define the main one and clean the relationship
            prev_imgs = []
            main_img_pk = ""
            #data["debug"] = ""
            for db_img in added_boat.images.all():
                if "selected_main_photo" in request.POST and str(db_img.boat_image).find(request.POST['selected_main_photo']) > -1:
                    main_img_pk = db_img.boat_image
                    #main_img_pk = db_img.pk
                else:
                    prev_imgs.append(db_img.boat_image)
                    #prev_imgs.append(db_img.pk)
                db_img.delete()
            # added_boat.images.clear()
            added_boat.save()

            # add the first and main image - if the image IS NOT new - OK
            if main_img_pk != "":
                # main_boat_image = BoatImages.objects.get(pk=main_img_pk)
                main_boat_image = BoatImages.objects.create(user=request.user, boat_image=main_img_pk)
                added_boat.images.add(main_boat_image)
                added_boat.save()

            # add the first and main image - if the image IS new
            for img in request.FILES.getlist('inp_pic'):
                if "selected_main_photo" in request.POST and str(img).find(request.POST['selected_main_photo']) > -1:
                    boat_image = BoatImages.objects.create(user=request.user, boat_image=img)
                    added_boat.images.add(boat_image)
                    added_boat.save()
                else:
                    prev_imgs.append(img)

            for saved_imgs in prev_imgs:
                img_to_add = BoatImages.objects.create(user=request.user, boat_image=saved_imgs)
                added_boat.images.add(img_to_add)

            if added_boat.pk:
                data['boat_message'] = "Embarcação salva com sucesso."
                data['boat_message_class'] = "alert-success"
            else:
                data['boat_message'] = "Ops, houve um erro no cadastro da sua embarcação. Favor tentar novamente."
                data['boat_message_class'] = "alert-danger"

        if 'boat_status' in request.POST:
            add_boat = ""
            if request.POST.get('boat_status') == "update":
                data['update_boat'] = Boat.objects.get(pk=request.POST.get('boat_id'))
                data['add_boat'] = "True"
            else:
                boat = Boat.objects.get(pk=request.POST.get('boat_id'))
                boat.status = request.POST.get('boat_status')
                boat.save()
                data['boat_message'] = "Embarcação alterada com sucesso."
                data['boat_message_class'] = "alert-success"

    # get years to form
    years = []
    for y in range(1900, datetime.datetime.now().year+1):
        years.append(y)
    data['years'] = sorted(years, reverse=True)

    # get boat sizes
    boat_sizes = []
    for s in range(10, 200):
        boat_sizes.append(s)
    data['boat_sizes'] = boat_sizes

    # get boat capacity options
    boat_capacity = []
    for c in range(1, 300):
        boat_capacity.append(c)
    data['boat_capacity'] = boat_capacity

    # get all states
    data['all_states'] = State.objects.all().order_by('name')

    data['boat_price_includes'] = BoatPriceIncludes.objects.all()

    data['boat_manufectors'] = ['Alumibarcos','Aqua Yachts','Armada Yachts','Arthmarine','ArtSol Náutica',
                                'Attalus Yacht','Atymar','Azimut Yachts','Bayliner Boats','Beneteau','BMYD Boats',
                                'Boreas Boats','Brasboats','Brazilian Boat','Caprice','Carbrasmar','Cat Boat',
                                'Chris Craft','Cimitarra','Cobra','Colunna Yachts','Coral','Corisco Lanchas',
                                'Costa Dourada Boats','Cranchi','Crownline','Diamar','Ecomariner','Esquimar',
                                'Euroboats','Evolution Boats','Evolve Boats','Fairline Boats','Fast Yachts',
                                'Ferretti','Fibrafort','Fibramar','Fibrasmar','Fishing','Force One Boats','Four Winns',
                                'FS Yachts','Glastron','HD Marine','Imperio Yachts (DM)','Intermarine',
                                'Kastigar amp Lenzi Yachts','Levefort','Luna Boats','Maestrale Yachts',
                                'Magna Estaleiros','Magnum Estaleiros','Mares Mar Azul','Mariner Boats','Maresias',
                                'Maxima Yachts','Mega Bass','Mestra Boats','MJ','Murano Yachts','NXBoats','Onix Yachts',
                                'Parcel Brasil','Perimar','Pershing','Phoenix Boats','Phoenix Vip','Pier ',
                                'Planet Boat','Portofino Yachts','Princess Yachts','Pro Boat','Quest Boats',
                                'Real Power Boats','Regal','Riostar','Royal Mariner','Runner','Schaefer Yachts',
                                'Sea Crest','Sea Ray','Sedna','Segue Yachts','Sessa Marine','Singular Boats',
                                'Solara - HF Marine','Sterling Yachts','Sunline Boats','Tecnoboats','Tecnomarine',
                                'Tethys','Top Boats','Top Sul Estaleiro','Triton Boats (Way Brasil)','Uniboat',
                                'Ventura','Walglass Nutica','Wellcraft (Dumar)','Yacxo Yachts', data['BoatType_6']]

    boat_amenities = BoatAmenities.objects.all()
    data['boat_amenities_t1'] = boat_amenities.filter(type="EL")
    data['boat_amenities_t2'] = boat_amenities.filter(type="CO")
    data['boat_amenities_t3'] = boat_amenities.filter(type="AA")
    data['boat_amenities_t4'] = boat_amenities.filter(type="LA")
    data['boat_amenities_t5'] = boat_amenities.filter(type="EQ")

    data['fish_species'] = BoatFishingSpecies.objects.all()

    if data['IsOwner']:
        user_captain_qry = CaptainProfile.objects.get(user=request.user.pk)
        data['CaptainForm'] = CaptainForm(instance=user_captain_qry)

    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    # Check if there is a boat creation request
    if add_boat == "add":
        captain_prof = CaptainProfile.objects.get_or_create(user=request.user)
        if not captain_prof[0].is_captaion:
            data['add_boat'] = "Add_CapProf"
        else:
            data['add_boat'] = "True"

    data["boat_types"] = BoatType.objects.all().order_by("pk")

    data['boats'] = Boat.objects.filter(user=request.user).exclude(status="Deleted")
    for boat in data['boats']:
        boat.status_id = boat.status
        boat.status = convert_status_id(boat.status)

    if request.user.username == "renangaspar@hotmail.com":
        data["debugy"] = "1"

    return render(request, "userarea_boats.html", data)


@csrf_exempt
def search_results(request, city="brasil"):
    data = {}
    capacity_filter = 0
    price_single_min = 0
    price_single_max = 999999
    price_hday_min = 0
    price_hday_max = 999999
    price_day_min = 0
    price_day_max = 999999
    price_overnight_min = 0
    price_overnight_max = 999999
    boat_category_arr = []
    filter_price = 0

    if "default_page" in request.session:
        data['boat_type_inp'] = request.session['default_page']
        data["f_category_class"] = "filter_inuse"
        boat_category = request.session['default_page']
        boat_category_arr = boat_category.split(";")
        data['home_type'] = request.session['default_page']

    # city search
    # if request.POST:
       # Search Boats by city request
    #    if 'search_city_name' in request.POST:
    #        city_name = request.POST['search_city_name']
    #        if city_name == "":
    #            city_name = 0
    #        return redirect('search_results', city=(city_name))

    # Sign in and Sign up function
    data.update(global_texts())
    data.update(signin_signup_func(request, data))
    if data['sms_error'] == "error":
        return redirect('user_profile')

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    # Update profile picture
    data.update(update_profile_pic(request))

    if request.POST:
        if 'search_boat_name' in request.POST:
            return redirect('barco_cidade', boat_id=request.POST['search_boat_id'], boat_city=request.POST['search_city_name'])
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            if request.POST['search_city_name'] != "":
                city = request.POST['search_city_name']
        if 'filter_city' in request.POST:
            if request.POST['filter_city'] != "":
                city = request.POST['filter_city']
        if 'filter_capacity' in request.POST:
            if request.POST['filter_capacity'] != "":
                # capacity_filter = {'{0}__{1}'.format('capacity', 'gte'): request.POST['filter_capacity'],}
                capacity_filter = request.POST['filter_capacity']
                data["filter_capacity"] = request.POST['filter_capacity']
                data["f_capacity_class"] = "filter_inuse"
        if 'filter_date_from' in request.POST:
            if request.POST['filter_date_from'] != "":
                data["filter_date_from"] = request.POST['filter_date_from']
                data["filter_date_to"] = request.POST['filter_date_to']
                data["f_date_class"] = "filter_inuse"
        if 'boat_type_inp' in request.POST:
            if request.POST['boat_type_inp'] != '':
                boat_category = request.POST['boat_type_inp']
                boat_category_arr = boat_category.split(";")
                data['boat_type_inp'] = boat_category
                data["f_category_class"] = "filter_inuse"
        if 'price_single' in request.POST:
            if request.POST['price_single'] != "":
                price_single = request.POST['price_single']
                price_single = price_single.replace("R$", "")
                price_single_arr = price_single.split(" - ")
                price_single_min = price_single_arr[0]
                data['price_single_min'] = price_single_min
                price_single_max = price_single_arr[1]
                data['price_single_max'] = price_single_max
        if 'price_hday' in request.POST:
            if request.POST['price_hday'] != "":
                price_hday = request.POST['price_hday']
                price_hday = price_hday.replace("R$", "")
                price_hday_arr = price_hday.split(" - ")
                price_hday_min = price_hday_arr[0]
                data['price_hday_min'] = price_hday_min
                price_hday_max = price_hday_arr[1]
                data['price_hday_max'] = price_hday_max
        if 'price_day' in request.POST:
            if request.POST['price_day'] != "":
                price_day = request.POST['price_day']
                price_day = price_day.replace("R$", "")
                price_day_arr = price_day.split(" - ")
                price_day_min = price_day_arr[0]
                data['price_day_min'] = price_day_min
                price_day_max = price_day_arr[1]
                data['price_day_max'] = price_day_max
        if 'price_overnight' in request.POST:
            if request.POST['price_overnight'] != "":
                price_overnight = request.POST['price_overnight']
                price_overnight = price_overnight.replace("R$", "")
                price_overnight_arr = price_overnight.split(" - ")
                price_overnight_min = price_overnight_arr[0]
                data['price_overnight_min'] = price_overnight_min
                price_overnight_max = price_overnight_arr[1]
                data['price_overnight_max'] = price_overnight_max
        if 'filter_price' in request.POST:
            if request.POST['filter_price'] != '':
                price_day = request.POST['filter_price']
                price_day = price_day.replace("R$", "")
                price_day_arr = price_day.split(" - ")
                price_day_min = price_day_arr[0]
                data['price_day_min'] = price_day_min
                price_day_max = price_day_arr[1]
                data['price_day_max'] = price_day_max

    # page texts
    data.update(results_texts())

    nearby_boats = []
    if city != "brasil":
        city_obj = City.objects.get(city__icontains=city)

        boats = Boat.objects.filter(Q(city__exact=city_obj) & Q(capacity__gte=capacity_filter) &
            (Q(price_single__gte=price_single_min, price_single__lte=price_single_max) | Q(price_single__exact=0)) &
            (Q(price_half_day__gte=price_hday_min, price_half_day__lte=price_hday_max) | Q(price_half_day__exact=0)) &
            (Q(price_overnight__gte=price_overnight_min, price_overnight__lte=price_overnight_max) | Q(price_overnight__exact=0)) &
            (Q(price_day__gte=price_day_min, price_day__lte=price_day_max) | Q(price_day__exact=0)) & Q(status="Published")
            ).exclude(Q(status="Paused") | Q(status="Deleted")).annotate(
            price_pperson_single=ExpressionWrapper(F('price_single') / F('capacity'), output_field=IntegerField()),
            price_pperson_hday=ExpressionWrapper(F('price_half_day') / F('capacity'), output_field=IntegerField()),
            price_pperson_day=ExpressionWrapper(F('price_day') / F('capacity'), output_field=IntegerField()),
            price_pperson_overnight=ExpressionWrapper(F('price_overnight') / F('capacity'), output_field=IntegerField()))

        counter = 0
        boats_qry_one = boats
        all_boats = Boat.objects.all()
        boats_qry_two = all_boats

        for cat in boat_category_arr:
            counter = counter + 1
            if counter == 1:
                if cat:
                    boats_qry_one = boats.filter(boat_type__sid_bt=cat)
                    boats_qry_two = all_boats.filter(boat_type__sid_bt=cat)
            else:
                if cat:
                    boats_qry_one = boats_qry_one | boats.filter(boat_type__sid_bt=cat)
                    boats_qry_two = boats_qry_two | all_boats.filter(boat_type__sid_bt=cat)

        boats = boats_qry_one
        all_boats = boats_qry_two

        for city in city_obj.nearby_cities.all():
            nearby_boats.extend(list(all_boats.filter(Q(city=city) & Q(capacity__gte=capacity_filter) &
                (Q(price_single__gte=price_single_min, price_single__lte=price_single_max) | Q(price_single__exact=0)) &
                (Q(price_half_day__gte=price_hday_min, price_half_day__lte=price_hday_max) | Q(price_half_day__exact=0)) &
                (Q(price_overnight__gte=price_overnight_min, price_overnight__lte=price_overnight_max) | Q(price_overnight__exact=0)) &
                (Q(price_day__gte=price_day_min, price_day__lte=price_day_max) | Q(price_day__exact=0)) & Q(status="Published")
                ).annotate(
                price_pperson_single=ExpressionWrapper(F('price_single') / F('capacity'), output_field=IntegerField()),
                price_pperson_hday=ExpressionWrapper(F('price_half_day') / F('capacity'), output_field=IntegerField()),
                price_pperson_day=ExpressionWrapper(F('price_day') / F('capacity'), output_field=IntegerField()),
                price_pperson_overnight=ExpressionWrapper(F('price_overnight') / F('capacity'), output_field=IntegerField()))))

        data["nearby_boats"] = nearby_boats
        data["city_name"] = city_obj.city + ", " + city_obj.state.name
        data['city_only'] = city_obj.city
    else:
        boats = Boat.objects.filter(Q(status="Published") & Q(capacity__gte=capacity_filter) &
            (Q(price_single__gte=price_single_min, price_single__lte=price_single_max) | Q(price_single__exact=0)) &
            (Q(price_half_day__gte=price_hday_min, price_half_day__lte=price_hday_max) | Q(price_half_day__exact=0)) &
            (Q(price_overnight__gte=price_overnight_min, price_overnight__lte=price_overnight_max) | Q(price_overnight__exact=0)) &
            (Q(price_day__gte=price_day_min, price_day__lte=price_day_max) | Q(price_day__exact=0)) & Q(status="Published")
            ).exclude(Q(status="Paused") | Q(status="Deleted")).annotate(
            price_pperson_single=ExpressionWrapper(F('price_single') / F('capacity'), output_field=IntegerField()),
            price_pperson_hday=ExpressionWrapper(F('price_half_day') / F('capacity'), output_field=IntegerField()),
            price_pperson_day=ExpressionWrapper(F('price_day') / F('capacity'), output_field=IntegerField()),
            price_pperson_overnight=ExpressionWrapper(F('price_overnight') / F('capacity'), output_field=IntegerField()),)

        counter = 0
        boats_qry_one = boats
        for cat in boat_category_arr:
            counter = counter + 1
            if counter == 1:
                if cat:
                    boats_qry_one = boats.filter(boat_type__sid_bt=cat)
            else:
                if cat:
                    boats_qry_one = boats_qry_one | boats.filter(boat_type__sid_bt=cat)
        boats = boats_qry_one

    data["boats"] = boats
    data.update(get_price_min_max())
    request.session['default_page'] = ""

    return render(request, "search_results.html", data)


def boat_view(request, boat_id="0", boat_city="", boat_name=""):
    data = {}

    # page texts
    data.update(bview_texts())
    data.update(global_texts())
    data['pag_token'] =  paggcerto_gettoken()
    data['Booking_Alert_Class'] = "hideOnly"
    data['Message_Alert_Class'] = "hideOnly"

    # city search
    if request.POST:
        if 'search_boat_id' in request.POST and boat_id=="0":
            boat_id = request.POST['search_boat_id']

        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = 0
            return redirect('search_results', city=(city_name))

    # city search
    if request.GET:

        if "boat_pk" in request.GET and (boat_id=="0" or boat_id==""):
            boat_id = request.GET["boat_pk"]

        if 'id' in request.GET and (boat_id=="0" or boat_id==""):
            boat_id = request.GET['id']

    # Sign in and Sign up function
    data.update(signin_signup_func(request, data))
    if data['sms_error'] == "error":
        return redirect('user_profile')

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    if boat_id == "" or boat_id == "0":
        boat_rescue_search = Boat.objects.filter(title__contains=boat_name.replace("_", " "), city__city__contains=boat_city)
        if boat_rescue_search.count() == 0:
            send_mail("boat_id empty", boat_id + "_" + boat_city + "_" + boat_name, "contato@bnboats.com", ["renangasp@gmail.com"], fail_silently=True)
            if boat_city == "":
                boat_city = "brasil"
            return redirect('search_results', city=(boat_city))
        else:
            boat_id = boat_rescue_search[0].pk


    Boats_Query = Boat.objects.get(pk=boat_id)

    data['reviews'] = Review.objects.filter(boat=Boats_Query)

    # get boat sizes
    boat_sizes = []
    s=1
    for s in range(1, Boats_Query.capacity):
        boat_sizes.append(s)
    boat_sizes.append(s+1)
    data['boat_sizes'] = boat_sizes

    data['Boats_Query'] = Boats_Query

    data['bookings'] = ""
    blocked_dates = BoatBlockedDates.objects.filter(boat=Boats_Query)
    if blocked_dates.count() == 1:
        data['bookings'] = blocked_dates[0].blocked_dates

    if request.user.is_anonymous:
        data['Anonymous_User_Block_Class'] = 'disabled'
        data['Booking_Alert_Class'] = 'alert-warning'
        data['Booking_Alert_Message'] = "<a href='#' onclick='modalSignIn()' data-toggle='modal' data-target='#modal_login'>Clique aqui</a> para entrar com suas credenciais antes de realizar uma reserva."
        data['Anonymous_User_Block_Message_Class'] = 'disabled'
        data['Message_Alert_Class'] = 'alert-warning'
        data['Message_Alert_Message'] = "<a href='#' onclick='modalSignIn()' data-toggle='modal' data-target='#modal_login'>Clique aqui</a> para entrar com suas credenciais antes de enviar uma mensagem ao proprietário."
    else:
        if is_user_profile_complete(request.user) == False:
            data['Anonymous_User_Block_Class'] = 'disabled'
            data['Booking_Alert_Class'] = 'alert-danger'
            data['Booking_Alert_Message'] = "<a href='/meu-perfil'>Clique aqui</a> para completar seu perfil antes de realizar uma reserva."
        if request.user.userprofile.fishing_discount:
            data['strike'] = "text-decoration: line-through;"
            data['discount'] = FISHING_STORES_DISCOUNT
            data['disc_price_single'] = Boats_Query.price_single - FISHING_STORES_DISCOUNT
            data['disc_price_hday'] = Boats_Query.price_half_day - FISHING_STORES_DISCOUNT
            data['disc_price_day'] = Boats_Query.price_day - FISHING_STORES_DISCOUNT
            data['disc_price_overnight'] = Boats_Query.price_overnight - FISHING_STORES_DISCOUNT


    return render(request, "boat_view.html", data)


def terms_page(request):
    data = {}

    data.update(global_texts())

    # city search
    if request.POST:
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = 0
            return redirect('search_results', city=(city_name))

    # Sign in and Sign up function
    data.update(signin_signup_func(request, data))

    return render(request, "terms.html", data)


def privacy_policy(request):
    data = {}

    data.update(global_texts())

    # city search
    if request.POST:
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = 0
            return redirect('search_results', city=(city_name))

        if request.user.is_superuser:
            if "username" in request.POST:
                logout(request)
                user_tologin = User.objects.get(username=request.POST["username"])
                login(request, user_tologin)
                return redirect('home')

    # Sign in and Sign up function
    data.update(signin_signup_func(request, data))

    return render(request, "privacy_policy.html", data)


# ---------------------------------  FUNCTIONS ----------------------------------------------------------


def is_user_owner(user_id):
    # user_captain = CaptainProfile.objects.get(user=user_id)
    user_cap = CaptainProfile.objects.filter(user=user_id)
    if not user_cap:
        user_captain = False
    else:
        if not user_cap[0].is_captaion:
            user_captain = False
        else:
            user_captain = True

    return user_captain


def captain_setup(request):
    data = {}
    data['CaptainForm'] = CaptainForm()

    if request.POST:
        if 'is_captaion' in request.POST:
            CaptainProfile.objects.get_or_create(user=request.user)
            form = CaptainForm(request.POST, instance=request.user.captainprofile)
            if form.is_valid():
                form.save()
            else:
                data['alert_message'] = form.errors
                data['alert_classes'] = 'alert-danger'

    data['IsOwner'] = is_user_owner(request.user.pk)
    if not data['IsOwner']:
        data['hideToClients'] = "hideOnly"

    return data


def convert_status_id(status_id):
    status_desc = "Error"
    status_descs = {}
    status_descs.update(userarea_texts())
    if status_id == "New":
        status_desc = status_descs['Status_30']
    if status_id == "PaymentPending":
        status_desc = status_descs['Status_30']
    if status_id == "Paid":
        status_desc = status_descs['Status_40']
    if status_id == "Confirmed":
        status_desc = status_descs['Status_50']
    if status_id == "Cancelled":
        status_desc = status_descs['Status_60']
    if status_id == "InReview":
        status_desc = status_descs['Status_10a']
    if status_id == "Published":
        status_desc = status_descs['Status_20a']
    if status_id == "Paused":
        status_desc = status_descs['Status_30a']
    if status_id == "Deleted":
        status_desc = status_descs['Status_40a']

    return status_desc


def create_booking(request):
        # booking
        booking_kwargs = {}
        booking_id = ""
        cust_city_code = ""
        city_code = ""
        area = ""
        street = ""
        street_no = ""
        postcode = ""
        doc_no = ""

        if 'booking_type' in request.GET:
            booking_type = request.GET.get('booking_type')
            booking_date_from = datetime.datetime.strptime(request.GET.get('booking_date_from'), '%d/%m/%Y').strftime('%Y-%m-%d')
            if request.GET.get('booking_date_to'):
                booking_date_to = datetime.datetime.strptime(request.GET.get('booking_date_to'), '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                booking_date_to = booking_date_from
            booking_pax = request.GET.get('booking_pax')
            boat_pk = request.GET.get('boat_pk')
            boat = Boat.objects.get(pk=boat_pk)
            if booking_type == "2":
                booking_total = boat.price_single
            if booking_type == "4":
                booking_total = boat.price_half_day
            if booking_type == "8":
                booking_total = boat.price_day
            if booking_type == "24":
                booking_total = boat.price_overnight
            # apply fishing discount if thats the case
            if request.user.userprofile.fishing_discount:
                booking_total = booking_total - FISHING_STORES_DISCOUNT
                request.user.userprofile.fishing_discount = False
                request.user.userprofile.save()
            #booking_total = float(request.GET.get('booking_total_price'))
            booking_kwargs = {"boat": boat,
                              "customer": request.user,
                              "date_from": booking_date_from,
                              "date_to": booking_date_to,
                              "total_cost": booking_total,
                              "no_passengers": booking_pax,
                              "booking_period": booking_type,
                              "status": "New"}
            booking_id = Booking.objects.create(**booking_kwargs)
            sendEmail(request.user, "admin", {"subject": "Reserva realizada", "message": "Nova reserva criada sob "
                "número " + str(booking_id.pk) + ", feita pelo cliente " + str(request.user.username) + " para o "
                "proprietário " + str(boat.user.username)})
            # update boat prices
            Booked_boat = Boat.objects.get(pk=boat_pk)
            Booked_boat.has_discount = "No"
            bnboats_tax = BNBOATS_TAX # 1.185
            Booked_boat.price_single = float(Booked_boat.owner_price_single) * bnboats_tax
            Booked_boat.price_half_day = float(Booked_boat.owner_price_half_day) * bnboats_tax
            Booked_boat.price_day = float(Booked_boat.owner_price_day) * bnboats_tax
            Booked_boat.price_overnight = float(Booked_boat.owner_price_overnight) * bnboats_tax
            Booked_boat.save()

            # Add booking dates to blocked dates table
            BlockedDates_ForBoat = BoatBlockedDates.objects.get_or_create(boat=boat)[0]
            BlockedDates = BlockedDates_ForBoat.blocked_dates
            BlockedDates_ForBoat.blocked_dates = BlockedDates + booking_date_from + "_" + booking_date_to + ";"
            BlockedDates_ForBoat.save()

            # grap booking info to send emails and SMS
            booking_data = {
                "owner": Booked_boat.user.first_name,
                "date_from": request.GET.get('booking_date_from'),
                "date_to": request.GET.get('booking_date_to'),
                "city": Booked_boat.city,
                "no_passangers": booking_pax,
                "booking_id": booking_id.pk,
                "customer": request.user.first_name
            }
            sendEmail(boat.user, 4, booking_data)
            sendEmail(request.user, 3, booking_data)
            send_sms(boat.user, 3, {"date_from": request.GET.get('booking_date_from')})

        # send client and booking data back to the front end
        if request.user is not None:
            if request.user.userprofile.address_city == "":
                city_code = IBGECityCodes.objects.get(id=5265)
            else:
                city_code = IBGECityCodes.objects.filter(name__icontains=request.user.userprofile.address_city)[0]
            area = request.user.userprofile.address_area
            street = request.user.userprofile.address_street
            street_no = request.user.userprofile.address_number
            postcode = request.user.userprofile.address_postcode
            doc_no = request.user.userprofile.doc_number

        return JsonResponse({"city_code": city_code.ibge_id, "booking_id": booking_id.pk, "city_area": area, "street": street,
                             "street_no": street_no, "postcode": postcode, "doc_no": doc_no, "booking_total": booking_total}) # HttpResponse(booking_id.pk)


def create_extra_activity(request):
    new_values = request.GET.get('new_values')
    if new_values:
        arr_new_values = new_values.split(',')
        for value in arr_new_values:
            if value:
                CaptainExtraActivities.objects.get_or_create(activity=value, sid_cea=value[:3].upper())
        return HttpResponse(arr_new_values[0]) # JsonResponse(arr_new_values)


def load_allcities(request):
    data = {}

    if request.user.is_authenticated:
        user_name = request.user.first_name.split(' ')[0]
        data['first_name'] = user_name

    qry_cities = City.objects.select_related('state').order_by('-state')
    res_cities = []
    res_all_cities = defaultdict(list)
    for city in qry_cities:
        res_cities.append(city.city + " - " + city.state.name + "_ " + city.state.country)
        res_all_cities[city.state.name].append(city.city)

    data['cityList'] = res_cities
    data['res_all_cities'] = dict(res_all_cities)

    return data


def add_to_favorities(request):
    boat_id = request.GET.get('boat_id', None)

    boat = Boat.objects.get(pk=boat_id)

    if boat_id:
       BoatFavorite.objects.get_or_create(user=request.user, boat=boat)

    return HttpResponse("done")


def get_price_min_max():
    data = {}

    all_boats = Boat.objects.all()

    boat_single_price_min = all_boats.filter(price_single__gt=0).annotate(
        price_single_min=Min('price_single')).order_by("price_single")
    if len(boat_single_price_min) == 0:
        boat_single_price_min[0] = 0
    boat_single_price_max = all_boats.filter(price_single__gt=0).annotate(
        price_single_max=Max('price_single')).order_by("-price_single")
    if len(boat_single_price_max) == 0:
        boat_single_price_max[0] = 0

    boat_hday_price_min = all_boats.filter(price_half_day__gt=0).annotate(
        price_hday_min=Min('price_half_day')).order_by("price_half_day")
    if len(boat_hday_price_min) == 0:
        boat_hday_price_min[0] = 0
    boat_hday_price_max = all_boats.filter(price_half_day__gt=0).annotate(
        price_hday_max=Max('price_half_day')).order_by("-price_half_day")
    if len(boat_hday_price_max) == 0:
        boat_hday_price_max[0] = 0

    boat_day_price_min = all_boats.filter(price_day__gt=0).annotate(
        price_day_min=Min('price_day')).order_by("price_day")
    if len(boat_day_price_min) == 0:
        boat_day_price_min[0] = 0
    boat_day_price_max = all_boats.filter(price_day__gt=0).annotate(
        price_day_max=Max('price_day')).order_by("-price_day")
    if len(boat_day_price_max) == 0:
        boat_day_price_max[0] = 0

    boat_overnight_price_min = all_boats.filter(price_overnight__gt=0).annotate(
        price_overnight_min=Min('price_overnight')).order_by("price_overnight")
    if len(boat_overnight_price_min) == 0:
        boat_overnight_price_min[0] = 0
    boat_overnight_price_max = all_boats.filter(price_overnight__gt=0).annotate(
        price_overnight_max=Max('price_overnight')).order_by("-price_overnight")
    if len(boat_overnight_price_max) == 0:
        boat_overnight_price_max[0] = 0

    data["boat_single_price_min"] = boat_single_price_min[0]
    data["boat_single_price_max"] = boat_single_price_max[0]

    data["boat_hday_price_min"] = boat_hday_price_min[0]
    data["boat_hday_price_max"] = boat_hday_price_max[0]

    data["boat_day_price_min"] = boat_day_price_min[0]
    data["boat_day_price_max"] = boat_day_price_max[0]

    data["boat_overnight_price_min"] = boat_overnight_price_min[0]
    data["boat_overnight_price_max"] = boat_overnight_price_max[0]

    return data


def update_profile_pic(request):
    data = {}
    data.update(userarea_texts())

    # Change photo
    if 'image' in request.FILES:
        form = UploadUserPhotoForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            data['alert_message'] = data['UploadPhotoSuccessfully']
            data['alert_classes'] = 'alert-success'
        else:
            data['alert_message'] = form.errors
            data['alert_classes'] = 'alert-danger'

    return data


def how_it_works(request):
    data = {}

     # page texts
    data.update(how_it_works_texts())

    # get page texts
    data.update(global_texts())

    # city search
    if request.POST:
        # Search Boats by city request
        if 'search_city_name' in request.POST:
            city_name = request.POST['search_city_name']
            if city_name == "":
                city_name = 0
            return redirect('search_results', city=(city_name))

    # Sign in and Sign up function
    data.update(signin_signup_func(request, data))
    if data['sms_error'] == "error":
        return redirect('user_profile')

    # Check if user is an owner, prepare owner setup
    data.update(captain_setup(request))

    # print(data.Questions);

    return render(request, "how_it_works.html", data)


def create_invoice(request):
    data = {}
    query_params = {}
    if 'booking_id' in request.GET:
        booking_id = request.GET.get('booking_id')
        booking_id = booking_id.split("_")[0]
        payment_id = request.GET.get('payment_id')
        payment_method = request.GET.get('payment_method')
        payment_status = request.GET.get('payment_status')
        payment_ccard_brand = request.GET.get('payment_ccard_brand')
        payment_ccard_no = request.GET.get('payment_ccard_no')
        payment_total = request.GET.get('payment_total')
        payment_paid_on = request.GET.get('payment_paid_on')

        booking = Booking.objects.get(pk=booking_id)
        query_params = {"booking": booking}
        query_params.update({"payment_code": payment_id})
        query_params.update({"payment_method": payment_method})
        query_params.update({"payment_api_status": payment_status})
        if payment_ccard_brand != "":
            query_params.update({"payment_ccard_brand": payment_ccard_brand.title()})
            query_params.update({"payment_ccard_no": payment_ccard_no})
        if payment_paid_on != "":
            query_params.update({"paid_on_date": payment_paid_on})
        query_params.update({"payment_total": payment_total})
        if payment_status == "paid":
            query_params.update({"is_paid": True})
            booking.status = 'Paid'
            booking.save()
        else:
            query_params.update({"is_paid": False})
            booking.status = 'PaymentPending'
            booking.save()

        invoice_no = Invoice.objects.create(**query_params)

        return HttpResponse(invoice_no.pk)


def send_message(request):
    created_msg = ""

    if 'owner_id' in request.GET:
        owner_id = request.GET.get('owner_id')
        dest = User.objects.get(pk=owner_id)
        sender = request.user
        message_text = request.GET.get('message_text')
        created_msg = Message.objects.create(msg_from=sender, msg_to=dest, message=message_text)
        sendEmail(dest, 10, "")
        send_sms(dest, 6, "")

    return HttpResponse(created_msg.pk)


def send_sms(user, msg_type, data=None):

    if config("ENVIRONMENT") != "PROD":
        return

    cliente = Cliente("7c58f0809e6ad4b929bb90043e475d77", 'https://api.totalvoice.com.br')  # ex: api.totalvoice.com.br

    receiver = user.username
    mensagem = ""
    numero_destino = str(user.userprofile.mobile_area) + str(user.userprofile.mobile_number)

    if str(user.userprofile.gender).upper() == "F":
        gender = "a"
    else:
        gender = "o"

    # user setup - code confirmation
    if msg_type == 1:
        mensagem = "Bnboats: Saudações Marinheiras, segue seu código de confirmação de cadastro na Bnboats: " + str(user.userprofile.mobile_code)

    # new message
    if msg_type == 2:
        mensagem = "Bnboats: Você recebeu uma mensagem.\n"
        mensagem += "Para ler e responder, acesse www.bnboats.com/mensagens"

    # booking done to owner
    if msg_type == 3:
        mensagem = "Bnboats: Você recebeu uma solicitação de aluguel do seu barco para o dia " + str(data['date_from']) + "\n"
        mensagem += "Acesse www.bnboats.com/reservas-recebidas para aprovar"

    # approved booking - to customer
    if msg_type == 4:
        mensagem = "Bnboats: O Capitão aceitou sua solicitação.\n"
        mensagem += "Entre em contato com ele, através de seu telefone " + str(data['mobile']) + " para organizar os detalhes de embarque."

    # rejected booking - to customer
    if msg_type == 5:
        mensagem = "Bnboats: O Capitão não poderá navegar com você.\n"
        mensagem += "Mas não esquenta, tenta reservar outro barco na Bnboats: www.bnboats.com"

    # new msg from boats page
    if msg_type == 6:
        mensagem = "Bnboats: Tem gente interessada em alugar seu barco que te enviou uma mensagem.\n"
        mensagem += "Para ler e responder, acesse www.bnboats.com/mensagens"

    # forgot password
    if msg_type == 7:
        mensagem = "Bnboats: Nós recebemos um pedido para mudança da sua senha.\n"
        mensagem += "Para acessar www.bnboats.com, utilize sua nova senha:\n\n" + str(data['password'])

    # approved booking - to owner
    if msg_type == 9:
        mensagem = "Bnboats: Você aceitou a solicitação de reserva de " + str(data['customer_name']) + ".\n"
        mensagem += "Entre em contato com ele, através de seu telefone " + str(data['mobile']) + " para organizar os detalhes de embarque."

    # forgot password
    if msg_type == 10:
        mensagem = "Bnboats: Nós recebemos um pedido para mudança da sua senha.\n"
        mensagem += "Para acessar www.bnboats.com, utilize sua nova senha:\n\n" + str(data['password'])

    # password updated
    if msg_type == 12:
        mensagem = "Bnboats: Sua senha foi alterada.\n"
        mensagem += "Se você não fez essa mudança, verifique sua conta em www.bnboats.com"

    if numero_destino != "" and mensagem != "":
        # Send sms
        response = cliente.sms.enviar(numero_destino, str(mensagem))
    else:
        response = False
    # mensagem = "teste 2: " + mensagem
    # mensagem = mensagem.encode("utf-8").decode("utf-8")
    # response = cliente.sms.enviar(numero_destino, mensagem)
    return response

    # Get sms
    # id = "1958"
    # response = cliente.sms.get_by_id(id)
    # print(response)

    # Relatório de sms
    # data_inicio = "2019-08-30T00:01:00-03:00"
    # data_fim = "2019-08-30T17:15:59-03:00"
    # response = cliente.sms.get_relatorio(data_inicio, data_fim)
    # print(response)


def randomDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def sendEmail(user, email_type, data=None):

    if config("ENVIRONMENT") != "PROD":
        return

    if email_type == "admin":
        send_mail(
            data['subject'],
            data['message'],
            "contato@bnboats.com",
            ["contato@bnboats.com"],
            fail_silently=True,
        )
        return

    receiver = user.username
    rec_name = user.first_name
    rec_name_arr = rec_name.split(" ")
    rec_name = rec_name_arr[0]
    sender = 'contato@bnboats.com'
    subject = ""
    body = ""

    if str(user.userprofile.gender).upper() == "F":
        gender = "a"
    else:
        gender = "o"

    # new user
    if email_type == 1:
        subject = "Bem-vind"+gender+" a Bnboats! Seu usuário foi criado com sucesso"
        body = "Opa, estou escrevendo esse e-mail para avisa-l"+gender+" que criei seu usuário no nosso site " \
               "www.bnboats.com.\n\nAgora é só acessar, informar seu e-mail '"+receiver+"', senha cadastrada e procurar" \
               " sua primeira embarcação para navegar.\n\n\nAtt.,\nTripulação Bnboats"

    # message
    if email_type == 2:
        subject = rec_name + " chegou uma mensagem para você"
        body = "Olá " + rec_name + "\n\n"
        body += "Você recebeu uma mensagem do(a) " + str(data['to_user']) + ":\n\n"
        body += str(data['msg'])
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking done - owner
    if email_type == 3:
        subject = "Solicitação de reserva efetuada - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Sua solicitação foi enviada. \nO proprietário " + str(data['owner']) + " irá te responder em breve.\n\n"
        body += "Reserva sob número " + str(data['booking_id']) + ":"
        body += "\nDia " + str(data['date_from'])
        body += "\nLocal " + str(data['city'])
        body += "\nPara " + str(data['no_passangers']) + " pessoas"
        body += "\n\nPara verificar sua reserva, acesse https://www.bnboats.com/minhas-reservas"
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking done - client
    if email_type == 4:
        subject = "Solicitação de reserva para aluguel da sua embarcação - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Você recebeu uma solicitação para aluguel do seu barco de " + str(data['customer']) + ".\n\n"
        body += "Reserva sob número " + str(data['booking_id']) + ":"
        body += "\nDia " + str(data['date_from'])
        body += "\nLocal " + str(data['city'])
        body += "\nPara " + str(data['no_passangers']) + " pessoas"
        body += "\n\nAcesse https://www.bnboats.com/reservas-recebidas para aprovar a solicitação e entrar em contato com o cliente."
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking approved - client
    if email_type == 5:
        subject = "Reserva confirmada - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "O proprietário " + str(data['owner']) + " aceitou sua solicitação de reserva.\n"
        body += "Entre em contato com ele para organizar os detalhes para embarque."
        body += "Reserva sob número " + str(data['booking_id']) + ":"
        body += "\nDia " + str(data['date_from'])
        body += "\nLocal " + str(data['city'])
        body += "\nPara " + str(data['no_passangers']) + " pessoas"
        body += "\n\nPara verificar sua reserva, acesse https://www.bnboats.com/minhas-reservas"
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking rejected
    if email_type == 6:
        subject = "Solicitação declinada para " + str(data['boat_name'])
        body = "Olá " + rec_name + "\n\n"
        body += "O proprietário " + str(data['owner']) + " não poderá navegar com você.\n"
        body += "Mas não esquenta, tenta reservar outro barco."
        body += "Aqui está um lembrete dos detalhes da sua última busca."
        body += "\nDia " + str(data['date_from'])
        body += "\nLocal " + str(data['city'])
        body += "\nPara " + str(data['no_passangers']) + " pessoas"
        body += "\n\nPara realizar uma nova reserva, acesse https://www.bnboats.com/procurar"
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # forgot password
    if email_type == 7:
        new_pass = (randomStringDigits(3) + "1" + randomStringDigits(4)).lower()
        user.set_password(new_pass)
        user.save()
        send_sms(user, 7, {"password": new_pass})
        subject = "Mudança de senha"
        body = "Olá " + rec_name + "\n\n"
        body += "Nós recebemos um pedido para mudança de sua senha, portanto a resetamos para:" + "\n\n" + new_pass
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking approved - owner
    if email_type == 8:
        subject = "Reserva confirmada - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Você aceitou a solicitação de reserva de " + str(data['customer']) + "\n"
        body += "Entre em contato com ele para organizar os detalhes do passeio. Seu telefone é " + str(data['cust_mobile'])
        body += "Reserva sob número " + str(data['booking_id']) + ":"
        body += "\nDia " + str(data['date_from'])
        body += "\nLocal " + str(data['city'])
        body += "\nPara " + str(data['no_passangers']) + " pessoas"
        body += "\n\nPara verificar sua reserva, acesse https://www.bnboats.com/reservas-recebidas"
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # booking rejected - owner
    if email_type == 9:
        subject = "Solicitação de reserva declinada - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Você cancelou a solicitação de reserva de " + str(data['customer']) + "\n"
        body += "Se certifique que os dados da sua embarcação estão atualizados assim como as datas disponíveis no calendário.\n\n"
        body += "Acesse seu barco neste link https://www.bnboats.com/barco/" + str(data['boat_id'])
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # message sent from boat page
    if email_type == 10:
        subject = "Alguém está interessado no seu barco - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Tem gente interessada em alugar seu barco que te enviou uma mensagem.\n"
        body += "Acesse https://www.bnboats.com/mensagens para ler e responder."
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # message sent from boat page
    if email_type == 11:
        subject = "Reserva Cancelada - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += str(data['customer']) + " cancelou a reserva.\n"
        body += "Acesse https://www.bnboats.com/ para ler nossa política de cancelamento."
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    # discount for user signup coming from fishing store
    if email_type == 12:
        subject = "Aqui está seu desconto - Bnboats"
        body = "Olá " + rec_name + "\n\n"
        body += "Gostaria de confirmar seu desconto de R$ " + str(FISHING_STORES_DISCOUNT) + ",00.\n\n"
        body += "Esse desconto será válido na sua primeira reserva e será aplicado diretamente no momento do pagamento.\n\n"
        body += "Acesse https://www.bnboats.com/procurar/ para encontrar uma embarcação."
        body +=  "\n\n\nGrande Abraço,\nTripulação Bnboats."

    if subject != "":
        send_mail(subject, body, sender, [receiver], fail_silently=True)

    pass

def forgot_password(request):
    process_complete = "nok"
    try:
        user_db = User.objects.get(username=request.GET['email'])
        if user_db:
            sendEmail(user_db, 7)
            process_complete = "ok"
    except ObjectDoesNotExist:
        process_complete = "nok"

    return JsonResponse({"status": process_complete})


def signin_signup_func(request, data):
    # data = {}
    # data['test'] = "test"
    data['sms_error'] = ""

    # get all cities from db
    data.update(load_allcities(request))

    # signup and signin forms
    data['SignUpForm'] = SignUpForm()
    data['SignInForm'] = SignInForm()
    data['SignInFormVisibilityClass'] = ""
    data['SignUpFormVisibilityClass'] = "hideOnly"

    # forms submits
    if request.POST:

        # signup
        if 'first_name' in request.POST:
            form = SignUpForm(request.POST)
            # if signup form is valid
            if form.is_valid():
                user = None
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.userprofile.mobile_country = form.cleaned_data.get('mobile_country')
                user.userprofile.mobile_area = form.cleaned_data.get('mobile_area')
                user.userprofile.mobile_number = form.cleaned_data.get('mobile_number')
                user.userprofile.mobile_code = str(randomDigits(5))
                user.userprofile.fishing_client = form.cleaned_data.get('fishing_client')
                user.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)

                # if signup and signin is successfully
                if user is not None:
                    sendEmail(user, "admin", {"subject": "Usuário Novo", "message": "Novo usuário criado: " + user.username})
                    data.update({"LogonFormMsgClass": "hideOnly"})
                    user_name = user.first_name.split(" ")[0]
                    data['first_name'] = user_name
                    data['user_created'] = 'true'
                    updated_user = User.objects.get(pk=request.user.pk)
                    send_sms(updated_user, 1)
                    sendEmail(updated_user, 1)
                    if user.userprofile.fishing_client != "":
                        user.userprofile.fishing_discount = True
                        user.userprofile.save()
                        sendEmail(updated_user, 12)
                    data["SignUpForm"] = form
                    if request.POST['add_boat'] == 'true':
                        data['add_boat'] = 'true'
                else:
                    data['SignInFormVisibilityClass'] = "hideOnly"
                    data['SignUpFormVisibilityClass'] = ""
                    data.update({"LogonFormMsg": "Erro no cadastro. Por favor, tente novamente."})
                    data.update({"LogonFormMsgClass": "alert-danger"})

            # if signup form has errors
            else:
                error_dict = form.errors
                form.password1 = ""
                form.password2 = ""

                if 'first_name' in error_dict:
                    error_dict[data['FullName']] = error_dict.pop("first_name")
                    form.first_name = ""
                if 'username' in error_dict:
                    error_dict[data['Email']] = error_dict.pop("username")
                    error_dict[data['Email']][0] = "E-mail já está em uso ou é inválido, favor alterar."
                if 'password2' in error_dict:
                    error_dict[data['ConfirmPassword']] = error_dict.pop("password2")
                if 'password1' in error_dict:
                    error_dict[data['Password']] = error_dict.pop("password1")
                if 'password' in error_dict:
                    error_dict[data['Password']] = error_dict.pop("password")
                if 'mobile_country' in error_dict:
                    error_dict[data['MobileCountry']] = error_dict.pop("mobile_country")
                    form.mobile_country = ""
                if 'mobile_area' in error_dict:
                    error_dict[data['MobileArea']] = error_dict.pop("mobile_area")
                    form.mobile_area = ""
                if 'mobile_number' in error_dict:
                    error_dict[data['Mobile']] = error_dict.pop("mobile_number")
                    form.mobile_number = ""
                data['SignInFormVisibilityClass'] = "hideOnly"
                data['SignUpFormVisibilityClass'] = ""
                data.update({"LogonFormMsg": error_dict})
                data.update({"LogonFormMsgClass": "alert-danger"})
                data["SignUpForm"] = form

        # if submit form is NOT signup
        else:
            # if submit form is Login
            if 'username' in request.POST:
                username = request.POST['username']
                if 'password' in request.POST:
                    password = request.POST['password']
                if 'password1' in request.POST:
                    password = request.POST['password1']
                user = authenticate(request, username=username, password=password)
                # if login is successfully
                if user is not None:
                    try:
                        login(request, user)
                    except ObjectDoesNotExist:
                        pass
                    data.update({"LogonFormMsgClass": "hideOnly"})
                    user_name = user.first_name.split(" ")[0]
                    data['first_name'] = user_name
                    if request.POST['add_boat'] == 'true':
                        data['add_boat'] = 'true'
                        data['next'] = "user_boats"
                        data['next_param'] = "add"
                # if login is NOT successfully
                else:
                    data['SignInFormVisibilityClass'] = ""
                    data['SignUpFormVisibilityClass'] = "hideOnly"
                    data.update({"LogonFormMsg": data['Login_AuthError']})
                    data.update({"LogonFormMsgClass": "alert-danger"})
                    # Return an 'invalid login' error message.

            # if mobile sms is sent to be confirmed, here is the validation
            if 'mobile_code' in request.POST:
                userprofile = UserProfile.objects.get(user=request.user)
                if str(request.POST['mobile_code']).lower() == str(userprofile.mobile_code).lower():
                    userprofile.mobile_confirmed = True
                    userprofile.save()
                else:
                    data['SignInFormVisibilityClass'] = ""
                    data['SignUpFormVisibilityClass'] = "hideOnly"
                    data.update({"LogonFormMsg": "Código inválido. Por favor, tente novamente."})
                    data.update({"LogonFormMsgClass": "alert-danger"})
                    data['sms_error'] = "error"
                if request.user is not None and request.POST['add_boat'] == 'true':
                    data['next'] = "user_boats"
                    data['next_param'] = "add"

    return data


def is_user_profile_complete(user):
    is_complete = False
    if user.first_name is None or user.userprofile.mobile_number is None or user.userprofile.address_city is None or \
            user.userprofile.doc_number is None or user.first_name == "" or user.userprofile.mobile_number == "" or \
            user.userprofile.address_city == "" or user.userprofile.doc_number == "":
        is_complete = False
    else:
        is_complete = True

    return is_complete


def handler404(request, exception=None):
    return render(request, 'home.html', status=404)


def handler500(request, exception=None):
    # send_mail("ERRO 500", "", "contato@bnboats.com", ["renangasp@gmail.com"], fail_silently=True)
    return render(request, 'home.html', status=500)


@login_required
def get_boat_details(request):

    boat_no = request.GET.get('boat_no')

    # GET BOAT RAW DATA - NO RELATIONSHIPS
    boat = Boat.objects.filter(pk=boat_no, user=request.user)
    boat_details = boat.values().first()

    # SET BOAT TO AN OBJECT TO EXTRACT RELATIONSHIPS
    boat_object = Boat.objects.get(pk=boat_no, user=request.user)

    # GET AMENITIES
    amenit_lst = ""
    boat_amenities = boat_object.boat_amenities.all()
    for amenit in boat_amenities:
        amenit_lst = amenit_lst + amenit.name + ","
    boat_details["amenities"] = amenit_lst

    # GET CITIY AND STATE
    boat_details["city_name"] = boat_object.city.city
    boat_details["state_name"] = boat_object.city.state.name

    # GET IMAGES
    boat_images = boat_object.images.all()
    img_lst = ""
    for img in boat_images:
        img_lst = img_lst + STATIC_URL + img.boat_image.name + ","
    boat_details["images"] = img_lst

    # GET SINGLE PRICE INCLUDES
    boat_single_includes = boat_object.p_single_includes.all()
    single_includes_lst = ""
    for sincludes in boat_single_includes:
        single_includes_lst = single_includes_lst + sincludes.name + ","
    boat_details["boat_single_includes"] = single_includes_lst

    # GET HALF DAY PRICE INCLUDES
    boat_hday_includes = boat_object.p_hday_includes.all()
    hday_includes_lst = ""
    for hincludes in boat_hday_includes:
        hday_includes_lst = hday_includes_lst + hincludes.name + ","
    boat_details["boat_hday_includes"] = hday_includes_lst

    # GET DAY PRICE INCLUDES
    boat_day_includes = boat_object.p_day_includes.all()
    day_includes_lst = ""
    for dincludes in boat_day_includes:
        day_includes_lst = day_includes_lst + dincludes.name + ","
    boat_details["boat_day_includes"] = day_includes_lst

    # GET DAY PRICE INCLUDES
    boat_overnight_includes = boat_object.p_overnight_includes.all()
    overnight_includes_lst = ""
    for dincludes in boat_overnight_includes:
        overnight_includes_lst = overnight_includes_lst + dincludes.name + ","
    boat_details["boat_overnight_includes"] = overnight_includes_lst

    # GET FISH SPECIES
    fish_species = boat_object.fish_species.all()
    fish_species_lst = ""
    for fspecies in fish_species:
        fish_species_lst = fish_species_lst + fspecies.name + ","
    boat_details["fish_species"] = fish_species_lst

    boat_details['bookings'] = ""
    blocked_dates = BoatBlockedDates.objects.filter(boat=boat_no)
    if blocked_dates.count() == 1:
        boat_details['bookings'] = blocked_dates[0].blocked_dates

    return JsonResponse(boat_details, safe=False)


@csrf_exempt
def upload_boat_picture(request):

    if "file" in request.FILES:
        added_img = BoatImages.objects.create(user=request.user, boat_image=request.FILES['file'])
    else:
        return HttpResponse(request.POST.items())

    return HttpResponse(str(added_img.pk))


@csrf_exempt
def boat_block_dates(request):
    boat_id = Boat.objects.get(pk=request.GET.get('barco'))
    boat_date = request.GET.get('date_from')
    boat_availability = request.GET.get('date_availability')

    boat_dates = BoatBlockedDates.objects.get_or_create(boat=boat_id)[0]
    str_blocked_dates = boat_dates.blocked_dates

    if str_blocked_dates == None:
        str_blocked_dates = ""

    if boat_availability == "false":
        str_blocked_dates = str(str_blocked_dates) + str(boat_date) + "_" + str(boat_date) + ";"
        boat_dates.blocked_dates = str_blocked_dates
    else:
        str_blocked_dates = str_blocked_dates.replace(str(boat_date) + "_" + str(boat_date)+";","")
        boat_dates.blocked_dates = str_blocked_dates

    boat_dates.save()

    return HttpResponse(str_blocked_dates)
