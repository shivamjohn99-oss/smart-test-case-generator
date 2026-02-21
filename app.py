import streamlit as st
from generator import generate
from export_excel import export_to_excel
from playwright_converter import convert_to_playwright

st.set_page_config(page_title="Smart Test Case Generator", layout="wide")

st.title("🚀 Smart Test Case Generator")

story = st.text_area("Enter User Story")

if st.button("Generate Test Cases"):
    cases = generate(story)

    if not cases:
        st.warning("No matching module found. Try login or signup.")
    else:
        st.success(f"{len(cases)} Test Cases Generated!")

        for case in cases:
            with st.expander(f"{case['id']} - {case['title']}"):
                st.write("**Risk Level:**", case["risk"])
                st.write("**Severity:**", case["severity"])
                st.write("**Priority:**", case["priority"])

                st.write("**Preconditions:**", case["preconditions"])
                st.write("**Steps:**")
                st.code(case["steps"])
                st.write("**Expected Result:**", case["expected"])

        # Export options
        export_to_excel(cases)
        convert_to_playwright(cases)

        st.info("Excel & Playwright files generated in project folder.")