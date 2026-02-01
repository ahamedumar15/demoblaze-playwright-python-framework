
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common utilities"""

    def __init__(self, page: Page, base_url: str = "https://www.demoblaze.com"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = ""):
        url = f"{self.base_url}/{path}".rstrip("/")
        self.page.goto(url)
        logger.info(f"Navigated to {url}")

    def click(self, locator: str):
        self.page.locator(locator).click()
        logger.info(f"Clicked element: {locator}")

    def fill(self, locator: str, text: str):
        self.page.locator(locator).fill(text)
        logger.info(f"Filled element: {locator} with text: {text}")

    def get_text(self, locator: str) -> str:
        text = self.page.locator(locator).inner_text()
        logger.info(f"Got text from {locator}: {text}")
        return text

    def is_visible(self, locator: str) -> bool:
        visible = self.page.locator(locator).is_visible()
        logger.info(f"Element {locator} visible: {visible}")
        return visible

    def get_all_elements(self, locator: str) -> list:
        elements = self.page.locator(locator).all()
        logger.info(f"Found {len(elements)} elements with locator: {locator}")
        return elements

    def wait_for_element(self, locator: str, state: str = "visible", timeout: int = 5000):
        self.page.locator(locator).wait_for(state=state, timeout=timeout)
        logger.info(f"Waited for element {locator} to be {state}")

    def wait_for_url(self, url: str, timeout: int = 5000):
        self.page.wait_for_url(url, timeout=timeout)
        logger.info(f"Waited for URL: {url}")

    def reload_page(self):
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")
