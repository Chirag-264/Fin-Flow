import datetime
import re

def format_currency(amount):
    """Formats a number into a currency string."""
    return f"${amount:,.2f}"

def validate_email(email):
    """Validates an email format."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def calculate_budget_surplus(income, expenses):
    """Calculates the remaining budget after expenses."""
    return income - expenses

def categorize_expense(amount):
    """Categorizes an expense based on amount."""
    if amount < 50:
        return "Low"
    elif 50 <= amount < 200:
        return "Medium"
    else:
        return "High"

def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.date.today().strftime("%Y-%m-%d")

def reward_eligibility(expenses, threshold=500):
    """Determines if a user qualifies for a reward based on expense threshold."""
    return expenses < threshold

def sanitize_input(text):
    """Sanitizes user input to prevent basic injection attacks."""
    return re.sub(r"[<>\"';]", "", text)
