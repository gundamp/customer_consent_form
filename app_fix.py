import streamlit as st
import pandas as pd
from datetime import datetime, date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets config ---------------------------------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Streamlit secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    dict(st.secrets["gcp_service_account"]),
    scope
)

def connect_to_gsheet(creds, spreadsheet_name, sheet_name):
    client = gspread.authorize(creds)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)

# Set Google Sheet info
SPREADSHEET_NAME = 'customer_consent_form_little_art_tattoo'
SHEET_NAME = 'collate'
sheet_by_name = connect_to_gsheet(creds, SPREADSHEET_NAME, sheet_name=SHEET_NAME)

# --- Page Config ------------------------------------------------------------
st.set_page_config(page_title="Tattoo & Piercing - Customer Consent & Release Form", page_icon="🖊️")
st.title("🖊️ Tattoo & Piercing - Customer Consent & Release Form")

# --- DOB and Age Validation -------------------------------------------------
dob = st.date_input(
    "Date of Birth",
    value=datetime.today(),
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    key="dob"
)

service = st.selectbox("Select a Service", ["Tattoo", "Piercing"], key="service")

# Calculate Age
today = date.today()
age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
st.markdown(f"**Age (last birthday):** {age}")

underage_tattoo = service == "Tattoo" and age < 18
underage_other = service != "Tattoo" and age < 16

if underage_tattoo:
    st.warning("⚠️ You must be at least 18 years old for this service.")
elif underage_other:
    st.warning("⚠️ You must be at least 16 years old for this service.")

# --- Consent Text -----------------------------------------------------------
st.markdown("""
I hereby give consent to the Artist named in this form of Little Art Tattoo & Piercing studio to perform a tattoo...

I HAVE RECEIVED A COPY OF THE WRITTEN TATTOO AFTERCARE INSTRUCTIONS which I have read and fully understood and hereby assume full responsibility for aftercare and cleanliness. I understand that by having this tattoo performed that I am making a permanent change to my body and no claims have been made regarding the ability to undo the changes made.            
""")

# --- Form Section -----------------------------------------------------------
with st.form("consent_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    suburb = st.text_input("Suburb")
    phone = st.text_input("Phone Number")
    id_type = st.selectbox("ID Type", ["Driver's License", "Passport", "Other"])
    id_number = st.text_input("ID Number")
    id_expiry_date = st.date_input("ID Expiry Date", datetime.today())
    price = st.number_input("Price", min_value=0, format="%d", step=1)

    st.markdown("""
    <u><strong>PLEASE ANSWER THE FOLLOWING QUESTIONS</strong></u><br>
    <i>Answering "Yes" does not necessarily preclude the person from receiving a tattoo.</i>
    """, unsafe_allow_html=True)

    q_eat = st.radio("Have you eaten within the last four (4) hours?", ["Yes", "No"])
    q_alcohol = st.radio("Have you had any alcoholic beverages in the last eight (8) hours?", ["Yes", "No"])
    q_med = st.radio("Have you taken aspirin, ibuprofen or blood thinners in the last twenty four (24) hours?", ["Yes", "No"])
    q_bleed = st.radio("Are you prone to heavy bleeding?", ["Yes", "No"])
    q_faint = st.radio("Are you prone to fainting?", ["Yes", "No"])
    q_breastfeed = st.radio("Are you pregnant or breastfeeding?", ["Yes", "No"])
    q_bloodpressure = st.radio("Do you have high blood pressure?", ["Yes", "No"])
    q_latex = st.radio("Do you have a latex allergy?", ["Yes", "No"])
    q_allergy = st.radio("Do you have any other known allergies?", ["Yes", "No"])
    allergy_details = st.text_input("If yes, please advise:", key="allergy_details") if q_allergy == "Yes" else ""

    q_other = st.radio("Do you have any other conditions which might affect the healing of this tattoo?", ["Yes", "No"])
    other_details = st.text_input("If yes, please advise:", key="other_details") if q_other == "Yes" else ""

    st.markdown("""
    I confirm that all information given is correct. I understand that this is a release form and I agree to be legally bound by it.  
    I confirm that I'm 18 years of age or older.
    """)

    date_of_consent = st.date_input("Date of Consent", datetime.today())
    signature = st.text_area("Signature (please print your name)")

    disabled = underage_tattoo or underage_other
    submitted = st.form_submit_button("Submit", disabled=disabled)

# --- Submission Handling -----------------------------------------------------
if submitted:
    if not full_name or not email or not phone or not suburb or not id_number or not signature:
        st.error("❌ Please complete all required fields.")
    else:
        row = [
            datetime.now().isoformat(),
            full_name,
            dob.isoformat(),
            age,
            email,
            suburb,
            phone,
            id_type,
            id_number,
            id_expiry_date.isoformat(),
            service,
            price,
            q_eat,
            q_alcohol,
            q_med,
            q_bleed,
            q_faint,
            q_breastfeed,
            q_bloodpressure,
            q_latex,
            q_allergy,
            allergy_details,
            q_other,
            other_details,
            date_of_consent.isoformat(),
            signature
        ]
        sheet_by_name.append_row(row)
        st.success("✅ Thank you! Your response has been recorded.")

# --- Footer ------------------------------------------------------------------
st.markdown("---")
# st.caption("Built with ❤️ using Streamlit")
