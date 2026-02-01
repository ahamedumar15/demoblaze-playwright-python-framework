
from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class TestUser:
    """Test user data"""
    username: str
    password: str


@dataclass
class ContactInfo:
    """Contact form data"""
    email: str
    name: str
    message: str


@dataclass
class OrderInfo:
    """Order/checkout data"""
    name: str
    country: str
    city: str
    card: str
    month: str
    year: str


class TestDataFactory:
    """Factory for generating test data"""

    @staticmethod
    def create_user() -> TestUser:
        """Generate random user data"""
        return TestUser(
            username=fake.user_name() + fake.random_number(digits=4, fix_len=True).__str__(),
            password=fake.password(length=10)
        )

    @staticmethod
    def create_contact_info() -> ContactInfo:
        """Generate contact form data"""
        return ContactInfo(
            email=fake.email(),
            name=fake.name(),
            message=fake.text(max_nb_chars=100)
        )

    @staticmethod
    def create_order_info() -> OrderInfo:
        """Generate order data"""
        return OrderInfo(
            name=fake.name(),
            country=fake.country(),
            city=fake.city(),
            card=fake.credit_card_number(),
            month=fake.month_name(),
            year=str(fake.year())
        )


# Predefined test data
VALID_PRODUCTS = [
    "Samsung galaxy s6",
    "Nokia lumia 1520",
    "Nexus 6",
    "Samsung galaxy s7",
    "Iphone 6 32gb",
    "Sony xperia z5",
    "HTC One M9",
    "Sony vaio i5",
    "Sony vaio i7",
    "MacBook air",
    "Dell i7 8gb",
    "2017 Dell 15.6 Inch",
    "ASUS Full HD",
    "MacBook Pro",
    "Apple monitor 24"
]

CATEGORIES = ["Phones", "Laptops", "Monitors"]