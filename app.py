import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="HR Employee Master → Excel", layout="wide")

# ---------- Store / Company dropdown options ----------
STORE_OPTIONS = [
    "4955 USA LLC","A&K Global USA LLC","Aaliya USA LLC","Arshi & Khushi LLC","Ask Global USA LLC",
    "BH1 USA LLC","CAD1 USA LLC","CDP USA LLC","CDP1 USA LLC","CH1 USA LLC","EM1 USA LLC",
    "Fairview Tobacco Store LLC","Forest Park Mart LLC","FR1 USA LLC","FR2155 USA LLC","HR1 USA LLC",
    "JBR2 USA LLC","JFH3 USA LLC","JFH4 USA LLC","Kushi Ali Inc","M1L1K USA LLC","MAM1 USA LLC",
    "MH1 USA LLC","MVB1 USA LLC","NE41 USA LLC","Newnan Gas & Food LLC","Nextday Wholesale LLC",
    "ODH1","RX1 USA LLC","SGC Gas Mart LLC","SS1 USA LLC","SSM2 USA LLC","TR1 USA LLC","TS1 USA LLC",
    "TWP1 USA LLC","WC1 USA LLC","NextDay Wholesale LLC","YVS Partners LLC","Skyzone",
]

# ---------- Store ID dropdown options ----------
STORE_ID_OPTIONS = [
    "4955","AKG","AAL","ANK1","ASK","BH1","CAD1","CDP","CDP1","CH1","EM1","FTS","FPM1","FR1","FR2",
    "HR1","JBR2","JFH3","JFH4","KAI","MLK1","MAM1","MH1","MVB1","NE41","NNG1","NDWS","ODH1","RX1",
    "SGC","SS1","SSM2","TR1","TS1","TWP1","WC1"
]

# ---------- Controlled dropdowns ----------
EMPLOYMENT_STATUS_OPTIONS = ["F1","F2","Citizen","Greencard","Asylum","H1B","B1/B2","H4"]
GENDER_OPTIONS = ["Male","Female","Prefer not to say"]
MARITAL_STATUS_OPTIONS = ["Single","Married","Prefer not to say"]
PAY_BASIS_OPTIONS = ["Hourly","Salary","Mixed"]           # drives required pay fields
PAYMENT_TYPE_OPTIONS = ["Cash","Check","Cash/Check"]      # method of payment

# ----------------------------
# Schema (SSN REMOVED)
# types: text | number | date | select | multiselect
# ----------------------------
SCHEMA = [
    ("Employee ID", "Unique, non-recycled employee code.", "text", None),
    ("Payroll ID", "Payroll system employee ID.", "text", None),

    ("Store ID", "Select store/site code.", "select", STORE_ID_OPTIONS),
    ("Store/ Company Name", "Select store/company from list.", "select", STORE_OPTIONS),
    ("Store Address", "Full store address (optional).", "text", None),

    ("Full Name", "Employee full name.", "text", None),
    ("Designation", "Job title/designation.", "text", None),
    ("Manager Name", "Direct manager's full name.", "text", None),

    ("Date of Birth", "YYYY-MM-DD.", "date", None),
    ("Gender", "Gender.", "select", GENDER_OPTIONS),
    ("Marital Status", "Marital status.", "select", MARITAL_STATUS_OPTIONS),
    ("Contact Number", "Primary phone.", "text", None),
    ("Email Address", "Work/personal email.", "text", None),

    ("Status", "Active state.", "select", ["Active","On Leave","Terminated"]),
    ("Employment Status", "Work authorization / status.", "select", EMPLOYMENT_STATUS_OPTIONS),
    ("Employment Type", "FT/PT/etc.", "select", ["Full-time","Part-time","Temporary","Intern","Contractor"]),

    ("Pay Basis", "Hourly/Salary/Mixed (controls required pay fields).", "select", PAY_BASIS_OPTIONS),
    ("Payment Type", "Payment method.", "select", PAYMENT_TYPE_OPTIONS),

    ("Hourly Pay Rate", "Hourly $ (if Pay Basis is Hourly or Mixed).", "number", None),
    ("Monthly Salary", "Monthly $ (if Pay Basis is Salary or Mixed).", "number", None),
    ("Weekly Salary", "Weekly $ (if Pay Basis is Salary or Mixed).", "number", None),

    ("Scheduled Hours", "Planned hours per week.", "number", None),
    ("Working Days", "Weekdays worked.", "multiselect", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),

    ("Joining Date", "Employee start date (YYYY-MM-DD).", "date", None),
    ("Leaving Date", "If left, last day (YYYY-MM-DD).", "date", None),
]

FIELDS = [f[0] for f in SCHEMA]

# ----------------------------
# Session state
# ----------------------------
if "rows_raw" not in st.session_state:
    st.session_state.rows_raw = []
if "defaults" not in st.session_state:
    st.session_state.defaults = {}

# ----------------------------
# Header & quick actions
# ----------------------------
st.title("HR Employee Master → Excel")
st.caption("Fill the form → Add row → Download Excel/CSV. Excel includes a Data Dictionary sheet.")

b1, b2, b3, _ = st.columns([1,1,1,3])
with b1:
    if st.button("Load Sample into Form"):
        st.session_state.defaults = {
            "Employee ID": "E1027",
            "Payroll ID": "PR-7788",
            "Store ID": "NDWS",
            "Store/ Company Name": "NextDay Wholesale LLC",
            "Store Address": "123 Peachtree St, Atlanta, GA 30303",
            "Full Name": "Sami Khan",
            "Designation": "Inventory Control & CRM Associate",
            "Manager Name": "Alex Morgan",
            "Date of Birth": "1996-04-15",
            "Gender": "Male",
            "Marital Status": "Single",
            "Contact Number": "404-555-2000",
            "Email Address": "sami.khan@company.com",
            "Status": "Active",
            "Employment Status": "Citizen",
            "Employment Type": "Full-time",
            "Pay Basis": "Hourly",
            "Payment Type": "Cash",
            "Hourly Pay Rate": 22,
            "Monthly Salary": None,
            "Weekly Salary": None,
            "Scheduled Hours": 40,
            "Working Days": ["Mon","Tue","Wed","Thu","Fri","Sat"],
            "Joining Date": "2024-05-15",
            "Leaving Date": ""
        }
        st.rerun()
