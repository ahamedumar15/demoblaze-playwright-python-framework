
from pages.base_page import BasePage
from utils.config import Locators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class LoginModal(BasePage):
    """Login modal interactions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def login(self, username: str, password: str) -> str:
        """Perform login"""
        self.fill(Locators.LOGIN_USERNAME, username)
        self.fill(Locators.LOGIN_PASSWORD, password)

        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            logger.info(f"Login alert: {alert_message}")
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(Locators.LOGIN_SUBMIT)
        self.page.wait_for_timeout(1800)
        return alert_message

    def close_modal(self):
        """Close login modal"""
        self.click(Locators.LOGIN_CLOSE)
        self.wait_for_element(Locators.LOGIN_MODAL, state="hidden")


class SignupModal(BasePage):
    """Signup modal interactions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def signup(self, username: str, password: str) -> str:
        """Perform signup and return alert message"""
        self.fill(Locators.SIGNUP_USERNAME, username)
        self.fill(Locators.SIGNUP_PASSWORD, password)

        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            logger.info(f"Signup alert: {alert_message}")
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(Locators.SIGNUP_SUBMIT)
        self.page.wait_for_timeout(1800)
        return alert_message

    def close_modal(self):
        """Close signup modal"""
        self.click(Locators.SIGNUP_CLOSE)
        self.wait_for_element(Locators.SIGNUP_MODAL, state="hidden")


class ContactModal(BasePage):
    """Contact modal interactions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def send_message(self, email: str, name: str, message: str) -> str:
        """Send contact message and return alert"""
        self.fill(Locators.CONTACT_EMAIL, email)
        self.fill(Locators.CONTACT_NAME, name)
        self.fill(Locators.CONTACT_MESSAGE, message)

        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            logger.info(f"Contact alert: {alert_message}")
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(Locators.CONTACT_SUBMIT)
        self.page.wait_for_timeout(1800)
        return alert_message

    def close_modal(self):
        """Close contact modal"""
        self.click(Locators.CONTACT_CLOSE)
        self.wait_for_element(Locators.CONTACT_MODAL, state="hidden")


class PlaceOrderModal(BasePage):
    """Place order modal interactions"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        super().__init__(page, base_url)

    def fill_order_details(self, name: str, country: str, city: str,
                           card: str, month: str, year: str):
        """Fill order form"""
        self.fill(Locators.ORDER_NAME, name)
        self.fill(Locators.ORDER_COUNTRY, country)
        self.fill(Locators.ORDER_CITY, city)
        self.fill(Locators.ORDER_CARD, card)
        self.fill(Locators.ORDER_MONTH, month)
        self.fill(Locators.ORDER_YEAR, year)

    def click_purchase(self):
        """Click purchase button"""
        self.click(Locators.ORDER_PURCHASE_BTN)
        self.wait_for_element(Locators.SUCCESS_MESSAGE)

    def get_success_message(self) -> str:
        """Get order success message"""
        return self.get_text(Locators.SUCCESS_MESSAGE)

    def click_ok(self):
        """Click OK on success dialog"""
        self.click(Locators.CONFIRM_OK)

    def close_modal(self):
        """Close order modal"""
        self.click(Locators.MODAL_CLOSE)
