
from pages.base_page import BasePage
from utils.config import Locators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Shopping cart page actions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def get_cart_products(self) -> list:
        """Get all products in cart"""
        products = []
        product_rows = self.get_all_elements(Locators.CART_PRODUCT_ROW)

        for row in product_rows:
            try:
                title = row.locator(Locators.CART_PRODUCT_TITLE).inner_text()
                price = row.locator(Locators.CART_PRODUCT_PRICE).inner_text()
                products.append({"title": title, "price": price})
            except:
                continue

        logger.info(f"Cart has {len(products)} products")
        return products

    def get_cart_product_count(self) -> int:
        """Get number of products in cart"""
        return len(self.get_all_elements(Locators.CART_PRODUCT_ROW))

    def get_total_price(self) -> str:
        """Get total cart price"""
        return self.get_text(Locators.CART_TOTAL)

    def delete_product_by_title(self, product_title: str):
        """Delete specific product from cart"""
        product_rows = self.get_all_elements(Locators.CART_PRODUCT_ROW)
        for row in product_rows:
            title = row.locator(Locators.CART_PRODUCT_TITLE).inner_text()
            if title == product_title:
                row.locator(Locators.DELETE_PRODUCT).click()
                self.page.wait_for_timeout(1000)
                return
        raise ValueError(f"Product '{product_title}' not found in cart")

    def delete_first_product(self):
        """Delete the first product in cart"""
        delete_buttons = self.get_all_elements(Locators.DELETE_PRODUCT)
        if delete_buttons:
            delete_buttons[0].click()
            self.page.wait_for_timeout(1000)
        else:
            raise ValueError("No products in cart to delete")

    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.get_cart_product_count() == 0

    def click_place_order(self):
        """Click place order button and wait for modal"""
        self.click(Locators.PLACE_ORDER_BTN)
        self.wait_for_element("#orderModal.show")

    def navigate_to_home(self):
        """Go back to home page"""
        self.click(Locators.HOME_LINK)
        self.page.wait_for_url(f"{self.base_url}/index.html")
