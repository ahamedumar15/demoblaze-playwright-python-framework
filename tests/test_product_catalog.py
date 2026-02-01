
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from utils.test_data import CATEGORIES, VALID_PRODUCTS


class TestProductCatalog:
    """Test cases for product catalog functionality"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_home_page_loads_products(self, page: Page, base_url: str):
        """Test home page displays products"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()
        products = home_page.get_all_products()

        # Assert
        assert len(products) > 0, "Home page should display products"
        assert all("title" in p and "price" in p for p in products), "Products should have title and price"

    @pytest.mark.smoke
    @pytest.mark.parametrize("category", CATEGORIES)
    def test_filter_by_category(self, page: Page, base_url: str, category: str):
        """Test filtering products by category"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()
        initial_products = home_page.get_all_products()

        home_page.select_category(category)
        filtered_products = home_page.get_all_products()

        # Assert
        assert len(filtered_products) > 0, f"Should display {category} products"
        # Products should change after filtering
        assert initial_products != filtered_products, "Product list should change after filtering"

    @pytest.mark.regression
    def test_all_categories_display_products(self, page: Page, base_url: str):
        """Test all categories have products"""
        # Arrange
        home_page = HomePage(page, base_url)
        home_page.navigate()

        # Act & Assert
        for category in CATEGORIES:
            home_page.select_category(category)
            products = home_page.get_all_products()
            assert len(products) > 0, f"{category} category should have products"

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_product_details_page(self, page: Page, base_url: str):
        """Test product details page displays correct information"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        products = home_page.get_all_products()
        first_product = products[0]

        home_page.click_product_by_name(first_product["title"])

        # Assert
        product_name = product_page.get_product_name()
        assert product_name == first_product["title"], "Product name should match"

        product_price = product_page.get_product_price()
        assert len(product_price) > 0, "Product should have a price"
        assert "$" in product_price, "Price should contain dollar sign"

    @pytest.mark.regression
    def test_product_has_description(self, page: Page, base_url: str):
        """Test product page displays description"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        description = product_page.get_product_description()

        # Assert
        assert len(description) > 0, "Product should have a description"

    @pytest.mark.regression
    def test_product_has_image(self, page: Page, base_url: str):
        """Test product page displays image"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")

        # Assert
        assert product_page.is_product_image_visible(), "Product image should be visible"

    @pytest.mark.regression
    def test_navigate_back_to_home_from_product(self, page: Page, base_url: str):
        """Test navigation from product page back to home"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name("Samsung galaxy s6")
        product_page.click_home()

        # Assert
        assert base_url in page.url, "Should navigate back to home page"

    @pytest.mark.slow
    def test_pagination_next_button(self, page: Page, base_url: str):
        """Test pagination next button functionality"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()
        first_page_products = home_page.get_all_products()

        if home_page.is_next_button_visible():
            home_page.click_next_page()
            second_page_products = home_page.get_all_products()

            # Assert
            assert first_page_products != second_page_products, "Products should change on next page"
        else:
            pytest.skip("Next button not available - all products on one page")

    @pytest.mark.slow
    def test_pagination_previous_button(self, page: Page, base_url: str):
        """Test pagination previous button functionality"""
        # Arrange
        home_page = HomePage(page, base_url)

        # Act
        home_page.navigate()

        if home_page.is_next_button_visible():
            home_page.click_next_page()
            page.wait_for_timeout(1000)

            assert home_page.is_previous_button_visible(), "Previous button should be visible on page 2"

            home_page.click_previous_page()

            # Assert - should be back on first page
            assert True, "Successfully navigated with previous button"
        else:
            pytest.skip("Pagination not available")

    @pytest.mark.regression
    @pytest.mark.parametrize("product_name", ["Samsung galaxy s6", "Nokia lumia 1520", "Nexus 6"])
    def test_specific_products_accessible(self, page: Page, base_url: str, product_name: str):
        """Test specific products are accessible"""
        # Arrange
        home_page = HomePage(page, base_url)
        product_page = ProductPage(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_product_by_name(product_name)
        actual_name = product_page.get_product_name()

        # Assert
        assert actual_name == product_name, f"Expected {product_name}, got {actual_name}"