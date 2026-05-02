# DemoBlaze E-Commerce Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.57.0-green.svg)
![Pytest](https://img.shields.io/badge/Pytest-9.0.2-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python-based UI test automation framework for the DemoBlaze e-commerce application, built using Playwright and pytest. The framework follows the Page Object Model (POM) to ensure clean separation between test logic and browser interactions, with a focus on maintainability, scalability, and reliable execution.

Application under test: https://www.demoblaze.com/

---

## Overview

This project demonstrates a practical QA automation framework designed to validate core e-commerce workflows.

Key focus areas:
- Clean architecture using Page Object Model
- Stable execution using Playwright auto-waiting
- Structured test organization using pytest markers
- CI/CD readiness with GitHub Actions and Docker

---

## Current Status

- Smoke tests are implemented and passing
- Regression, critical, and slow markers are available
- CI workflows configured for automated runs and Allure reporting
- Dockerized execution supported
- Total tests: 42

---

## Scope

The framework currently covers:

- Authentication and session handling
- Product catalog navigation and filtering
- Product detail interactions
- Cart operations and checkout flow
- Contact form submission
- Navigation and modal interactions

---

## Repository Layout

```
conftest.py
pytest.ini
README.md
requirements.txt
Dockerfile
docker-compose.yml
.github/workflows/
pages/
tests/
utils/
```

---

## Technology Stack

- Python
- Playwright
- pytest
- pytest-playwright
- pytest-xdist
- pytest-html
- allure-pytest
- Faker

---

## Test Coverage

### Coverage Breakdown

| Area | Tests | Focus |
|------|------|-------|
| Authentication | 6 | Login, signup, session |
| Product Catalog | 9 | Filtering, listing |
| Product Details | 5 | Validation |
| Cart & Checkout | 10 | Cart and checkout flow |
| Contact Form | 4 | Submission |
| Navigation and UI | 8 | Modals and navigation |
| Total | 42 | Core flows |

### Coverage Highlights

- End-to-end coverage of core user journeys
- UI validation across multiple interaction paths
- Cart state persistence validation
- Form and modal interaction coverage
- Marker-based execution strategy (smoke, regression, critical, slow)

---

## Prerequisites

- Python 3.8 or later
- pip
- Git

---

## Installation

```bash
git clone https://github.com/ahamedumar15/demoblaze-playwright-python-framework.git
cd demoblaze-playwright-python-framework

python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m playwright install
```

---

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run specific suites:

```bash
python -m pytest -m smoke -v
python -m pytest -m regression -v
python -m pytest -m critical -v
python -m pytest -m slow -v
```

Run in parallel:

```bash
python -m pytest -n auto -v
```

Generate reports:

```bash
python -m pytest --html=reports/report.html --self-contained-html
python -m pytest --alluredir=allure-results
```

---

## Reporting

- HTML reports in reports/
- Allure results in allure-results/

CI configuration:
.github/workflows/allure-report.yml

---

## Continuous Integration and Docker

- CI pipeline: .github/workflows/ci.yml
- Allure publishing: .github/workflows/allure-report.yml
- Docker: Dockerfile, docker-compose.yml

Run using Docker:

```bash
docker compose up --build
```

---

## Framework Design

The framework follows the Page Object Model.

- pages/base_page.py: shared browser actions
- pages/home_page.py: catalog navigation
- pages/product_page.py: product interactions
- pages/cart_page.py: cart operations
- pages/modals.py: modal handling

---

## Test Data and Utilities

- utils/config.py: configuration and locators
- utils/test_data.py: test data
- utils/helpers.py: shared helper functions

---

## Skills and Competencies Demonstrated

### Automation
- Playwright UI automation
- pytest (fixtures, markers, parametrization)
- Cross-browser testing
- Parallel execution
- Debugging using screenshots and traces

### Programming
- Python-based automation
- Modular framework design
- Reusable abstraction layers

### DevOps
- GitHub Actions CI/CD
- Docker-based execution
- Allure reporting

### QA Engineering Practices
- Test categorization
- Maintainable POM architecture
- Stable execution with reduced flakiness
- Separation of concerns

---

## Future Improvements

- API testing integration
- External test data management
- Visual regression testing
- Performance testing hooks
- Flakiness detection strategies

---

## Notes

- Reflects the current working state of the repository
- Designed for portfolio and internship evaluation
- Focused on practical QA implementation

---

## Conclusion

This project demonstrates a structured QA automation framework using modern tools and practices.

It highlights:
- Practical Playwright and pytest implementation
- Scalable and maintainable test design
- CI/CD integration
- Emphasis on reliability and clarity

---

## Contact

Umar Ahamed  
QA Automation Engineer  

GitHub: https://github.com/ahamedumar15  
LinkedIn: https://www.linkedin.com/in/ahamed-umar/  
Email: ahamedumar825@gmail.com  

---

If you found this project useful, consider giving it a star.
