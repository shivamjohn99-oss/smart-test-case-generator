def convert_to_playwright(cases, filename="test_playwright.py"):

    with open(filename, "w") as f:
        f.write("import pytest\n\n")

        for case in cases:
            test_name = case["title"].replace(" ", "_").lower()

            f.write(f"""
def test_{test_name}(page):
    # Preconditions: {case['preconditions']}
    # Steps:
    # {case['steps'].replace(chr(10), '\\n    # ')}
    
    # TODO: Implement Playwright steps here
    
    assert True  # Replace with actual validation
""")

    print(f"Playwright skeleton saved as {filename}")