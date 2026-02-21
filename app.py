import streamlit as st
from generator import generate
from export_excel import export_to_excel
from playwright_converter import convert_to_playwright

st.set_page_config(
    page_title="Smart Test Case Generator",
    layout="wide",
    page_icon="🧠"
)

st.title("🧠 Enterprise Smart Test Case Generator")
st.caption("Hybrid Rule-Based QA Intelligence Engine")

st.divider()

story = st.text_area(
    "📌 Enter Project Description or User Story",
    height=150,
    placeholder="Example: E-commerce app with login, payment gateway, admin dashboard and REST APIs..."
)

generate_btn = st.button("🚀 Generate Test Cases", use_container_width=True)

if generate_btn:

    if not story.strip():
        st.warning("Please enter a valid project description.")
    else:
        cases = generate(story)

        st.success(f"✅ {len(cases)} Test Cases Generated")

        # Summary Dashboard
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cases", len(cases))

        high_risk = len([c for c in cases if c["risk"] == "High"])
        col2.metric("High Risk Cases", high_risk)

        p1_cases = len([c for c in cases if c["priority"] == "P1"])
        col3.metric("Priority P1", p1_cases)

        st.divider()

        # Display Cases
        for case in cases:
            risk_color = "🔴" if case["risk"] == "High" else "🟠" if case["risk"] == "Medium" else "🟢"

            with st.expander(f"{risk_color} {case['id']} - {case['title']}"):
                st.markdown(f"**Risk:** {case['risk']}")
                st.markdown(f"**Severity:** {case['severity']}")
                st.markdown(f"**Priority:** {case['priority']}")

                st.markdown("**Preconditions:**")
                st.write(case["preconditions"])

                st.markdown("**Steps:**")
                st.code(case["steps"])

                st.markdown("**Expected Result:**")
                st.write(case["expected"])

        st.divider()

        # Download Section
        colA, colB = st.columns(2)

        if colA.button("📥 Export to Excel"):
            export_to_excel(cases)
            st.success("Excel file generated.")

        if colB.button("⚙ Generate Playwright File"):
            convert_to_playwright(cases)
            st.success("Playwright file generated.")