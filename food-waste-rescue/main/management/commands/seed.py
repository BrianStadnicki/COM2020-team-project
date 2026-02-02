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
        telephone_number="440123456789", 
        website_url="https://www.exeter.ac.uk/")
    return demo_seller

def create_consumer_profiles():
    """Create consumer profiles"""
    logger.info("Creating 400 consumer profiles")
    
    for i in range(400):
        user = User.objects.create_user(username=f"consumer{i}", email=f"consumer{i}@exeter.ac.uk", password="consumer")
        Consumer.objects.create(user=user, display_name=f"Consumer{i}")

def create_seller_profiles():
    """Create seller profiles"""
    logger.info("Creating 25 seller profiles")
    
    for i in range(25):
        user = User.objects.create_user(username=f"seller{i}", email=f"seller{i}@exeter.ac.uk", password="seller")
        Seller.objects.create(
            user=user, 
            display_name=f"Seller{i}", 
            location="Exeter", 
            opening_time="09:00", 
            closing_time="17:00",
            telephone_number="440123456789", 
            website_url="https://www.exeter.ac.uk/")
        # Phone number, opening and closing times, website to be randomised, WIP.

def create_bundle_postings():
    """Create 250 bundle postings"""
    logger.info("Creating bundle postings")
    
    categories =["Meals", "Bread & Pastries", "Groceries", "Flowers & Plants", "Pet Food", "Collect Now", "Collect Today", "Collect Tomorrow", "Vegetarian", "Vegan"]
    # No seller type implemented in models.py? To implement maybe? If so, can improve the randomised categories logic.
    
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
            
def create_reservations():
    """Create reservations"""
    logger.info("Creating reservations")
    
    consumers = Consumer.objects.all()
    postings = Bundle_posting.objects.all()
    
    statuses = ["C", "N", "R", "E"] 
    
    # 80 no-shows
    for _ in range(80):
        Reservation.objects.create(
            reservation_id=random.randint(0, 9999),
            posting_id=random.choice(postings),
            consumer_id=random.choice(consumers),
            claim_code=random.randint(0, 9999),
            status="N")
        
    # 50 expires
    for _ in range(50):
        Reservation.objects.create(
            reservation_id=random.randint(0, 9999),
            posting_id=random.choice(postings),
            consumer_id=random.choice(consumers),
            claim_code=random.randint(0, 9999),
            status="E")
        
    # Remaining reservations to be randomised
    for _ in range(270):
        Reservation.objects.create(
            reservation_id=random.randint(0, 9999),
            posting_id=random.choice(postings),
            consumer_id=random.choice(consumers),
            claim_code=random.randint(0, 9999),
            status=random.choice(statuses))
        
def create_issue_reports():
    """Create issue reports"""
    logger.info("Creating 150 issue reports")
    
    consumers = Consumer.objects.all()
    postings = Bundle_posting.objects.all()
    
    types = ["C", "A", "S"]
    
    for _ in range(150):
        IssueReport.objects.create(
            issue_id=random.randint(0, 9999),
            posting_id=random.choice(postings),
            consumer_id=random.choice(consumers),
            type=random.choice(types),
            description="This is terrible!"
        )
        
def run_seed():
    pass