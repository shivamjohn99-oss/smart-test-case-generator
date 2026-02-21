from generator import generate
from export_excel import export_to_excel
from playwright_converter import convert_to_playwright

if __name__ == "__main__":
    story = input("Enter user story: ")
    cases = generate(story)

    print("\nGenerated Cases:\n")
    for case in cases:
        print(case["id"], "-", case["title"])

    export_to_excel(cases)
    convert_to_playwright(cases)