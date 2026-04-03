import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
from pathlib import Path

API_URL = "https://automated-invoice-processing-and-verification-sy-production.up.railway.app"

# GST verification file
GST_FILE = Path("output/structured_data/gst_verification.json")

st.set_page_config(
    page_title="AI Invoice Automation",
    layout="wide"
)

# =====================================================
# CUSTOM STYLING
# =====================================================

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #0f3b46 0%, #050816 35%, #02040a 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #0b1220;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.2rem;
    }

    .glass-card {
        background: rgba(8, 15, 28, 0.85);
        border: 1px solid rgba(0, 255, 255, 0.18);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 0 18px rgba(0,255,255,0.08);
        margin-bottom: 18px;
    }

    .metric-card {
        background: rgba(6, 12, 24, 0.88);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 0 12px rgba(0,255,255,0.06);
    }

    .metric-title {
        font-size: 0.95rem;
        color: #b8c1d1;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }

    .metric-sub {
        font-size: 0.95rem;
        color: #31d67b;
        font-weight: 600;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }

    .small-label {
        color: #aab3c5;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }

    .value-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        color: white;
    }

    .approved-box {
        background: linear-gradient(90deg, #108d4f, #17a95c);
        border-radius: 12px;
        padding: 14px;
        color: white;
        font-weight: 700;
        text-align: left;
        font-size: 1.5rem;
    }

    .pending-box {
        background: linear-gradient(90deg, #9a6b00, #c98a00);
        border-radius: 12px;
        padding: 14px;
        color: white;
        font-weight: 700;
        font-size: 1.3rem;
    }

    .error-box {
        background: linear-gradient(90deg, #a11d1d, #d92c2c);
        border-radius: 12px;
        padding: 14px;
        color: white;
        font-weight: 700;
        font-size: 1.3rem;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(8, 15, 28, 0.8);
        border: 1px solid rgba(0,255,255,0.18);
        border-radius: 14px;
        padding: 10px;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(8, 15, 28, 0.85);
        border-radius: 12px;
        padding: 6px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #00c2ff, #00e6c3);
        color: #001018;
        font-weight: 700;
        border: none;
        padding: 0.7rem 1rem;
    }

    .stButton > button:hover {
        color: #001018;
        border: none;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1rem 0 1rem 0;
    }

    [data-testid="stMetric"] {
        background: rgba(6, 12, 24, 0.88);
        border: 1px solid rgba(255,255,255,0.12);
        padding: 12px;
        border-radius: 14px;
    }

    label, .stMarkdown, .stText, p, div {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown('<div class="main-title">🧾 AI Invoice Automation Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# =====================================================
# FETCH INVOICES FOR TOP METRICS
# =====================================================

dashboard_df = pd.DataFrame()

try:
    top_response = requests.get(f"{API_URL}/invoices")
    if top_response.status_code == 200:
        top_data = top_response.json()
        if len(top_data) > 0:
            dashboard_df = pd.DataFrame(top_data)
            if "total_amount" in dashboard_df.columns:
                dashboard_df["total_amount"] = pd.to_numeric(
                    dashboard_df["total_amount"], errors="coerce"
                ).fillna(0)
except Exception:
    pass

total_invoices_top = len(dashboard_df) if not dashboard_df.empty else 0
total_spend_top = dashboard_df["total_amount"].sum() if not dashboard_df.empty else 0
avg_processing_time = "7 sec"   # UI only, logic untouched

top1, top2, top3 = st.columns(3)

with top1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Invoices</div>
        <div class="metric-value">{total_invoices_top}</div>
        <div class="metric-sub">▲ Live Count</div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Spend</div>
        <div class="metric-value">₹ {total_spend_top:,.2f}</div>
        <div style="color:#ff6b6b;font-weight:600;">▼ Financial Overview</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Processing Time</div>
        <div class="metric-value">{avg_processing_time}</div>
        <div style="color:#ff6b6b;font-weight:600;">- Performance</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# =====================================================
# UPLOAD + LATEST PROCESSING SECTION
# =====================================================

left_col, right_col = st.columns([1.1, 1.2])

with left_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Upload Invoice</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Invoice (PDF / Image)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    process_clicked = st.button("Process Invoice")

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Latest Invoice Processing</div>', unsafe_allow_html=True)
    latest_invoice_container = st.container()
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PROCESS INVOICE LOGIC
# =====================================================

latest_invoice = None
result = None
gst_data = None

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    if process_clicked:
        with st.spinner("Processing invoice..."):
            response = requests.post(f"{API_URL}/process-invoice", files=files)

        if response.status_code == 200:
            result = response.json()
            st.success("Invoice processed successfully")

            invoice_response = requests.get(f"{API_URL}/invoices")

            if invoice_response.status_code == 200:
                invoices = invoice_response.json()
                if len(invoices) > 0:
                    latest_invoice = invoices[-1]

            try:
                if GST_FILE.exists():
                    gst_data = json.loads(GST_FILE.read_text())
            except Exception:
                gst_data = None

        else:
            st.error("Invoice processing failed")

# =====================================================
# SHOW LATEST INVOICE PROCESSING PANEL
# =====================================================

with latest_invoice_container:
    if latest_invoice:
        a, b = st.columns([2, 1])

        with a:
            st.markdown('<div class="small-label">Vendor Name</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box">{latest_invoice.get("vendor_name", "-")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="small-label">GSTIN</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box">{latest_invoice.get("gstin", "-")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="small-label">Date</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box">{latest_invoice.get("invoice_date", "-")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="small-label">Total</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box">₹ {latest_invoice.get("total_amount", "-")}</div>', unsafe_allow_html=True)

        with b:
            st.markdown('<div class="small-label">Uploaded File</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="value-box" style="height: 220px; display:flex; align-items:center; justify-content:center; text-align:center;">{uploaded_file.name if uploaded_file else "PDF Preview"}</div>', unsafe_allow_html=True)

# =====================================================
# STATUS + GST SECTION
# =====================================================

if result:
    left_status, right_status = st.columns([1.1, 1])

    with left_status:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Verification Status</div>', unsafe_allow_html=True)

        status = result.get("status")
        reasons = result.get("reasons", [])

        if status == "APPROVED":
            st.markdown('<div class="approved-box">STATUS<br>APPROVED</div>', unsafe_allow_html=True)
        elif status == "PENDING":
            st.markdown('<div class="pending-box">STATUS<br>PENDING</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">STATUS<br>{status}</div>', unsafe_allow_html=True)

        if reasons:
            st.markdown("### Reasons")
            for r in reasons:
                st.write("•", r)

        st.markdown('</div>', unsafe_allow_html=True)

    with right_status:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">GST Verification</div>', unsafe_allow_html=True)

        if gst_data:
            c1, c2 = st.columns(2)
            c1.metric("Expected GST", f"₹ {gst_data['expected_gst']}")
            c2.metric("Invoice GST", f"₹ {gst_data['invoice_gst']}")

            if gst_data["gst_status"] == "VALID":
                st.success("GST Status: VALID")
            else:
                st.error("GST Status: MISMATCH")

            gst_chart = px.bar(
                x=["Expected GST", "Invoice GST"],
                y=[gst_data["expected_gst"], gst_data["invoice_gst"]],
                title="GST Verification Comparison",
                color=["Expected GST", "Invoice GST"],
                template="plotly_dark"
            )
            gst_chart.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(gst_chart, use_container_width=True)
        else:
            st.warning("GST verification file not found")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# ANALYTICS SECTION
# =====================================================

st.markdown('<div class="section-title">Invoice Analytics</div>', unsafe_allow_html=True)

try:
    response = requests.get(f"{API_URL}/invoices")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)

            # Convert amount column to numeric
            df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

            analytics_left, analytics_right = st.columns([1.1, 1])

            # ============================================
            # VENDOR SPENDING CHART
            # ============================================
            with analytics_left:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Vendor Spending Trends</div>', unsafe_allow_html=True)

                if "vendor_name" in df.columns and "invoice_date" in df.columns:
                    temp_df = df.copy()
                    temp_df["invoice_date"] = pd.to_datetime(temp_df["invoice_date"], errors="coerce")
                    temp_df["month"] = temp_df["invoice_date"].dt.strftime("%b")

                    vendor_monthly = (
                        temp_df.groupby(["month", "vendor_name"])["total_amount"]
                        .sum()
                        .reset_index()
                    )

                    if not vendor_monthly.empty:
                        chart = px.bar(
                            vendor_monthly,
                            x="month",
                            y="total_amount",
                            color="vendor_name",
                            barmode="group",
                            title="",
                            template="plotly_dark"
                        )
                    else:
                        vendor_spend = df.groupby("vendor_name")["total_amount"].sum().reset_index()
                        chart = px.bar(
                            vendor_spend,
                            x="vendor_name",
                            y="total_amount",
                            color="vendor_name",
                            title="",
                            template="plotly_dark"
                        )
                else:
                    vendor_spend = df.groupby("vendor_name")["total_amount"].sum().reset_index()
                    chart = px.bar(
                        vendor_spend,
                        x="vendor_name",
                        y="total_amount",
                        color="vendor_name",
                        title="",
                        template="plotly_dark"
                    )

                chart.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    xaxis_title="Months / Vendors",
                    yaxis_title="Spend"
                )
                st.plotly_chart(chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ============================================
            # RECENT INVOICES TABLE
            # ============================================
            with analytics_right:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Recent Invoices</div>', unsafe_allow_html=True)

                display_df = df.copy()

                wanted_cols = []
                for col in ["invoice_id", "invoice_date", "vendor_name", "total_amount", "status"]:
                    if col in display_df.columns:
                        wanted_cols.append(col)

                if wanted_cols:
                    display_df = display_df[wanted_cols]

                st.dataframe(
                    display_df.tail(10),
                    use_container_width=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("No invoices found")

    else:
        st.error("API connection failed")

except Exception:
    st.error("Could not connect to FastAPI server. Make sure backend is running.")











