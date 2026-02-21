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

# ------------------------------
# UNIVERSAL FEATURE ENGINE
# ------------------------------

FEATURE_MAP = {
    "authentication": ["login", "signup", "register", "reset", "password", "auth"],
    "transaction": ["payment", "checkout", "cart", "fund", "transfer"],
    "search": ["search", "filter", "sort"],
    "upload": ["upload", "file", "attachment"],
    "dashboard": ["dashboard", "admin", "panel"],
    "api": ["api", "endpoint", "rest", "json"],
    "form": ["form", "submit", "input"],
    
}
ROLE_KEYWORDS = ["admin", "role", "permission", "access", "user management"]
def detect_roles(user_story):
    story = user_story.lower()
    return any(word in story for word in ROLE_KEYWORDS)

def detect_features(user_story):
    detected = []
    story = user_story.lower()

    for feature, keywords in FEATURE_MAP.items():
        if any(word in story for word in keywords):
            detected.append(feature)

    return detected


def generate_feature_tests(feature):
    cases = []

    cases.append(format_case(
        f"{feature} - Functional validation",
        "System available",
        f"Perform valid {feature} action",
        "System processes successfully"
    ))

    cases.append(format_case(
        f"{feature} - Negative validation",
        "System available",
        f"Perform invalid {feature} action",
        "System shows proper error"
    ))

    cases.append(format_case(
        f"{feature} - UI validation",
        "User on page",
        "Verify layout, labels, responsiveness",
        "UI should render correctly"
    ))

    cases.append(format_case(
        f"{feature} - Security validation",
        "User access available",
        "Attempt malicious or unauthorized input",
        "System prevents security breach"
    ))

    cases.append(format_case(
        f"{feature} - Performance validation",
        "System operational",
        f"Perform repeated {feature} action under load",
        "System remains stable"
    ))

    return cases
def generate_feature_tests(feature):
    cases = []
    ...
    return cases


# ⬇ ADD IT HERE ⬇

def generate_role_tests():
    cases = []

    cases.append(format_case(
        "Role-based access validation",
        "Multiple user roles exist",
        "Login as Admin and access restricted module",
        "Admin should access successfully"
    ))

    cases.append(format_case(
        "Unauthorized access prevention",
        "User role defined",
        "Login as normal user and access admin module",
        "Access should be denied"
    ))

    cases.append(format_case(
        "UI visibility per role",
        "User roles configured",
        "Login as different roles",
        "Only permitted UI elements should be visible"
    ))

    return cases

# ------------------------------
# MAIN GENERATE FUNCTION
# ------------------------------

def generate(user_story):
    features = detect_features(user_story)
    cases = []

    # Feature-based tests
    for feature in features:
        cases.extend(generate_feature_tests(feature))

    # 🔥 Role detection
    if detect_roles(user_story):
        cases.extend(generate_role_tests())

    # Boundary tests
    cases.extend(generate_boundary_cases(user_story))

    # Fallback
    if not cases:
        cases.append(format_case(
            "Generic Functional Validation",
            "System available",
            "Perform intended operation",
            "System behaves as expected"
        ))

    return cases