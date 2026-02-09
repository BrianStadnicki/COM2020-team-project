from main.models import User, Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import time, datetime
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


class BundleProvider:
    NAMES = {
        "Meals": [
            "Meat Bag", "Surprise Meat Bag", "Daily Special", "Healthy Meal", "Standard Meal",
            "Chef's Classic", "Food Leftovers", "Magic Meal Bag"
        ],
        "Bread & Pastries": [
            "Bakery Bag","Bakery Surprise Bag", "Pastry Bag", "Fresh Bakery Bag",
            "Bakery Leftovers", "Pastry Surprise Bag", "Magic Bakery Bag", "Magic Pastry Bag"
        ],
        "Groceries": [
            "Grocery Bag", "Grocery Surprise Bag", "Grocery Leftovers",
            "Mixed Grocery Bag", "Fresh Grocery Bag", "Magic Grocery Bag"
        ],
        "Flowers & Plants": [
            "Flower Bag", "Flower Surprise Bag", "Plant Bag", "Plant Surprise Bag",
            "Bouquet", "Magic Flower Bag", "Magic Plant Bag", "Garden Warfare Bag"
        ],
        "Pet Food": [
            "Pet Food Bag", "Pet Food Surprise Bag", "Magic Pet Food Bag"
        ],
        "Vegetarian": [
            "Vegetarian Bag", "Veggie Surprise Bag", "Magic Vegetarian Bag"
        ],
        "Vegan": [
            "Vegan Surprise Bag", "Plant-Based Rescue Box", "Magic Vegan Bag",
        ],
        "Collect Now": [
            "Last Minute Bag", "Last Minute Surprise Bag", "Magic Last Minute Bag"
        ],
        "Collect Today": [
            "Today’s Surprise Bag", "Today's Special Bag", "Today's Magic Bag"
        ]
    }

    CONTENTS = {
        "Meals": [
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

        "Bread & Pastries": [
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

        "Groceries": [
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

        "Flowers & Plants": [
            "Fresh flowers.",
            "Seasonal blooms.",
            "Mixed bouquets.",
            "Potted plants.",
            "Cut flowers.",
            "Indoor plants.",
            "Outdoor plants.",
            "Assorted floral items."
        ],

        "Pet Food": [
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

        "Vegetarian": [
            "Vegetarian meals.",
            "Meat-free dishes.",
            "Vegetarian groceries.",
            "Plant-based meals.",
            "Vegetarian cooked food.",
            "Vegetarian ready-to-eat food.",
            "Vegetarian selection of items."
        ],

        "Vegan": [
            "Vegan meals.",
            "Plant-based dishes.",
            "Vegan groceries.",
            "Vegan selection of items.",
            "Dairy-free food.",
            "Plant-based groceries."
        ],

        "Collect Now": [
            "Items available for immediate collection.",
            "Last-minute food rescue.",
            "Urgent collection items.",
            "Food hot and ready-to-go."
        ],

        "Collect Today": [
            "Items available for collection today.",
            "Food to be collected today.",
            "Same-day collection items.",
            "Today's surplus food."
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

    selected_category = random.choice(categories)

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
        category=selected_category,
        name=random.choice(BundleProvider.NAMES[selected_category])[:50],
        contents_description=random.choice(BundleProvider.CONTENTS[selected_category])[:100],
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
    """Create reservation. Ensures the reservation date is on the same date as the bundle posting."""
    logger.info("Creating reservation")
    
    consumers = list(Consumer.objects.all())
    postings = list(Bundle_posting.objects.all())
    
    available_postings = []
    
    for posting in postings:
        if posting.available > 0:
            available_postings.append(posting)
        else:
            pass
        
    if available_postings == []:
        return None
    
    selected_posting = random.choice(available_postings)
    
    pickup_start = selected_posting.pickup_window_start
    pickup_end = selected_posting.pickup_window_end
    
    start_minutes = pickup_start.hour * 60 + pickup_start.minute
    end_minutes = pickup_end.hour * 60 + pickup_end.minute
    
    chosen_minutes = random.randint(start_minutes, end_minutes)
    
    chosen_time = time(chosen_minutes // 60,chosen_minutes % 60)

    time_stamp = datetime.combine(selected_posting.creation_time.date(),chosen_time)

    reservation = Reservation.objects.create(
        posting = selected_posting,
        consumer = random.choice(consumers),
        time_stamp = time_stamp,
        claim_code = fake.unique.random_int(min=0, max=99999),
        is_collected = status == "C"
    )
    
    reservation.save()
    return reservation

def create_issue_report(type):
    """Create issue report"""
    logger.info("Creating issue report")
    
    consumers = list(Consumer.objects.all())
    postings = list(Bundle_posting.objects.all())
    
    # Ensure issue report creation time is within the last 6 weeks
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
    
    # Generate demo user and demo seller (fixed)
    demo_user = create_demo_user()
    print("------------------------------------")
    demo_seller = create_demo_seller()

    sellers = [demo_seller]
    
    # Generate 100 consumers
    for _ in range(100):
        create_consumer_profile()
    
    # Generate 25 sellers
    for _ in range(25):
        sellers.append(create_seller_profile())
    
    # For each seller, there will be 25 bundle postings
    for seller in sellers:
        for _ in range(25):
            create_bundle_posting(seller)

    for _ in range(400):
        pass