
from pages.base_page import BasePage
from utils.config import Locators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Product detail page actions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def get_product_name(self) -> str:
        """Get product name"""
        return self.get_text(Locators.PRODUCT_NAME)

    def get_product_price(self) -> str:
        """Get product price"""
        price_section = self.page.locator(".price-container").inner_text()
        # Extract price from text like "$790 *includes tax"
        return price_section.split("*")[0].strip()

    def get_product_description(self) -> str:
        """Get product description"""
        return self.get_text(Locators.PRODUCT_DESCRIPTION)

    def add_to_cart(self) -> str:
        """Add product to cart and return alert message"""
        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            logger.info(f"Add to cart alert: {alert_message}")
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(Locators.ADD_TO_CART_BTN)
        try:
            self.page.wait_for_response(lambda response: "addtocart" in response.url and response.ok, timeout=8000)
        except:
            pass
        self.page.wait_for_timeout(1500)
        return alert_message

    def click_home(self):
        """Navigate back to home"""
        self.click(Locators.HOME_LINK)
        self.wait_for_url(f"{self.base_url}/index.html")

    def is_product_image_visible(self) -> bool:
        """Check if product image is displayed"""
        return self.is_visible(".product-image img, .item img")