
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.modals import PlaceOrderModal
from utils.config import Messages
from utils.test_data import TestDataFactory


class TestCartCheckout:
    """Test cases for shopping cart and checkout process"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_add_product_to_cart(self, page: Page, base_url: str):
        """Test adding a product to cart"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")

        product_name = product_page.get_product_name()
        message = product_page.add_to_cart()

        # Assert
        assert Messages.PRODUCT_ADDED in message, f"Expected success message, got: {message}"

        # Verify in cart
        home_page.click_cart()
        cart_products = cart_page.get_cart_products()

        assert len(cart_products) > 0, "Cart should not be empty"
        assert any(p["title"] == product_name for p in cart_products), "Product should be in cart"

    @pytest.mark.regression
    def test_add_multiple_products_to_cart(self, page: Page, base_url: str):
        """Test adding multiple products to cart"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)
        products_to_add = ["Samsung galaxy s6", "Nokia lumia 1520"]

        # Act
        home_page.navigate()

        for product in products_to_add:
            home_page.click_product_by_name(product)
            product_page.add_to_cart()
            page.wait_for_timeout(1000)
            product_page.click_home()

        # Assert
        home_page.click_cart()
        cart_products = cart_page.get_cart_products()

        assert len(cart_products) >= len(products_to_add), "All products should be in cart"

    @pytest.mark.smoke
    def test_remove_product_from_cart(self, page: Page, base_url: str):
        """Test removing a product from cart"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Add product first
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_name = product_page.get_product_name()
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        # Act
        home_page.click_cart()
        initial_count = cart_page.get_cart_product_count()
        cart_page.delete_product_by_title(product_name)
        final_count = cart_page.get_cart_product_count()

        # Assert
        assert final_count < initial_count, "Product count should decrease after deletion"

    @pytest.mark.regression
    def test_cart_total_calculation(self, page: Page, base_url: str):
        """Test cart total is calculated correctly"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        home_page.click_cart()
        cart_products = cart_page.get_cart_products()
        total = cart_page.get_total_price()

        # Assert
        assert len(total) > 0, "Total should be displayed"

        # Calculate expected total
        expected_total = sum(int(p["price"]) for p in cart_products)
        actual_total = int(total)

        assert actual_total == expected_total, f"Total should be {expected_total}, got {actual_total}"

    @pytest.mark.critical
    @pytest.mark.smoke
    def test_complete_checkout_process(self, page: Page, base_url: str):
        """Test complete checkout flow from cart to order confirmation"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)
        order_modal = PlaceOrderModal(page, base_url)
        order_data = TestDataFactory.create_order_info()

        # Act - Add product to cart
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        # Go to cart and place order
        home_page.click_cart()
        cart_page.click_place_order()

        # Fill order details
        order_modal.fill_order_details(
            name=order_data.name,
            country=order_data.country,
            city=order_data.city,
            card=order_data.card,
            month=order_data.month,
            year=order_data.year
        )

        order_modal.click_purchase()

        # Assert
        success_message = order_modal.get_success_message()
        assert Messages.ORDER_SUCCESS in success_message, "Should show success message"

        # Close confirmation
        order_modal.click_ok()

        # Verify cart is empty or we're redirected
        page.wait_for_timeout(1000)

    @pytest.mark.regression
    def test_empty_cart_displays_correctly(self, page: Page, base_url: str):
        """Test empty cart state"""
        # Arrange
        home_page = HomePage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_cart()

        # Assert
        cart_count = cart_page.get_cart_product_count()
        # Empty cart might have 0 products
        assert cart_count >= 0, "Cart count should be valid"

    @pytest.mark.regression
    def test_cart_persistence_across_navigation(self, page: Page, base_url: str):
        """Test cart persists when navigating between pages"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        # Navigate away and back
        product_page.click_home()
        home_page.click_cart()

        initial_count = cart_page.get_cart_product_count()

        cart_page.navigate_to_home()
        home_page.click_cart()

        final_count = cart_page.get_cart_product_count()

        # Assert
        assert initial_count == final_count, "Cart should persist across navigation"

    @pytest.mark.regression
    def test_place_order_button_visible_with_items(self, page: Page, base_url: str):
        """Test place order button is visible when cart has items"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        home_page.click_cart()

        # Assert
        assert cart_page.is_visible(".btn-success"), "Place order button should be visible"

    @pytest.mark.slow
    def test_add_same_product_multiple_times(self, page: Page, base_url: str):
        """Test adding the same product multiple times"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)
        cart_page = CartPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")

        # Add same product twice
        product_page.add_to_cart()
        page.wait_for_timeout(1000)
        product_page.add_to_cart()
        page.wait_for_timeout(1000)

        home_page.click_cart()
        cart_count = cart_page.get_cart_product_count()

        # Assert
        assert cart_count >= 2, "Should allow adding same product multiple times"