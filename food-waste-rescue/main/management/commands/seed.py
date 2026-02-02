from main.models import User, Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
import random, logging

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
        self.stdout.write(f"Seeding data with mode={mode} and seed={seed}...")
        run_seed(self, mode, seed)
        self.stdout.write('Done.')
        
def clear_data():
    """Deletes all the table data"""
    logger.info("Delete all model data.")
    User.objects.all().delete()
    Consumer.objects.all().delete()
    Seller.objects.all().delete()
    Bundle_posting.objects.all().delete()
    Reservation.objects.all().delete()
    IssueReport.objects.all().delete()
    
def create_demo_user():
    """Create a fixed demo user"""
    logger.info("Creating demo user")
    demo_user = User.objects.create_user(username="demo", email="demo@exeter.ac.uk", password="demo")
    demo_user.save()
    logger.info("{} demo user created.".format(demo_user))
    return demo_user

def create_demo_seller():
    """Create a fixed demo seller"""
    logger.info("Creating demo seller")
    
    demo_seller_user = User.objects.create_user(username="demo_seller", email="demo_seller@exeter.ac.uk", password="demo_seller")
    demo_seller = Seller.objects.create(
        user=demo_seller_user, 
        display_name="Demo Seller", 
        location="Exeter", 
        opening_time="09:00", 
        closing_time="17:00", 
        telephone_number="441326370400", 
        website_url="https://www.exeter.ac.uk/")
    demo_seller.save()
    logger.info("{} demo seller created.".format(demo_seller))
    return demo_seller

def create_consumer_profile(i):
    """Create consumer profile"""
    logger.info("Creating consumer profile")
    user = User.objects.create_user(username=f"consumer{i}", email=f"consumer{i}@exeter.ac.uk", password="consumer")
    consumer = Consumer.objects.create(user=user, display_name=f"Consumer{i}")
    consumer.save()
    logger.info("{} consumer created.".format(consumer))
    return consumer

def create_seller_profile(i):
    """Create seller profile"""
    logger.info("Creating seller profile")
    
    user = User.objects.create_user(username=f"seller{i}", email=f"seller{i}@exeter.ac.uk", password="seller")
    seller = Seller.objects.create(
        user=user, 
        display_name=f"Seller{i}", 
        location="Exeter", 
        opening_time="09:00", 
        closing_time="17:00",
        telephone_number="440123456789", 
        website_url="https://www.exeter.ac.uk/")
        # Phone number, opening and closing times, website to be randomised, WIP.
    seller.save()
    logger.info("{} seller created.".format(seller))
    return seller

def create_bundle_posting():
    """Create bundle posting"""
    logger.info("Creating bundle posting")
    
    categories =["Meals", "Bread & Pastries", "Groceries", "Flowers & Plants", "Pet Food", "Collect Now", "Collect Today", "Collect Tomorrow", "Vegetarian", "Vegan"]
    
    sellers = Seller.objects.all()
    for seller in sellers:
        for _ in range(10):
            Bundle_posting.objects.create(
                posting_id=random.randint(0, 9999),
                seller_id=seller,
                category=random.choice(categories),
                allegerns=random.randint(0, 5),
                quantity=random.randint(1, 20),
                price=round(random.uniform(1.00, 50.00), 2)
            )
            
    bundle_posting.save()
    return bundle_posting
            
def create_reservation(status):
    """Create reservation"""
    logger.info("Creating reservation")
    
    consumers = Consumer.objects.all()
    postings = Bundle_posting.objects.all()
    
    reservation = Reservation.objects.create()
    reservation.save()
    return reservation

def create_issue_report(type):
    """Create issue report"""
    logger.info("Creating issue report")
    
    consumers = Consumer.objects.all()
    postings = Bundle_posting.objects.all()
    
    report = IssueReport.objects.create()
    report.save()
    return report
        
def run_seed(self, mode):
    """
    Seed database based on mode and seed
    """
    
    clear_data()
    if mode == MODE_CLEAR:
        return
    
    create_demo_user()
    create_demo_seller()
    create_consumer_profile()
    create_bundle_posting()
    create_reservation()
    create_issue_report()