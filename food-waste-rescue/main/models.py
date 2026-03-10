from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from decimal import Decimal


class User(AbstractUser):
    USER_TYPES = (("consumer", "Consumer"), ("seller", "Seller"))

    user_type = models.CharField(max_length=10, choices=USER_TYPES)


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default="Exeter University")
    opening_time = models.TimeField(default=datetime.time(9, 00))
    closing_time = models.TimeField(default=datetime.time(17, 00))
    telephone_number = models.CharField(max_length=100, default="441392661000")
    website_url = models.URLField(default="https://www.exeter.ac.uk/")
    wheelchair = models.BooleanField(default=False)


class Bundle_posting_category(models.Model):
    name = models.CharField(max_length=30)


class Bundle_posting(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Bundle_posting_category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Meat bag")
    contents_description = models.CharField(max_length=500, default="Chicken breast")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=Decimal("0.00")
    )
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    pickup_window_start = models.TimeField(default=datetime.time(18, 00))
    pickup_window_end = models.TimeField(default=datetime.time(19, 00))
    allergen_celery = models.BooleanField(default=False)
    allergen_crustacean = models.BooleanField(default=False)
    allergen_dairy = models.BooleanField(default=False)
    allergen_egg = models.BooleanField(default=False)
    allergen_fish = models.BooleanField(default=False)
    allergen_gluten = models.BooleanField(default=False)
    allergen_lupin = models.BooleanField(default=False)
    allergen_mollusc = models.BooleanField(default=False)
    allergen_mustard = models.BooleanField(default=False)
    allergen_nut = models.BooleanField(default=False)
    allergen_peanut = models.BooleanField(default=False)
    allergen_sesame = models.BooleanField(default=False)
    allergen_soya = models.BooleanField(default=False)
    allergen_sulphite = models.BooleanField(default=False)

    STATUSES = (("C", "Collected"), ("E", "Expired"), ("R", "Reserved"))

    @property
    def status(self):
        if self.reservation_set.filter(is_collected=True).count() == self.quantity:
            return "C"
        elif (
            self.creation_time.date() == datetime.datetime.today().date()
            and self.pickup_window_end > datetime.datetime.today().time()
        ):
            return "R"
        else:
            return "E"

    @property
    def status_str(self):
        status = self.status
        for possible in self.STATUSES:
            if status == possible[0]:
                return possible[1]

    @property
    def available(self):
        return self.quantity - self.reservation_set.count()


class Reservation(models.Model):
    posting = models.ForeignKey(Bundle_posting, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now, blank=True)
    claim_code = models.IntegerField(default=0)
    is_collected = models.BooleanField(default=False)
    STATUSES = (("C", "Collected"), ("N", "No Show"), ("R", "Reserved"))

    @property
    def status(self):
        if self.is_collected:
            return "C"
        if (
            self.posting.creation_time.date() == datetime.datetime.today().date()
            and self.posting.pickup_window_end > datetime.datetime.today().time()
        ):
            return "R"
        return "N"

    @property
    def status_str(self):
        status = self.status
        for possible in self.STATUSES:
            if status == possible[0]:
                return possible[1]

    def claim_code_generator(self):
        self.claim_code = self.pk * 2
        self.save(update_fields=["claim_code"])

    def save(self, *args, **kwargs):
        if (
            self._state.adding
            and self.posting.quantity - self.posting.reservation_set.count() <= 0
        ):
            raise Exception(f"Too many reservations for posting")
        super().save(*args, **kwargs)


class IssueReport(models.Model):
    posting = models.ForeignKey(Bundle_posting, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    TYPES = (("C", "Collection"), ("A", "Additional information"), ("S", "Seller"))
    type = models.CharField(max_length=1, choices=TYPES, default="C")
    description = models.CharField(max_length=1000, blank=True)
    STATUSES = (("P", "Pending"), ("A", "Acknowledged"), ("R", "Resolved"))
    status = models.CharField(max_length=1, choices=STATUSES, default="P")
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    seller_response = models.CharField(max_length=500, default="Hello consumer!")

    @property
    def type_str(self):
        type = self.type
        for possible in self.TYPES:
            if type == possible[0]:
                return possible[1]

    @property
    def status_str(self):
        status = self.status
        for possible in self.STATUSES:
            if status == possible[0]:
                return possible[1]


class Forecast_output(models.Model):
    posting = models.ForeignKey(Bundle_posting, on_delete=models.CASCADE)
    predicted_reservations = models.IntegerField(default=0)
    predicted_no_show_prob = models.IntegerField(default=0)
    confidence = models.IntegerField(default=0)
    rationale = models.CharField(max_length=1000, blank=True)
    time_recommendation = models.TimeField(blank=True)
    type = models.CharField(max_length=100, default="Linear Regression")

class Seller_actions(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Bundle_posting_category, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now, blank=True)    
    TYPES = (
        ("IPD", "Increased Production"),
        ("RPD", "Reduced Production"),
        ("IPR", "Increased Price"),
        ("RPR", "Reduces Price"),
        ("O", "Other"),
    )
    type = models.CharField(max_length=5, choices=TYPES, default="RPD")
    details = models.CharField(max_length=1000, blank=True)
