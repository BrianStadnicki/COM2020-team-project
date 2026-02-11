from main.models import User, Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import time, datetime, timedelta
from decimal import Decimal
import random, logging
from django.db.models import Count, F

"""Fake data generator"""
fake = Faker("en_GB")

""" Logger for debugging """
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh --seed=123

""" Clear all data and creates new data """
MODE_REFRESH = 'refresh'

""" Clear all data only """
MODE_CLEAR = 'clear'


class BundleProvider:
    NAMES = {
        "M": [
            "Meat Bag", "Surprise Meat Bag", "Daily Special", "Healthy Meal", "Standard Meal",
            "Chef's Classic", "Food Leftovers", "Magic Meal Bag"
        ],
        "B&P": [
            "Bakery Bag","Bakery Surprise Bag", "Pastry Bag", "Fresh Bakery Bag",
            "Bakery Leftovers", "Pastry Surprise Bag", "Magic Bakery Bag", "Magic Pastry Bag"
        ],
        "G": [
            "Grocery Bag", "Grocery Surprise Bag", "Grocery Leftovers",
            "Mixed Grocery Bag", "Fresh Grocery Bag", "Magic Grocery Bag"
        ],
        "F&P": [
            "Flower Bag", "Flower Surprise Bag", "Plant Bag", "Plant Surprise Bag",
            "Bouquet", "Magic Flower Bag", "Magic Plant Bag", "Garden Warfare Bag"
        ],
        "PF": [
            "Pet Food Bag", "Pet Food Surprise Bag", "Magic Pet Food Bag"
        ],
        "V": [
            "Vegetarian Bag", "Veggie Surprise Bag", "Magic Vegetarian Bag"
        ],
        "VE": [
            "Vegan Surprise Bag", "Plant-Based Rescue Box", "Magic Vegan Bag",
        ]
    }

    CONTENTS = {
        "M": [
            "Breakfast to go.",
            "Brunch to go.",
            "Lunch to go.",
            "Dinner to go.",
            "Supper to go.",
            "Buffet leftovers.",
            "Italian cuisine.",
            "Mexican cuisine.",
            "Indian cuisine.",
            "American BBQ.",
            "Korean BBQ.",
            "Stir fry.",
            "Roasted food.",
            "Fried food.",
            "Grilled food.",
            "Steamed food.",
            "Salad.",
            "Pasta.",
            "Rice dish.",
            "Burgers.",
            "Noodles.",
            "Soup.",
            "Curry.",
            "Fast food.",
            "Cooked food with fresh ingredients."
        ],

        "B&P": [
            "Fresh bread.",
            "Assorted pastries.",
            "Croissants and rolls.",
            "Cakes and sweet bakes.",
            "Mixed baked goods.",
            "Sweet treats.",
            "Savoury pastries.",
            "Bread rolls.",
            "Artisan bread.",
            "Sourdough bread.",
            "Doughnuts.",
            "Muffins.",
            "Cookies.",
            "Baked goods from today."
        ],

        "G": [
            "Mixed groceries.",
            "Fresh produce.",
            "Fruit and vegetables.",
            "Chilled groceries.",
            "Pantry items.",
            "Everyday essentials.",
            "Food close to best-before.",
            "A mix of fresh and packaged food.",
            "Seasonal groceries.",
            "Household food items."
        ],

        "F&P": [
            "Fresh flowers.",
            "Seasonal blooms.",
            "Mixed bouquets.",
            "Potted plants.",
            "Cut flowers.",
            "Indoor plants.",
            "Outdoor plants.",
            "Assorted floral items."
        ],

        "PF": [
            "Dry pet food.",
            "Wet pet food.",
            "Pet treats.",
            "Mixed pet supplies.",
            "Dog food.",
            "Cat food.",
            "Fish food.",
            "Pet food close to best-before.",
            "Pet snacks."
        ],

        "V": [
            "Vegetarian meals.",
            "Meat-free dishes.",
            "Vegetarian groceries.",
            "Plant-based meals.",
            "Vegetarian cooked food.",
            "Vegetarian ready-to-eat food.",
            "Vegetarian selection of items."
        ],

        "VE": [
            "Vegan meals.",
            "Plant-based dishes.",
            "Vegan groceries.",
            "Vegan selection of items.",
            "Dairy-free food.",
            "Plant-based groceries."
        ]
    }


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
    fake.unique.clear()
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
    demo_user.user_type = "consumer"
    demo_user.save()
    demo_consumer = Consumer.objects.create(user=demo_user)
    demo_consumer.save()
    logger.info("{} demo user created.".format(demo_user))
    
    print(f"Username: {demo_user.username}")
    print(f"Email: {demo_user.email}")
    print("Password: demo")
    # demo_user.password will not work for good reason.
    
    return demo_consumer

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
    demo_seller_user.user_type = "seller"
    demo_seller_user.save()
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
    user.user_type = "consumer"
    user.save()
    consumer = Consumer.objects.create(user=user)
    consumer.save()
    logger.info("{} consumer created.".format(consumer))
    return consumer

def create_seller_profile():
    """Create seller profile"""
    logger.info("Creating seller profile")
    
    user = User.objects.create_user(username=fake.unique.user_name(), email=fake.unique.email(), password=fake.password())
    user.user_type = "seller"
    user.save()
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

def create_bundle_posting(seller, creation=None, window_start=None, window_end=None):
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
        
    
    categories = Bundle_posting.CATEGORYS

    selected_category = random.choice(categories)[0]

    if creation == None:
        # Creation time within last 6 weeks
        creation = fake.date_time_between(
            start_date="-6w",
            end_date="now",
            tzinfo=timezone.now().tzinfo
        )

    # Select a random pickup window from the list
    if window_start == None:
        window_start, window_end = random.choice(pickup_windows)

    bundle_posting = Bundle_posting.objects.create(
        seller=seller,
        category=selected_category,
        name=random.choice(BundleProvider.NAMES[selected_category])[:50],
        contents_description=random.choice(BundleProvider.CONTENTS[selected_category])[:100],
        quantity=random.randint(1, 5),
        price=Decimal(fake.pydecimal(left_digits=2, right_digits=2, positive=True)),
        creation_time=creation,
        pickup_window_start=window_start,
        pickup_window_end=window_end,
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
            
def create_reservation(status, chosen_consumer=None, selected_posting=None, starting_date=None, ending_date=None):
    """Create reservation. Ensures the reservation date is on the same date as the bundle posting."""
    logger.info("Creating reservation")
            
    if chosen_consumer != None:
        consumer = chosen_consumer
    else:
        consumers_pk = Consumer.objects.values_list('pk', flat=True)
        consumer_pk = random.choice(consumers_pk)
        consumer = Consumer.objects.get(pk=consumer_pk)

    if selected_posting == None:
        postings = Bundle_posting.objects.annotate(num_reservations=Count("reservation"))
        postings = postings.filter(num_reservations__lt=F("quantity"))
        if starting_date != None:
            postings = postings.filter(creation_time__gte=starting_date)
        if ending_date != None:
            postings = postings.filter(creation_time__lte=ending_date)
                    
        selected_posting = random.choice(postings.all())
        
    pickup_start = selected_posting.pickup_window_start
    pickup_end = selected_posting.pickup_window_end
    
    start_minutes = pickup_start.hour * 60 + pickup_start.minute
    end_minutes = pickup_end.hour * 60 + pickup_end.minute
    
    # Bias towards earlier pickups which is a lot more likely in a real-world scenario:
    if random.random() < 0.6:
        chosen_minutes = start_minutes + random.randint(0, (end_minutes - start_minutes) // 2)
    else:
        chosen_minutes = random.randint(start_minutes, end_minutes)
    
    chosen_time = time(chosen_minutes // 60,chosen_minutes % 60)

    posting_date = selected_posting.creation_time.date()
    now = timezone.now()
    
    # RuntimeWarning: DateTimeField received a naive datetime solved with:
    # https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
    
    time_stamp = now.replace(posting_date.year,posting_date.month,posting_date.day,chosen_time.hour,chosen_time.minute,0,0)
    
    reservation = Reservation.objects.create(
        posting = selected_posting,
        consumer = consumer,
        time_stamp = time_stamp,
        claim_code = fake.unique.random_int(min=0, max=99999),
        is_collected = status == "C"
    )
    
    reservation.save()
    return reservation

def create_issue_report(type, consumer=None):
    """Create issue report"""
    logger.info("Creating issue report")
    
    consumers = list(Consumer.objects.all())
    postings = list(Bundle_posting.objects.all())

    if consumer == None:
        consumer = random.choice(consumers)
    
    # Ensure issue report creation time is within the last 6 weeks
    creation_time=fake.date_time_between(
            start_date="-6w",
            end_date="now",
            tzinfo=timezone.now().tzinfo)
    
    report = IssueReport.objects.create(
        posting=random.choice(postings),
        consumer=consumer,
        type=type,
        description=fake.sentence(),
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
    
    
    # Generate demo user and demo seller (fixed)
    demo_user = create_demo_user()
    print("------------------------------------")
    demo_seller = create_demo_seller()

    sellers = [demo_seller]
    
    # Generate 100 consumers
    for _ in range(100):
        create_consumer_profile()
    
    consumers = list(Consumer.objects.all())
    active_consumers = random.sample(consumers, 19) + [demo_user]
    
    # Generate 25 sellers
    for _ in range(25):
        sellers.append(create_seller_profile())
    
    # For each seller, there will be 25 bundle postings
    for seller in sellers:
        for _ in range(25):
            create_bundle_posting(seller)

    date_now = timezone.now().date()
    week_range = 6
    monday = date_now - timedelta(days=date_now.weekday())

    # Consumers with streaks
    for consumer in active_consumers:
        for i in range(week_range):
            start_week = monday - timedelta(weeks=i)
            end_week = start_week + timedelta(days=6)
            create_reservation("C", chosen_consumer=consumer, starting_date=start_week, ending_date=end_week)
            
    # 400 reservations
    for _ in range(400):
        
        if random.random() < 0.4:
            status = "C"
        else:
            status = "R"
            
        create_reservation(status)
    
    # 150 issues with random type
    for _ in range(150):
        create_issue_report(random.choice(["C","A","S"]))
    
    create_issue_report(random.choice(["C","A","S"]), demo_user)
    # At least a few active bundle postings
    create_bundle_posting(demo_seller, creation=date_now, window_start=time(10,00), window_end=time(23,00))
    create_bundle_posting(random.choice(sellers), creation=date_now, window_start=time(10,30), window_end=time(23,30))
    create_bundle_posting(random.choice(sellers), creation=date_now, window_start=time(10,30), window_end=time(23,30))

    demo_seller_postings = list(Bundle_posting.objects.filter(seller=demo_seller).all())
    for posting in random.sample(demo_seller_postings, 10):
        while posting.available > 0:
            create_reservation(status="C", selected_posting=posting)
