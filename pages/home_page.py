
from pages.base_page import BasePage
from utils.config import Locators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Home page actions and elements"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def click_login(self):
        """Click login link and wait for login modal"""
        self.click(Locators.LOGIN_LINK)
        self.wait_for_element("#logInModal.show")

    def click_signup(self):
        """Click signup link and wait for signup modal"""
        self.click(Locators.SIGNUP_LINK)
        self.wait_for_element("#signInModal.show")

    def click_cart(self):
        """Navigate to cart page"""
        self.page.wait_for_timeout(800)
        self.click(Locators.CART_LINK)
        self.page.wait_for_url(f"{self.base_url}/cart.html")

    def click_contact(self):
        """Open contact modal"""
        self.click(Locators.CONTACT_LINK)
        self.wait_for_element("#exampleModal.show")

    def click_about(self):
        """Open about modal"""
        self.click(Locators.ABOUT_LINK)
        self.wait_for_element("#videoModal.show")

    def click_logout(self):
        """Logout user"""
        self.click(Locators.LOGOUT_LINK)
        self.page.wait_for_timeout(1000)

    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        for _ in range(8):
            if self.is_visible(Locators.LOGGED_USER):
                return True
            self.page.wait_for_timeout(500)
        return False

    def get_logged_username(self) -> str:
        """Get logged in username"""
        if self.is_logged_in():
            text = self.get_text(Locators.LOGGED_USER)
            return text.replace("Welcome ", "")
        return ""

    def select_category(self, category: str):
        """Select product category and wait for products to load"""
        category_map = {
            "Phones": Locators.PHONES_CATEGORY,
            "Laptops": Locators.LAPTOPS_CATEGORY,
            "Monitors": Locators.MONITORS_CATEGORY
        }

        if category not in category_map:
            raise ValueError(f"Invalid category: {category}")

        self.click(category_map[category])
        self.wait_for_element(Locators.PRODUCT_TITLE, timeout=10000)
        self.page.wait_for_timeout(1200)

    def get_all_products(self) -> list:
        """Get all product cards on current page"""
        products = []
        self.wait_for_element(Locators.PRODUCT_TITLE, timeout=10000)
        title_locators = self.page.locator(Locators.PRODUCT_TITLE).all()

        for title_locator in title_locators:
            try:
                card = title_locator.locator("xpath=ancestor::div[contains(@class, 'card')]" ).first
                title = title_locator.inner_text().strip()
                price = card.locator(Locators.PRODUCT_PRICE).inner_text().strip()
                products.append({"title": title, "price": price})
            except:
                continue

        logger.info(f"Found {len(products)} products")
        return products

    def click_product_by_name(self, product_name: str):
        """Click on a product by its name"""
        self.page.locator(f".card-title >> text={product_name}").first.click()
        self.page.wait_for_url("**/prod.html**", timeout=12000)
        self.wait_for_element(".name", timeout=12000)  # Wait until product page loads

    def get_product_count(self) -> int:
        """Get count of visible products"""
        return len(self.get_all_elements(Locators.PRODUCT_CARD))

    def click_next_page(self):
        """Click next button in pagination"""
        if self.is_visible(Locators.NEXT_PAGE):
            self.click(Locators.NEXT_PAGE)
            self.wait_for_element(Locators.PRODUCT_CARD)

    def click_previous_page(self):
        """Click previous button in pagination"""
        if self.is_visible(Locators.PREVIOUS_PAGE):
            self.click(Locators.PREVIOUS_PAGE)
            self.wait_for_element(Locators.PRODUCT_CARD)

    def is_next_button_visible(self) -> bool:
        """Check whether the next pagination button is visible"""
        return self.is_visible(Locators.NEXT_PAGE)

    def is_previous_button_visible(self) -> bool:
        """Check whether the previous pagination button is visible"""
        return self.is_visible(Locators.PREVIOUS_PAGE)
