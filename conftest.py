
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from typing import Generator
import os
from datetime import datetime


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with additional settings"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new page for each test"""
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds
    yield page
    page.close()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Automatically capture screenshot on test failure"""
    yield
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = f"{screenshot_dir}/{request.node.name}_{timestamp}.png"
        try:
            page.screenshot(path=screenshot_path, timeout=5000)
            print(f"\nScreenshot saved: {screenshot_path}")
        except Exception as ex:
            print(f"\nScreenshot capture failed for {request.node.name}: {ex}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test results available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    return "https://www.demoblaze.com"


@pytest.fixture
def unique_username():
    """Generate unique username for testing"""
    timestamp = datetime.now().strftime("%H%M%S%f")
    return f"tu_{timestamp}"


@pytest.fixture
def test_credentials():
    """Standard test credentials"""
    return {
        "username": "testuser_demo",
        "password": "Test@123"
    }