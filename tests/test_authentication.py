
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.modals import LoginModal, SignupModal
from utils.config import Messages
from utils.test_data import TestDataFactory


class TestAuthentication:
    """Test cases for user authentication"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_signup(self, page: Page, base_url: str, unique_username: str):
        """Test user can successfully sign up with valid credentials"""
        # Arrange
        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_signup()
        message = signup_modal.signup(unique_username, "Test@123456")

        # Assert
        assert message == Messages.SIGNUP_SUCCESS, f"Expected success message, got: {message}"

    @pytest.mark.regression
    def test_signup_with_existing_user(self, page: Page, base_url: str):
        """Test signup fails with existing username"""
        # Arrange
        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)
        existing_user = "testuser_existing"

        # Act
        home_page.navigate()
        home_page.click_signup()
        message = signup_modal.signup(existing_user, "Password123")

        # Assert
        assert "already exist" in message.lower(), f"Expected 'already exist' in message, got: {message}"

    @pytest.mark.regression
    def test_signup_with_empty_fields(self, page: Page, base_url: str):
        """Test signup validation with empty fields"""
        # Arrange
        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)

        # Act
        home_page.navigate()
        home_page.click_signup()
        message = signup_modal.signup("", "")

        # Assert
        assert "fill out" in message.lower(), f"Expected validation message, got: {message}"

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, page: Page, base_url: str, unique_username: str):
        """Test user can login with valid credentials"""
        # Arrange - First create user
        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)
        login_modal = LoginModal(page, base_url)
        password = "Test@123456"

        # Create user
        home_page.navigate()
        home_page.click_signup()
        signup_modal.signup(unique_username, password)
        page.wait_for_timeout(1000)
        #signup_modal.close_modal()

        # Act - Login
        home_page.click_login()
        login_modal.login(unique_username, password)

        # Assert
        assert home_page.is_logged_in(), "User should be logged in"
        assert unique_username in home_page.get_logged_username(), "Logged username should match"

    @pytest.mark.regression
    def test_login_with_invalid_credentials(self, page: Page, base_url: str):
        """Test login fails with invalid credentials"""
        # Arrange
        home_page = HomePage(page, base_url)
        login_modal = LoginModal(page, base_url)

        # Setup alert handler
        alert_message = None

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)

        # Act
        home_page.navigate()
        home_page.click_login()
        login_modal.login("nonexistent_user_12345", "WrongPassword")

        # Wait for alert
        page.wait_for_timeout(2000)

        # Assert
        assert alert_message is not None, "Should show error message"
        assert "does not exist" in alert_message.lower() or "wrong password" in alert_message.lower()

    @pytest.mark.smoke
    def test_logout_functionality(self, page: Page, base_url: str, unique_username: str):
        """Test user can logout successfully"""
        # Arrange - Login first
        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)
        login_modal = LoginModal(page, base_url)
        password = "Test@123456"

        home_page.navigate()
        home_page.click_signup()
        signup_modal.signup(unique_username, password)
        page.wait_for_timeout(1000)
        #signup_modal.close_modal()

        home_page.click_login()
        login_modal.login(unique_username, password)
        page.wait_for_timeout(1000)

        # Act
        home_page.click_logout()

        # Assert
        assert not home_page.is_logged_in(), "User should be logged out"

    @pytest.mark.regression
    def test_login_does_not_persist_after_page_reload(self, page: Page, base_url: str, unique_username: str):
        """Test login session is lost after page reload (Demoblaze behavior)"""

        home_page = HomePage(page, base_url)
        signup_modal = SignupModal(page, base_url)
        login_modal = LoginModal(page, base_url)
        password = "Test@123456"

        home_page.navigate()
        home_page.click_signup()
        signup_modal.signup(unique_username, password)

        home_page.click_login()
        login_modal.login(unique_username, password)

        home_page.reload_page()

        assert not home_page.is_logged_in(), \
            "User should be logged out after reload"
