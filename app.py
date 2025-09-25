import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="HR Employee Master → Excel", layout="wide")

# ---------- Dropdown options ----------
STORE_OPTIONS = [
    "4955 USA LLC","A&K Global USA LLC","Aaliya USA LLC","Arshi & Khushi LLC","Ask Global USA LLC",
    "BH1 USA LLC","CAD1 USA LLC","CDP USA LLC","CDP1 USA LLC","CH1 USA LLC","EM1 USA LLC",
    "Fairview Tobacco Store LLC","Forest Park Mart LLC","FR1 USA LLC","FR2155 USA LLC","HR1 USA LLC",
    "JBR2 USA LLC","JFH3 USA LLC","JFH4 USA LLC","Kushi Ali Inc","M1L1K USA LLC","MAM1 USA LLC",
    "MH1 USA LLC","MVB1 USA LLC","NE41 USA LLC","Newnan Gas & Food LLC","Nextday Wholesale LLC",
    "ODH1","RX1 USA LLC","SGC Gas Mart LLC","SS1 USA LLC","SSM2 USA LLC","TR1 USA LLC","TS1 USA LLC",
    "TWP1 USA LLC","WC1 USA LLC","NextDay Wholesale LLC","YVS Partners LLC","Skyzone",
]

STORE_ID_OPTIONS = [
    "4955","AKG","AAL","ANK1","ASK","BH1","CAD1","CDP","CDP1","CH1","EM1","FTS","FPM1","FR1","FR2",
    "HR1","JBR2","JFH3","JFH4","KAI","MLK1","MAM1","MH1","MVB1","NE41","NNG1","NDWS","ODH1","RX1",
    "SGC","SS1","SSM2","TR1","TS1","TWP1","WC1"
]

EMPLOYMENT_STATUS_OPTIONS = ["F1","F2","Citizen","Greencard","Asylum","H1B","B1/B2","H4"]
GENDER_OPTIONS = ["Male","Female","Prefer not to say"]
MARITAL_STATUS_OPTIONS = ["Single","Married","Prefer not to say"]
PAY_BASIS_OPTIONS = ["Hourly","Salary","Mixed"]
PAYMENT_TYPE_OPTIONS = ["Cash","Check","Cash/Check"]

# ----------------------------
# Schema (SSN REMOVED)
# ----------------------------
SCHEMA = [
    ("Employee ID", "text", None),
    ("Payroll ID", "text", None),
    ("Store ID", "select", STORE_ID_OPTIONS),
    ("Store/ Company Name", "select", STORE_OPTIONS),
    ("Store Address", "text", None),
    ("Full Name", "text", None),
    ("Designation", "text", None),
    ("Manager Name", "text", None),
    ("Date of Birth", "date", None),
    ("Gender", "select", GENDER_OPTIONS),
    ("Marital Status", "select", MARITAL_STATUS_OPTIONS),
    ("Contact Number", "text", None),
    ("Email Address", "text", None),
    ("Status", "select", ["Active","On Leave","Terminated"]),
    ("Employment Status", "select", EMPLOYMENT_STATUS_OPTIONS),
    ("Employment Type", "select", ["Full-time","Part-time","Temporary","Intern","Contractor"]),
    ("Pay Basis", "select", PAY_BASIS_OPTIONS),
    ("Payment Type", "select", PAYMENT_TYPE_OPTIONS),
    ("Hourly Pay Rate", "number", None),
    ("Monthly Salary", "number", None),
    ("Weekly Salary", "number", None),
    ("Scheduled Hours", "number", None),
    ("Working Days", "multiselect", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),
    ("Joining Date", "date", None),
    ("Leaving Date", "date", None),
]

FIELDS = [f[0] for f in SCHEMA]

# ----------------------------
# Session state
# ----------------------------
if "rows_raw" not in st.session_state:
    st.session_state.rows_raw = []

# ----------------------------
# Header
# ----------------------------
st.title("HR Employee Master → Excel")
st.caption("Fill the form → Add row → Download Excel/CSV.")

# ----------------------------
# Form
# ----------------------------
st.subheader("Add Employee")

with st.form("emp_form", clear_on_submit=True):
    cols = st.columns(3)
    values = {}
    for i, (field, ftype, options) in enumerate(SCHEMA):
        with cols[i % 3]:
            if ftype == "select":
                opts = options or []
                values[field] = st.selectbox(field, opts, key=f"f_{field}")
            elif ftype == "multiselect":
                values[field] = st.multiselect(field, options, key=f"f_{field}")
            elif ftype == "date":
                values[field] = st.date_input(field, value=None, key=f"f_{field}")
            elif ftype == "number":
                values[field] = st.number_input(field, value=0.0, step=1.0, format="%.2f", key=f"f_{field}")
            else:
                values[field] = st.text_input(field, "", key=f"f_{field}")

    submitted = st.form_submit_button("Add row")

    if submitted:
        clean = {}
        for field, ftype, _ in SCHEMA:
            v = values[field]
            if ftype == "date" and v:
                v = v.isoformat()
            if ftype == "multiselect":
                v = ", ".join(v)
            clean[field] = v
        st.session_state.rows_raw.append(clean)
        st.success("Row added.")

# ----------------------------
# Preview
# ----------------------------
st.subheader("Staging Table")
df_raw = pd.DataFrame(st.session_state.rows_raw, columns=FIELDS)
st.dataframe(df_raw, use_container_width=True, hide_index=True)
st.write(f"**Rows:** {len(df_raw)}")

# ----------------------------
# Clear Table Button
# ----------------------------
if st.button("Clear All Records"):
    st.session_state.rows_raw = []
    st.success("All records cleared.")

# ----------------------------
# Downloads
# ----------------------------
def make_excel_bytes(master_df: pd.DataFrame) -> bytes:
    dict_df = pd.DataFrame({"Field": [s[0] for s in SCHEMA]})
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="xlsxwriter") as xw:
        master_df.to_excel(xw, sheet_name="Master", index=False)
        dict_df.to_excel(xw, sheet_name="DataDictionary", index=False)
    return bio.getvalue()

st.subheader("Download")
cA, cB = st.columns(2)
with cA:
    st.download_button(
        "Download Excel (.xlsx)",
        data=make_excel_bytes(df_raw),
        file_name="EmployeeMaster.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        disabled=df_raw.empty,
    )
with cB:
    st.download_button(
        "Download CSV",
        data=df_raw.to_csv(index=False).encode("utf-8"),
        file_name="EmployeeMaster.csv",
        mime="text/csv",
        disabled=df_raw.empty,
    )
