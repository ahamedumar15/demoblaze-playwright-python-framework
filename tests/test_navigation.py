
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestNavigation:
    """Test cases for site navigation"""

    @pytest.mark.smoke
    def test_navigate_to_home(self, page: Page, base_url: str):
        """Test navigation to home page"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()

        # Assert
        assert base_url in page.url, "Should be on home page"
        assert home_page.is_visible(".navbar-brand"), "Should see logo"

    @pytest.mark.smoke
    def test_navigate_to_cart(self, page: Page, base_url: str):
        """Test navigation to cart page"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_cart()

        # Assert
        assert "cart.html" in page.url, "Should be on cart page"

    @pytest.mark.regression
    def test_navigation_menu_links_visible(self, page: Page, base_url: str):
        """Test all navigation menu links are visible"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()

        # Assert
        assert home_page.is_visible("a:has-text('Home')"), "Home link should be visible"
        assert home_page.is_visible("a:has-text('Contact')"), "Contact link should be visible"
        assert home_page.is_visible("a:has-text('About us')"), "About link should be visible"
        assert home_page.is_visible("a#cartur"), "Cart link should be visible"

    @pytest.mark.regression
    def test_logo_navigation(self, page: Page, base_url: str):
        """Test clicking logo navigates to home"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")

        # Click logo
        page.click(".navbar-brand")
        page.wait_for_load_state("domcontentloaded")

        # Assert
        assert "index.html" in page.url or page.url == f"{base_url}/", "Should return to home"

    @pytest.mark.regression
    def test_category_navigation(self, page: Page, base_url: str):
        """Test category links are functional"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()

        # Assert each category is clickable
        assert home_page.is_visible("a:has-text('Phones')"), "Phones category should be visible"
        assert home_page.is_visible("a:has-text('Laptops')"), "Laptops category should be visible"
        assert home_page.is_visible("a:has-text('Monitors')"), "Monitors category should be visible"

    @pytest.mark.regression
    def test_breadcrumb_navigation_from_product(self, page: Page, base_url: str):
        """Test navigating back from product page"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")

        # Navigate back
        product_page.click_home()

        # Assert
        assert "index.html" in page.url or page.url.endswith("/"), "Should be back on home"

    @pytest.mark.smoke
    def test_about_modal_opens(self, page: Page, base_url: str):
        """Test About Us modal opens"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_about()

        # Assert
        assert home_page.is_visible("#videoModal.show"), "About modal should be open"

    @pytest.mark.regression
    def test_responsive_navigation_elements(self, page: Page, base_url: str):
        """Test navigation elements are present"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()

        # Assert - Check key navigation elements exist
        assert page.locator(".navbar").is_visible(), "Navigation bar should be visible"
        assert page.locator("#navbarExample").is_visible(), "Navigation items should be visible"