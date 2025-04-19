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
sheet_by_name = connect_to_gsheet(creds, SPREADSHEET_NAME, sheet_name = SHEET_NAME)

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

service = st.selectbox("Select a Service", ["Tattoo", "Piercing"], key = "service")

if service == "Tattoo":
    artist = st.selectbox("Artist", ["Raku", "Kobey", "Violet", "Emily", "Jusqu", "Bonnie", "Phoebe"], key = "artist")
else:
    artist = "Piercing"

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
I hereby give consent to the Artist named in this form of the Tattoo & Piercing studio to perform a tattoo and in consideration of doing so, I hereby release the tattoo studio, and its employees and agents from all manner of liabilities, claims, actions and demands in law or in equity, which I or my heirs might now or hereafter have by reason of complying with my request to be tattooed.

I fully understand that any employee or agent of this Tattoo & Piercing Studio when performing a tattoo does not act in the capacity of a medical professional. The suggestions made by any employee or agent of this studio are just suggestions. They are not to be construed as, or substituted for, advice from a medical professional.

I UNDERSTAND THAT I WILL BE TATTOOED USING appropriate techniques, instruments and pigments. To ensure proper healing of my tattoo, I agree to follow the written and verbal Tattoo Aftercare instructions that will be provided until healing is complete. I understand that a tattoo may take two weeks or more to heal.

I WILLINGLY SUBMIT TO THESE PROCEDURES with a full understanding of possible complications such as but not limited to infection, allergic reason or rejection of the ink.
            Neither the Artist named in this form nor this Tattoo & Piercing studio is responsible for the meaning or spelling of the symbol that I have provided to them or chosen from the flash design sheets.           

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
    id_expiry_date = st.date_input("ID Expiry Date", datetime.today(), min_value = date.today(), max_value=date(2049,12,31))
    #artist = st.selectbox("Artist", ["Artist 1", "Artist 2", "Artist 3"])
    placement = st.text_input("Placement (扎针部位)")
    description = st.text_input("Description (扎针内容)")
    price = st.number_input("Price (as agreed with Artist)", min_value = 0, format = "%d", step = 1)

    st.markdown("""
    <u><strong>PLEASE ANSWER THE FOLLOWING QUESTIONS</strong></u><br>
    <i>ANSWERING "YES" TO ANY OF THESE QUESTIONS DOES NOT NECESSARILY PRECLUDE THE PERSON FROM RECEIVING A TATTOO:</i>
                
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
                I acknowledge that the sterilisation method used was explained to my full satisfaction. I had the opportunity to ask questions
                regarding this procedure. All questions were answered to my satisfaction. All equipments during the procedure was opened in front of me.
                I witnessed the disposal of the tattoo needle(s) into regulated sharps container. Both written and verbal Tattoo Aftercare Instructions
                were provided to me. I have read this Tattoo and Piercing Consent and Release Form and confirm that all the information I have given is correct.
                I understand that this is a release form and I agree to be legally bound by it.

            
                
                """)

    date_of_consent = st.date_input("Date of Consent", datetime.today())
    signature = st.text_area("Signature (please print your name)")

    disabled = underage_tattoo or underage_other
    submitted = st.form_submit_button("Submit", disabled=disabled)

# --- Submission Handling -----------------------------------------------------
if submitted:
    if not full_name or not email or not suburb or not phone or not id_type or not id_number or not id_expiry_date or not placement or not description or not price or not signature:
        st.error("❌ Please complete all required fields.")
    else:
        row = [
            #datetime.now().isoformat(),
            full_name,
            service,
            dob.isoformat(),
            artist,
            age,
            email,
            suburb,
            phone,
            id_type,
            id_number,
            id_expiry_date.isoformat(),
            placement,
            description,
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

       

# Compute the next empty row index
        next_row = len(sheet_by_name.get_all_values()) + 1
        cell_range = f"A{next_row}"
        sheet_by_name.update(cell_range, [row])

    #sheet_by_name.append_row(row)
        st.success("✅ Thank you! Your response has been recorded.")

# --- Footer ------------------------------------------------------------------
st.markdown("---")
# st.caption("Built with ❤️ using Streamlit")
