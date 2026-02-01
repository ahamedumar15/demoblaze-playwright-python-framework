
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Environment configurations"""
    PRODUCTION = "https://www.demoblaze.com"


@dataclass
class Config:
    """Application configuration"""
    BASE_URL: str = Environment.PRODUCTION.value
    DEFAULT_TIMEOUT: int = 30000
    SLOW_TIMEOUT: int = 60000

    # Test data
    DEFAULT_PASSWORD: str = "Test@123"

    # Waits
    SHORT_WAIT: int = 3000
    MEDIUM_WAIT: int = 5000
    LONG_WAIT: int = 10000


class Locators:
    """Centralized locators for the application"""

    # Navigation
    HOME_LINK = "a.nav-link:has-text('Home')"
    CONTACT_LINK = "a.nav-link:has-text('Contact')"
    ABOUT_LINK = "a.nav-link:has-text('About us')"
    CART_LINK = "a#cartur"
    LOGIN_LINK = "a#login2"
    LOGOUT_LINK = "a#logout2"
    SIGNUP_LINK = "a#signin2"

    # Categories
    PHONES_CATEGORY = "a:has-text('Phones')"
    LAPTOPS_CATEGORY = "a:has-text('Laptops')"
    MONITORS_CATEGORY = "a:has-text('Monitors')"

    # Product list
    PRODUCT_CARD = ".card"
    PRODUCT_TITLE = ".card-title a"
    PRODUCT_PRICE = ".card-block h5"

    # Modals
    MODAL_TITLE = ".modal-title"
    MODAL_CLOSE = "button:has-text('Close')"

    # Signup Modal
    SIGNUP_MODAL = "#signInModal"
    SIGNUP_CLOSE = "#signInModal button.btn-secondary"

    # Login Modal
    LOGIN_MODAL = "#logInModal"
    LOGIN_CLOSE = "#logInModal button.btn-secondary"

    # Contact Modal
    CONTACT_MODAL = "#exampleModal"
    CONTACT_CLOSE = "#exampleModal button.btn-secondary"

    # Login Modal
    LOGIN_USERNAME = "#loginusername"
    LOGIN_PASSWORD = "#loginpassword"
    LOGIN_SUBMIT = "button:has-text('Log in')"

    # Signup Modal
    SIGNUP_USERNAME = "#sign-username"
    SIGNUP_PASSWORD = "#sign-password"
    SIGNUP_SUBMIT = "button:has-text('Sign up')"


    # Contact Modal
    CONTACT_EMAIL = "#recipient-email"
    CONTACT_NAME = "#recipient-name"
    CONTACT_MESSAGE = "#message-text"
    CONTACT_SUBMIT = "button:has-text('Send message')"

    # Product Page
    PRODUCT_NAME = "h2.name"
    PRODUCT_DESCRIPTION = "#more-information p"
    ADD_TO_CART_BTN = "a:has-text('Add to cart')"

    # Cart Page
    CART_PRODUCT_ROW = "tr.success"
    CART_PRODUCT_TITLE = "td:nth-child(2)"
    CART_PRODUCT_PRICE = "td:nth-child(3)"
    DELETE_PRODUCT = "a:has-text('Delete')"
    PLACE_ORDER_BTN = "button:has-text('Place Order')"
    CART_TOTAL = "#totalp"

    # Place Order Modal
    ORDER_NAME = "#name"
    ORDER_COUNTRY = "#country"
    ORDER_CITY = "#city"
    ORDER_CARD = "#card"
    ORDER_MONTH = "#month"
    ORDER_YEAR = "#year"
    ORDER_PURCHASE_BTN = "button:has-text('Purchase')"

    # Success confirmation
    SUCCESS_MESSAGE = ".sweet-alert h2"
    CONFIRM_OK = ".confirm"

    # User indicator
    LOGGED_USER = "#nameofuser"


class Messages:
    """Expected messages and text"""
    SIGNUP_SUCCESS = "Sign up successful."
    LOGIN_USER_NOT_EXIST = "User does not exist."
    LOGIN_WRONG_PASSWORD = "Wrong password."
    PRODUCT_ADDED = "Product added"
    ORDER_SUCCESS = "Thank you for your purchase!"
    CONTACT_SUCCESS = "Thanks for the message!!"

    # Validation messages
    FILL_USERNAME = "Please fill out Username and Password."