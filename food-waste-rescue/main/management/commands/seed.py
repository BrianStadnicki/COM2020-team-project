from main.models import User, Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import time
from decimal import Decimal
import random, logging

"""Fake data generator"""
fake = Faker("en_GB")

""" Logger for debugging """
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh --seed=123

""" Clear all data and creates new data """
MODE_REFRESH = 'refresh'

""" Clear all data only """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "Seed database with synthetic data"

    def add_arguments(self, parser):
        """Arguments"""
        parser.add_argument('--mode', type=str, help="Seeding Mode")
        parser.add_argument('--seed', type=int, help="Choose a seed")

    def handle(self, *args, **options):
        """Handles CLI"""
        mode = options['mode']
        seed = options['seed']
        random.seed(seed)
        fake.seed_instance(seed)
        self.stdout.write(f"Seeding data with mode={mode} and seed={seed}...")
        run_seed(self, mode, seed)
        self.stdout.write('Done.')
        
def clear_data():
    """Deletes all the table data"""
    logger.info("Delete all model data.")
    Consumer.objects.all().delete()
    Bundle_posting.objects.all().delete()
    Seller.objects.all().delete()
    IssueReport.objects.all().delete()
    Reservation.objects.all().delete()
    User.objects.all().delete()
    
def create_demo_user():
    """Create a fixed demo user"""
    logger.info("Creating demo user")
    demo_user = User.objects.create_user(username="demo", email="demo@exeter.ac.uk", password="demo")
    demo_user.save()
    logger.info("{} demo user created.".format(demo_user))
    
    print(f"Username: {demo_user.username}")
    print(f"Email: {demo_user.email}")
    print("Password: demo")
    # demo_user.password will not work for good reason.
    
    return demo_user

def create_demo_seller():
    """Create a fixed demo seller"""
    logger.info("Creating demo seller")
    
    demo_seller_user = User.objects.create_user(username="demo_seller", email="demo_seller@exeter.ac.uk", password="demo_seller")
    demo_seller = Seller.objects.create(
        user=demo_seller_user, 
        location="Exeter", 
        opening_time=time(9, 0), 
        closing_time=time(17,0), 
        telephone_number="441326370400", 
        website_url="https://www.exeter.ac.uk/")
    demo_seller.save()
    logger.info("{} demo seller created.".format(demo_seller))
    
    print(f"Username: {demo_seller_user.username}")
    print(f"Email: {demo_seller_user.email}")
    print("Password: demo_seller")
    # demo_seller_user.password will not work for good reason.
    
    return demo_seller

def create_consumer_profile():
    """Create consumer profile"""
    logger.info("Creating consumer profile")
    user = User.objects.create_user(username=fake.unique.user_name(), email=fake.unique.email(), password=fake.password())
    consumer = Consumer.objects.create(user=user)
    consumer.save()
    logger.info("{} consumer created.".format(consumer))
    return consumer

def create_seller_profile():
    """Create seller profile"""
    logger.info("Creating seller profile")
    
    user = User.objects.create_user(username=fake.unique.user_name(), email=fake.unique.email(), password=fake.password())
    seller = Seller.objects.create(
        user=user, 
        location=fake.city(), 
        opening_time=time(random.randint(6,10), random.choice([0,15,30,45])), 
        closing_time=time(random.randint(15,23),random.choice([0,15,30,45])),
        telephone_number=fake.phone_number(), 
        website_url=fake.url())
    seller.save()
    logger.info("{} seller created.".format(seller))
    return seller

def create_bundle_posting(seller):
    """Create bundle posting"""
    logger.info("Creating bundle posting")
    
    pickup_windows = [
        (time(15, 30), time(16, 30)),
        (time(16, 00), time(17, 00)),
        (time(16, 30), time(17, 30)),
        (time(17, 00), time(18, 00)),
        (time(17, 30), time(18, 30)),
        (time(18, 00), time(19, 00)),
        (time(18, 30), time(19, 30)),
        (time(19, 00), time(20, 00)),
        (time(19, 30), time(20, 30)),
        (time(20, 00), time(21, 00)),
        (time(20, 30), time(21, 30)),
        (time(21, 00), time(22, 00)),
    ]
        
    
    categories =["Meals", "Bread & Pastries", "Groceries", "Flowers & Plants", "Pet Food", "Collect Now", "Collect Today", "Vegetarian", "Vegan"]

    duration_minutes = random.choice([15, 30, 45, 60, 75, 90, 105, 120])

    # Creation time within last 6 weeks
    creation = fake.date_time_between(
        start_date="-6w",
        end_date="now",
        tzinfo=timezone.now().tzinfo
    )

    # Select a random pickup window from the list
    window_start, window_end = random.choice(pickup_windows)

    open_minutes = seller.opening_time.hour * 60 + seller.opening_time.minute
    close_minutes = seller.closing_time.hour * 60 + seller.closing_time.minute

    start_minutes = window_start.hour * 60 + window_start.minute
    end_minutes = window_end.hour * 60 + window_end.minute

    # Ensure start and end are within seller operating times
    start_minutes = max(start_minutes, open_minutes)
    end_minutes = min(end_minutes, close_minutes)

    # If end <= start, use a 60 minute window inside operating times
    if end_minutes <= start_minutes:
        duration = 60
        latest_start = close_minutes - duration
        
        # Use start and closing time if out of bounds
        if latest_start <= open_minutes:
            start_minutes = open_minutes
            end_minutes = close_minutes

        # If not out of bounds
        else:
            start_minutes = random.randint(open_minutes, latest_start)
            end_minutes = start_minutes + duration

    pickup_window_start = time(start_minutes // 60, start_minutes % 60)
    pickup_window_end = time(end_minutes // 60, end_minutes % 60)

    bundle_posting = Bundle_posting.objects.create(
        seller=seller,
        category=random.choice(categories),
        name=fake.catch_phrase()[:50],
        contents_description=fake.text(max_nb_chars=100),
        quantity=random.randint(1, 5),
        price=Decimal(fake.pydecimal(left_digits=2, right_digits=2, positive=True)),
        creation_time=creation,
        pickup_window_start=pickup_window_start,
        pickup_window_end=pickup_window_end,
        allergen_celery=random.choice([True, False]),
        allergen_crustacean=random.choice([True, False]),
        allergen_dairy=random.choice([True, False]),
        allergen_egg=random.choice([True, False]),
        allergen_fish=random.choice([True, False]),
        allergen_gluten=random.choice([True, False]),
        allergen_lupin=random.choice([True, False]),
        allergen_mollusc=random.choice([True, False]),
        allergen_mustard=random.choice([True, False]),
        allergen_nut=random.choice([True, False]),
        allergen_peanut=random.choice([True, False]),
        allergen_sesame=random.choice([True, False]),
        allergen_soya=random.choice([True, False]),
        allergen_sulphite=random.choice([True, False]),
    )
    return bundle_posting
            
def create_reservation(status):
    """Create reservation"""
    logger.info("Creating reservation")
    
    consumers = list(Consumer.objects.all())
    postings = list(Bundle_posting.objects.all())
    
    time_stamp=fake.date_time_between(
        start_date="-6w",
        end_date="now",
        tzinfo=timezone.now().tzinfo
    )
    
    reservation = Reservation.objects.create(
        posting = random.choice(postings),
        consumer = random.choice(consumers),
        time_stamp = time_stamp,
        claim_code = random.randint(0,99999),
        status = status
    )
    
    reservation.save()
    return reservation

def create_issue_report(type):
    """Create issue report"""
    logger.info("Creating issue report")
    
    consumers = list(Consumer.objects.all())
    postings = list(Bundle_posting.objects.all())
    
    creation_time=fake.date_time_between(
            start_date="-6w",
            end_date="now",
            tzinfo=timezone.now().tzinfo)
    
    report = IssueReport.objects.create(
        posting=random.choice(postings),
        consumer=random.choice(consumers),
        type=type,
        description=fake.text(max_nb_chars=500),
        status=random.choice(["P", "A", "R"]),
        creation_time=creation_time,
        seller_response=fake.sentence(),
    )
    report.save()
    return report
        
def run_seed(self, mode, seed):
    """
    Seed database based on mode and seed
    """
    
    clear_data()
    if mode == MODE_CLEAR:
        return
    
    demo_user = create_demo_user()
    print("------------------------------------")
    demo_seller = create_demo_seller()

    sellers = [demo_seller]
    
    for _ in range(100):
        create_consumer_profile()
    
    for _ in range(25):
        sellers.append(create_seller_profile())
    
    for seller in sellers:
        for _ in range(25):
            create_bundle_posting(seller)

    for _ in range(80):
        create_reservation("N")
        
    for _ in range(50):
        create_reservation("E")
        
    for _ in range(270):
        create_reservation(random.choice(["C", "R", "N", "E"]))        

    for _ in range(150):
        create_issue_report(random.choice(["C","A","S"]))