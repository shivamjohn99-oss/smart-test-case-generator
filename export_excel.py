from openpyxl import Workbook


def export_to_excel(cases, filename="test_cases.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    ws.append(["ID", "Title", "Preconditions", "Steps", "Expected Result"])

    for case in cases:
        ws.append([
            case["id"],
            case["title"],
            case["preconditions"],
            case["steps"],
            case["expected"]
        ])

    wb.save(filename)
    print(f"Excel file saved as {filename}")