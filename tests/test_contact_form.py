
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.modals import ContactModal
from utils.config import Messages
from utils.test_data import TestDataFactory


class TestContactForm:
    """Test cases for contact form functionality"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_send_contact_message_success(self, page: Page, base_url: str):
        """Test sending a contact message successfully"""
        # Arrange
        home_page = HomePage(page, base_url)
        contact_modal = ContactModal(page, base_url)
        contact_data = TestDataFactory.create_contact_info()

        # Act
        home_page.navigate()
        home_page.click_contact()

        message = contact_modal.send_message(
            email=contact_data.email,
            name=contact_data.name,
            message=contact_data.message
        )

        # Assert
        assert Messages.CONTACT_SUCCESS in message, f"Expected success message, got: {message}"

    @pytest.mark.regression
    def test_contact_form_validation_empty_fields(self, page: Page, base_url: str):
        """Test contact form validation with empty fields"""
        # Arrange
        home_page = HomePage(page, base_url)
        contact_modal = ContactModal(page, base_url)

        # Setup alert handler
        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)

        # Act
        home_page.navigate()
        home_page.click_contact()
        contact_modal.send_message("", "", "")

        page.wait_for_timeout(1000)

        # Assert
        assert alert_message is not None, "Should show validation message"

    @pytest.mark.regression
    def test_close_contact_modal(self, page: Page, base_url: str):
        """Test closing contact modal"""
        # Arrange
        home_page = HomePage(page, base_url)
        contact_modal = ContactModal(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_contact()

        assert contact_modal.is_visible("#exampleModal.show"), "Modal should be visible"

        contact_modal.close_modal()
        page.wait_for_timeout(500)

        # Assert
        assert not contact_modal.is_visible("#exampleModal.show"), "Modal should be closed"

    @pytest.mark.regression
    def test_contact_form_with_special_characters(self, page: Page, base_url: str):
        """Test contact form handles special characters"""
        # Arrange
        home_page = HomePage(page, base_url)
        contact_modal = ContactModal(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_contact()

        message = contact_modal.send_message(
            email="test+special@example.com",
            name="Test O'Brien",
            message="Testing special chars: !@#$%^&*()"
        )

        # Assert
        assert Messages.CONTACT_SUCCESS in message, "Should handle special characters"


