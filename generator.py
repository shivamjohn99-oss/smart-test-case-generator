import re
import uuid

# ------------------------------
# Utility
# ------------------------------
def assign_risk(title):
    title = title.lower()

    if any(word in title for word in ["login", "payment", "fund", "transaction"]):
        return "High"
    elif any(word in title for word in ["signup", "reset"]):
        return "Medium"
    else:
        return "Low"
def assign_severity(title):
    title = title.lower()

    if "fail" in title or "invalid" in title:
        return "High"
    elif "boundary" in title:
        return "Medium"
    else:
        return "Low"
def assign_priority(risk):
    if risk == "High":
        return "P1"
    elif risk == "Medium":
        return "P2"
    else:
        return "P3"    
def extract_numbers(user_story):
    numbers = re.findall(r'\d+', user_story)
    return [int(num) for num in numbers]

def generate_boundary_cases(user_story):
    cases = []
    numbers = extract_numbers(user_story)

    for num in numbers:
        cases.append(format_case(
            f"Boundary test for value {num - 1}",
            "System constraint defined",
            f"Enter value {num - 1}",
            "System should validate correctly"
        ))

        cases.append(format_case(
            f"Boundary test for exact value {num}",
            "System constraint defined",
            f"Enter value {num}",
            "System should accept if within limit"
        ))

        cases.append(format_case(
            f"Boundary test for value {num + 1}",
            "System constraint defined",
            f"Enter value {num + 1}",
            "System should reject if exceeding limit"
        ))

    return cases

def generate_test_case_id():
    return f"TC_{str(uuid.uuid4())[:6].upper()}"


def format_case(title, preconditions, steps, expected):
    risk = assign_risk(title)
    severity = assign_severity(title)
    priority = assign_priority(risk)

    return {
        "id": generate_test_case_id(),
        "title": title,
        "preconditions": preconditions,
        "steps": steps,
        "expected": expected,
        "risk": risk,
        "severity": severity,
        "priority": priority
    }
    


# ------------------------------
# MODULES
# ------------------------------

def login_cases():
    return [
        format_case(
            "Login with valid credentials",
            "Registered user exists",
            "Enter valid username\nEnter valid password\nClick Login",
            "User redirected to dashboard"
        ),
        format_case(
            "Login with invalid password",
            "Registered user exists",
            "Enter valid username\nEnter wrong password\nClick Login",
            "Error message displayed"
        ),
        format_case(
            "Login with empty fields",
            "None",
            "Leave username and password empty\nClick Login",
            "Validation error shown"
        ),
    ]


def signup_cases():
    return [
        format_case(
            "Signup with valid details",
            "User on signup page",
            "Enter valid name/email/password\nClick Signup",
            "Account created"
        ),
        format_case(
            "Signup with existing email",
            "Email already exists",
            "Enter existing email\nClick Signup",
            "Duplicate email error"
        ),
    ]


def transaction_cases():
    return [
        format_case(
            "Add funds with valid amount",
            "User logged in",
            "Enter valid amount\nClick Add Funds",
            "Balance updated successfully"
        ),
        format_case(
            "Add funds with negative amount",
            "User logged in",
            "Enter -100\nClick Add Funds",
            "Validation error shown"
        ),
        format_case(
            "Add funds exceeding max limit",
            "Max limit is 50,000",
            "Enter 100000\nClick Add Funds",
            "System should block transaction"
        ),
    ]


def reset_password_cases():
    return [
        format_case(
            "Reset password with valid email",
            "User registered",
            "Enter registered email\nClick Reset",
            "Password reset link sent"
        ),
        format_case(
            "Reset password with invalid email",
            "None",
            "Enter unregistered email\nClick Reset",
            "Error message displayed"
        ),
    ]


# ------------------------------
# DYNAMIC ENGINE
# ------------------------------

keyword_map = {
    "login": login_cases,
    "signin": login_cases,
    "signup": signup_cases,
    "register": signup_cases,
    "add": transaction_cases,
    "fund": transaction_cases,
    "payment": transaction_cases,
    "reset": reset_password_cases,
    "forgot": reset_password_cases,
}


def generate(user_story):
    user_story = user_story.lower()
    cases = []

    triggered_modules = set()

    # Keyword-based modules
    for keyword, function in keyword_map.items():
        if keyword in user_story:
            if function not in triggered_modules:
                cases.extend(function())
                triggered_modules.add(function)

    # 🔥 ADD THIS LINE (Boundary Engine Integration)
    cases.extend(generate_boundary_cases(user_story))

    # Fallback
    if not cases:
        cases.append(format_case(
            "Generic validation",
            "System available",
            "Perform intended action",
            "System behaves as expected"
        ))

    return cases
    if not cases:
        cases.append(format_case(
            "Generic validation",
            "System available",
            "Perform intended action",
            "System behaves as expected"
        ))

    return cases