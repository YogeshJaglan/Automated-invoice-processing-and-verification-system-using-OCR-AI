import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Invoice Automation",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("🧾 AI Invoice Automation Dashboard")

st.markdown("---")

# =====================================================
# UPLOAD SECTION
# =====================================================

st.header("Upload Invoice")

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF / Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    if st.button("Process Invoice"):

        with st.spinner("Processing invoice..."):

            response = requests.post(f"{API_URL}/process-invoice", files=files)

        if response.status_code == 200:

            result = response.json()

            st.success("Invoice processed successfully")

            st.write("Invoice ID:", result.get("invoice_id"))

            # ============================================
            # GET LATEST INVOICE FROM DATABASE
            # ============================================

            invoice_response = requests.get(f"{API_URL}/invoices")

            if invoice_response.status_code == 200:

                invoices = invoice_response.json()

                if len(invoices) > 0:

                    latest_invoice = invoices[-1]

                    st.subheader("Extracted Invoice Data")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("Vendor Name:", latest_invoice.get("vendor_name"))
                        st.write("GSTIN:", latest_invoice.get("gstin"))
                        st.write("Invoice Number:", latest_invoice.get("invoice_number"))

                    with col2:
                        st.write("Invoice Date:", latest_invoice.get("invoice_date"))
                        st.write("Total Amount: ₹", latest_invoice.get("total_amount"))

            # ============================================
            # VERIFICATION RESULT
            # ============================================

            st.subheader("Verification Result")

            status = result.get("status")
            reasons = result.get("reasons", [])

            if status == "APPROVED":
                st.success(f"Status: {status}")
            else:
                st.error(f"Status: {status}")

            if reasons:
                st.write("Reasons:")
                for r in reasons:
                    st.write("•", r)

        else:
            st.error("Invoice processing failed")


st.markdown("---")

# =====================================================
# ANALYTICS SECTION
# =====================================================

st.header("Invoice Analytics")

try:

    response = requests.get(f"{API_URL}/invoices")

    if response.status_code == 200:

        data = response.json()

        if len(data) > 0:

            df = pd.DataFrame(data)

            # Convert amount column to numeric
            df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

            total_invoices = len(df)
            total_spend = df["total_amount"].sum()
            total_vendors = df["vendor_name"].nunique()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Invoices", total_invoices)
            col2.metric("Total Vendors", total_vendors)
            col3.metric("Total Spend", f"₹ {total_spend:,.2f}")

            st.markdown("---")

            # ============================================
            # VENDOR SPENDING CHART
            # ============================================

            vendor_spend = df.groupby("vendor_name")["total_amount"].sum().reset_index()

            chart = px.bar(
                vendor_spend,
                x="vendor_name",
                y="total_amount",
                title="Vendor Spending",
                text="total_amount"
            )

            st.plotly_chart(chart, use_container_width=True)

            st.markdown("---")

            # ============================================
            # INVOICE TABLE
            # ============================================

            st.subheader("Invoice Records")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:
            st.warning("No invoices found")

    else:
        st.error("API connection failed")

except Exception:
    st.error("Could not connect to FastAPI server. Make sure backend is running.")








