from main.models import Bundle_posting_category, User, Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
from datetime import time
import random, logging

""" Logger for debugging """
logger = logging.getLogger(__name__)

""" Clear all data and creates new data """
MODE_REFRESH = "refresh"

""" Clear all data only """
MODE_CLEAR = "clear"

CATEGORIES = [
        "Meals",
        "Bread & Pastries",
        "Groceries",
        "Flowers & Plants",
        "Pet Food",
        "Vegetarian",
        "Vegan"
    ]

class Command(BaseCommand):
    help = "Seed database with synthetic data"

    def add_arguments(self, parser):
        """Arguments"""
        parser.add_argument("--mode", type=str, help="Seeding Mode")
        parser.add_argument("--seed", type=int, help="Choose a seed")

    def handle(self, *args, **options):
        """Handles CLI"""
        mode = options["mode"]
        seed = options["seed"]
        random.seed(seed)
        self.stdout.write(f"Seeding data with mode={mode} and seed={seed}...")
        run_seed(self, mode, seed)
        self.stdout.write("Done.")


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete all model data.")
    Consumer.objects.all().delete()
    Bundle_posting.objects.all().delete()
    Seller.objects.all().delete()
    IssueReport.objects.all().delete()
    Reservation.objects.all().delete()
    User.objects.all().delete()


def create_demo_user(id):
    """Create a fixed demo user"""
    logger.info("Creating demo user")
    demo_user = User.objects.create_user(
        username="demo" + str(id), email=str(id) + "demo@exeter.ac.uk", password="demo"
    )
    demo_user.user_type = "consumer"
    demo_user.save()
    demo_consumer = Consumer.objects.create(pk=id, user=demo_user)
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

    demo_seller_user = User.objects.create_user(
        username="demo_seller", email="demo_seller@exeter.ac.uk", password="demo_seller"
    )
    demo_seller = Seller.objects.create(
        pk=1,
        user=demo_seller_user,
        location="Exeter",
        opening_time=time(9, 0),
        closing_time=time(17, 0),
        telephone_number="441326370400",
        website_url="https://www.exeter.ac.uk/",
    )
    demo_seller_user.user_type = "seller"
    demo_seller_user.save()
    logger.info("{} demo seller created.".format(demo_seller))

    print(f"Username: {demo_seller_user.username}")
    print(f"Email: {demo_seller_user.email}")
    print("Password: demo_seller")
    # demo_seller_user.password will not work for good reason.

    return demo_seller


def run_seed(self, mode, seed):
    """
    Seed database based on mode and seed
    """

    clear_data()
    if mode == MODE_CLEAR:
        return

    # Generate demo user and demo seller (fixed)
    create_demo_user(1)
    create_demo_user(2)
    create_demo_user(3)
    demo_seller = create_demo_seller()
    for category in CATEGORIES:
        Bundle_posting_category.objects.create(name=category)
