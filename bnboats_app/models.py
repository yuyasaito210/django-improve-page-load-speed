from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


def get_member_upload_to(instance, filename):
    try:
        user_name = "media/users/"+str(instance.user.pk)
    except AttributeError:
        user_name = "media/admin"
    return str(user_name)+"/"+filename


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    DOC_TYPES = [
        ('CPF', 'CPF'),
        ('Passport', 'Passport'),
        ('CNPJ', 'CNPJ')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_member_upload_to, verbose_name='Image', null=True)
    mobile_country = models.CharField(max_length=3, default='+55')
    mobile_area = models.IntegerField(null=True, blank=True)
    mobile_number = models.IntegerField(null=True, blank=True)
    address_street = models.CharField(max_length=100, null=True, blank=True)
    address_number = models.IntegerField(null=True, blank=True)
    address_additional = models.CharField(max_length=60, null=True, blank=True)
    address_postcode = models.CharField(max_length=30, null=True, blank=True)
    address_area = models.CharField(max_length=30, null=True, blank=True)
    address_city = models.CharField(max_length=100, null=True, blank=True)
    address_state = models.CharField(max_length=30, null=True, blank=True)
    address_country = models.CharField(max_length=30, default='Brasil')
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=GENDER_CHOICES[0])
    dob_day = models.IntegerField(null=True, blank=True)
    dob_month = models.CharField(null=True, blank=True, max_length=15)
    dob_year = models.IntegerField(null=True, blank=True)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default=DOC_TYPES[0])
    doc_number = models.CharField(max_length=18, null=True, blank=True)
    profile_desc = models.TextField(max_length=500, null=True, blank=True)
    mobile_confirmed = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    mobile_code = models.CharField(max_length=5, null=True, blank=True)
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    bank_branch = models.CharField(max_length=30, null=True, blank=True)
    bank_account = models.CharField(max_length=20, null=True, blank=True)
    bank_owner = models.CharField(max_length=100, null=True, blank=True)
    old_id = models.CharField(max_length=10, null=True, blank=True)
    fishing_client = models.CharField(max_length=100, null=True, blank=True)
    fishing_discount = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class CaptainExtraActivities(models.Model):
    sid_cea = models.CharField(unique=True, max_length=3, default="ZZZ")
    activity = models.CharField(max_length=60, default="")

    def __str__(self):
        return str(self.activity)


class CaptainLanguages(models.Model):
    sid_cl = models.CharField(unique=True, max_length=3, default="ZZZ")
    language = models.CharField(max_length=60, default="")

    def __str__(self):
        return str(self.language)


class CaptainProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    is_captaion = models.CharField(max_length=30, null=True, blank=True)
    license_type = models.CharField(max_length=30, null=True, blank=True)
    lt_professional = models.CharField(max_length=60, null=True, blank=True)
    experience = models.CharField(max_length=60, null=True, blank=True)
    extra_activities = models.ManyToManyField(CaptainExtraActivities, blank=True)
    languages = models.ManyToManyField(CaptainLanguages, blank=True)

    def __str__(self):
        return self.user.first_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CaptainProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.captainprofile.save()


class State(models.Model):
    name = models.CharField(max_length=25)
    country = models.CharField(max_length=25, default='Brasil')

    def __str__(self):
        return str(self.name) + " - " + str(self.country)


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(max_length=25)
    nearby_cities = models.ManyToManyField('self', related_name="cities_nearby", blank=True)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = "Cities"


class BoatImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    boat_image = models.ImageField(upload_to=get_member_upload_to, verbose_name='Image', null=True)

    def __str__(self):
        return str(self.boat_image)


class BoatType(models.Model):
    sid_bt = models.CharField(max_length=3, unique=True, default="ZZZ")
    name = models.CharField(max_length=25, default="Boat Type blank")
    image = models.ImageField(upload_to=get_member_upload_to, verbose_name='Image', null=True)

    def __str__(self):
        return str(self.sid_bt) + " - " + str(self.name)


class BoatAmenities(models.Model):
    AMENITY_TYPES = (
        ('EL', 'EL'),
        ('CO', 'CO'),
        ('AA', 'AA'),
        ('LA', 'LA'),
        ('EQ', 'EQ')
    )
    sid_ba = models.CharField(max_length=3, unique=True, default="ZZZ")
    type = models.CharField(max_length=2, choices=AMENITY_TYPES, default=AMENITY_TYPES[0])
    name = models.CharField(max_length=25)

    def __str__(self):
        return str(self.sid_ba) + " - " + str(self.type) + " - " + str(self.name)

    class Meta:
        verbose_name_plural = "BoatAmenities"


class BoatPriceIncludes(models.Model):
    sid_bpi = models.CharField(max_length=3, unique=True, default="ZZZ")
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.sid_bpi) + " - " + str(self.name)


class BoatFishingSpecies(models.Model):
    sid_bfs = models.CharField(max_length=3, unique=True, default="ZZZ")
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.sid_bfs) + " - " + str(self.name)


class Boat(models.Model):
    boat_type = models.ForeignKey("BoatType", null=True, on_delete=models.SET_NULL, to_field="sid_bt")
    user = models.ForeignKey(User, related_name="+", null=True, on_delete=models.CASCADE)
    city = models.ForeignKey("City", null=True, on_delete=models.SET_NULL)
    boat_amenities = models.ManyToManyField("BoatAmenities", blank=True, related_name="boatamen")
    images = models.ManyToManyField(BoatImages)
    fab_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2030)], blank=True, null=True)
    title = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=60, blank=True, null=True)
    size = models.IntegerField(default=0)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)], default=0)
    overnight_capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=0)
    bathrooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], default=0)
    rooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], default=0)
    animals = models.CharField(max_length=30, default="0")
    smoke = models.CharField(max_length=30, default="0")
    wheelchair = models.CharField(max_length=30, default="0")
    has_discount = models.CharField(max_length=30, default="0")
    postcode = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    additional = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    price_overnight = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_day = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_half_day = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    price_single = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    p_single_includes = models.ManyToManyField(BoatPriceIncludes, related_name='ps_includes', blank=True)
    p_hday_includes = models.ManyToManyField(BoatPriceIncludes, related_name='phd_includes', blank=True)
    p_day_includes = models.ManyToManyField(BoatPriceIncludes, related_name='pd_includes', blank=True)
    p_overnight_includes = models.ManyToManyField(BoatPriceIncludes, related_name='po_includes', blank=True)
    fish_rules = models.CharField(null=True, blank=True, max_length=30)
    fish_species = models.ManyToManyField(BoatFishingSpecies, blank=True)
    fish_bait = models.CharField(null=True, blank=True, max_length=30)
    fish_places = models.CharField(null=True, blank=True, max_length=30)
    review_score = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    reviews_count = models.IntegerField(default=0)
    log = models.IntegerField(default=0)
    BOAT_STATUS = (
        ('InReview', 'InReview'),
        ('Published', 'Published'),
        ('Paused', 'Paused'),
        ('Deleted', 'Deleted'),
    )
    status = models.CharField(choices=BOAT_STATUS, max_length=30, default=BOAT_STATUS[0])
    keywords = models.CharField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    owner_price_overnight = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    owner_price_day = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    owner_price_half_day = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    owner_price_single = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return str(self.title) + " - " + str(self.user.first_name)

class Review(models.Model):
    boat = models.ForeignKey("Boat", null=True, on_delete=models.SET_NULL)
    notowner_user = models.ForeignKey(UserProfile, related_name="+", null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(UserProfile, related_name="+", null=True, on_delete=models.SET_NULL)
    review = models.CharField(max_length=1000)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5)
    created_on = models.DateTimeField(auto_now_add=True)
    status_list = (
        ("New", "New"),
        ("Published", "Published"),
        ("Hidden", "Hidden"),
        ("Rejected", "Rejected"),
    )
    status = models.CharField(choices=status_list, default=status_list[0], max_length=25)

    def __str__(self):
        return str(self.review)


class Booking(models.Model):
    boat = models.ForeignKey("Boat", null=True, on_delete=models.SET(251))
    customer = models.ForeignKey(User, related_name="+", null=True, on_delete=models.SET(251))
    date_from = models.DateField()
    date_to = models.DateField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    no_passengers = models.IntegerField(default=1)
    booking_period = models.CharField(max_length=20, default="08")
    status_list = (
        ('New', 'New'),
        ('PaymentPending', 'PaymentPending'),
        ('Paid', 'Paid'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(choices=status_list, default=status_list[0], max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey(User, related_name="+", null=True, on_delete=models.SET_NULL)
    # description = models.CharField(max_length=200)
    # location = models.CharField(max_length=25)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.status) + ' - ' + str(self.created_on) + ' - ' + str(self.boat.title) + ' - ' + str(self.customer.first_name)


class Invoice(models.Model):
    methods_list = (
        ("Boleto", "Boleto"),
        ("CCard", "CCard"),
        ("DCard", "DCard"),
    )
    booking = models.OneToOneField("Booking", null=True, on_delete=models.SET_NULL)
    payment_code = models.CharField(max_length=200)
    payment_method = models.CharField(choices=methods_list, default=methods_list[0], max_length=25)
    is_paid = models.BooleanField(default=False)
    payment_api_status = models.CharField(max_length=200, null=True, blank=True)
    payment_ccard_brand = models.CharField(max_length=200, null=True, blank=True)
    payment_ccard_no = models.CharField(max_length=200, null=True, blank=True)
    payment_total = models.CharField(max_length=200, null=True, blank=True)
    paid_on_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.booking)


class Message(models.Model):
    msg_from = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    msg_to = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    sent_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return "(" + str(self.msg_from) + " - " + str(self.msg_to) + ") " + self.message


class BoatFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.first_name) + " - " + str(self.boat.title)


class IBGECityCodes(models.Model):
    ibge_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default="cidade")

    def __str__(self):
        return str(self.ibge_id) + " - " + str(self.name)


class BoatBlockedDates(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    blocked_dates = models.CharField(max_length=5000, null=True, blank=True, default="")

    def __str__(self):
        return str(self.boat.title) + " - " + str(self.blocked_dates)


