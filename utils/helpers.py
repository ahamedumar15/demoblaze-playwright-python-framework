
import logging
import json
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def log_test_info(test_name: str, message: str):
    """Log test information"""
    logger.info(f"[{test_name}] {message}")


def log_test_error(test_name: str, error: str):
    """Log test errors"""
    logger.error(f"[{test_name}] ERROR: {error}")


def generate_timestamp() -> str:
    """Generate timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_to_json(data: Dict[str, Any], filename: str):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {filename}")


def load_from_json(filename: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    logger.info(f"Data loaded from {filename}")
    return data


def format_price(price_str: str) -> float:
    """Convert price string to float"""
    # Remove dollar sign and convert to float
    return float(price_str.replace('$', '').strip())


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
    """Wait for a condition to be true"""
    import time
    start_time = time.time()

    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)

    return False


class TestDataValidator:
    """Validate test data"""

    @staticmethod
    def validate_product_data(product: Dict[str, str]) -> bool:
        """Validate product data structure"""
        required_fields = ['title', 'price']
        return all(field in product for field in required_fields)

    @staticmethod
    def validate_cart_data(cart_item: Dict[str, str]) -> bool:
        """Validate cart item data"""
        required_fields = ['title', 'price']
        return all(field in cart_item for field in required_fields)


class StringHelper:
    """String manipulation helpers"""

    @staticmethod
    def extract_numbers(text: str) -> str:
        """Extract numbers from string"""
        import re
        return ''.join(re.findall(r'\d+', text))

    @staticmethod
    def clean_whitespace(text: str) -> str:
        """Remove extra whitespace"""
        return ' '.join(text.split())


