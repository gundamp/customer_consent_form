
# 1. Update SPREADSHEET_NAME and SHEET_NAME in this script
# 2. Update Google Sheets ID in Streamlit secrets on Streamlit cloud
## streamlit-sheets-writer@trusty-axe-457305-g0.iam.gserviceaccount.com



import streamlit as st
import pandas as pd
from datetime import datetime, date
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
import os

#from streamlit_js_eval import streamlit_js_eval, get_geolocation

# Capture client IP & more
#info = streamlit_js_eval(js_expressions="window.navigator.userAgent", key="info")
#if info:
#    st.write("Client Info:", info)

#geo = get_geolocation()
#if geo:
#    st.write("IP-based Location:", geo)


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
SPREADSHEET_NAME = 'tattoo_removal_consent_form'
SHEET_NAME = 'form_capture'
sheet_by_name = connect_to_gsheet(creds, SPREADSHEET_NAME, sheet_name = SHEET_NAME)
#SHEET_NAME_backup = 'backup'
#sheet_by_name = connect_to_gsheet(creds, SPREADSHEET_NAME, sheet_name = SHEET_NAME)
#sheet_backup = connect_to_gsheet(creds, SPREADSHEET_NAME, sheet_name = SHEET_NAME_backup)


# --- For image uploads -----------------------------------------------------
#folder_id = st.secrets["drive_folder_id"]

#gauth = GoogleAuth()
#gauth.credentials = creds
#drive = GoogleDrive(gauth)






# --- Page Config ------------------------------------------------------------
st.set_page_config(page_title = "Tattoo Removal Consent Form", page_icon="📝")
st.title("📝 Tattoo Removal Consent Form")

with st.form("consent_form", clear_on_submit = False):

    st.markdown("Patient Information")

    
    st.markdown(
    f"<span style='color:red'><strong>Please use the calendar to select your Date of Birth - You don't need to manually key it in =]]</strong></span>",
    unsafe_allow_html=True
)

# --- DOB and Age Validation -------------------------------------------------
    dob = st.date_input(
        "Date of Birth",
        #value=datetime.today(),
        value = date(2000, 1, 1),
        min_value = date(1900, 1, 1),
        max_value = date.today(),
        key = "dob"
                        )

    st.markdown(
    f"<span style='color:red'><strong>The Date of Birth you've put in is {dob.strftime('%B %d, %Y')}</strong></span>",
    unsafe_allow_html=True
)


# Calculate Age
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.markdown(f"**Age (last birthday):** {age}")

    

# Name
    full_name = st.text_input("Full Name")

# Email
    email = st.text_input("Email Address")

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if email and not re.fullmatch(email_pattern, email):
        st.error("Please enter a valid email address.")

# Suburb (in place of address)
    suburb = st.text_input("Suburb")

# Phone Number
    phone = st.text_input("Phone Number")

    if phone and not re.fullmatch(r"0\d{9}", phone):
        st.error("Phone number must be exactly 10 digits and start with 0.")




    st.markdown("Tattoo Information")

# Location
    tattoo_location = st.text_input("Location of Tattoo")

# Size
    tattoo_size = st.text_input("Size")

# Colours
    tattoo_colours = st.text_input("Colour(s)")

# Age
    tattoo_age = st.text_input("How old is the tattoo?")

#Questionnaires
    q_allergies = st.radio("Do you have any known allergies?", ["Yes", "No"])
    allergies_details = st.text_input("If yes, please list:", key = "allergies_details") if q_allergies == "Yes" else ""

    q_medications = st.radio("Are you currently taking any medications?", ["Yes", "No"])
    medications_details = st.text_input("If yes, please list:", key = "medications_details") if q_medications == "Yes" else ""

    q_conditions = st.radio("Do you have any chronic illnesses or skin conditions?", ["Yes", "No"])
    conditions_details = st.text_input("If yes, please list / explain:", key = "conditions_details") if q_conditions == "Yes" else ""

 # Date   
    date_of_consent = st.date_input("Date of Consent", datetime.today())

# --- Consent Text -----------------------------------------------------------


    st.markdown("""
    ## **Procedure Overview**

    I, the undersigned, consent to undergo tattoo removal. I have been informed about the details of the procedure, including:
    * The process of laser tattoo removal, which involves using lasers to break down ink particles in the skin.
    * The potential need for multiple sessions.
    * The possibility of incomplete removal, scarring, or changes in skin texture or pigmentation.
    """)

    st.markdown("""
    ## **Potential Risks and Complications**

    I understand the risks associated with tattoo removal, which may include but are not limited to:
    * Pain, discomfort, and burning sensation during and after the procedure.
    * Temporary redness, swelling, and blistering.
    * Permanent scarring or changes in skin colour.
    * Infection if post-procedure care instructions are not followed properly.
    """)

    st.markdown("""
    ## **Pre-Procedure Instructions**

    I have been advised to:
    * Avoid sun exposure before the treatment.
    * Avoid taking blood-thinning medications before the procedure unless prescribed by a doctor.
    * Disclose any medical conditions, including skin conditions, that may affect the outcome of the procedure.
    """)

    st.markdown("""
    ## **Post-Procedure Care**

    I have been informed about the post-procedure care, which includes:
    * Keeping the treated area clean and dry.
    * Avoiding sun exposure on the treated area.
    * Applying ointment as directed.
    * Following up with the clinic as necessary.
    """)

    st.markdown("""
    ## **Acknowledgement**

    I acknowledge that:
    * I have been given the opportunity to ask questions about the procedure.
    * I understand that individual results may vary.
    * I consent to the tattoo removal procedure and accept the potential risks involved.
    * I have received and understand the pre- and post-procedure care instructions.
    """)

    st.markdown("""
    ## **Consent**

    I, the undersigned, acknowledge that I have read and fully understand the information provided in this consent form. I give my informed consent for the tattoo removal procedure.
    """)

    signature = st.text_area("Signature (please print your name)")

    artist = st.text_input("Artist")

    price = st.number_input("Price (as agreed with Artist)", min_value = 0, format = "%d", step = 1)

    source = st.selectbox("How did you hear about us =]", ["Instagram", "Google", "Red Note / 小红书", "Website", "Friends / Word of Mouth",  "Other"], key = "source")



    submitted = st.form_submit_button("Submit")

# --- Submission Handling -----------------------------------------------------
phone_valid = re.fullmatch(r"0\d{9}", phone)
email_valid = re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

if submitted:
    if not full_name or not email or not suburb or not phone or not signature:
        st.error("❌ Please complete all required fields.")

    elif not phone_valid:
        st.error("❌ Phone number must be exactly 10 digits and start with 0.")
    
    elif not email_valid:
        st.error("❌ Please enter a valid email address.")

    elif price is None:
            st.error("Please enter the price.")
        
    else:
        row = [
            date_of_consent.isoformat(),
            artist,
            #service,
            price,
            #description,
            #placement,
            suburb,
            source,
            full_name,
            dob.isoformat(),
            age,
            phone,
            email,
            tattoo_location,
            tattoo_size,
            tattoo_colours,
            tattoo_age,
            q_allergies,
            allergies_details,
            q_medications,
            medications_details,
            q_conditions,
            conditions_details,

            signature
        
        ]

       

# Compute the next empty row index
        next_row = len(sheet_by_name.get_all_values()) + 1
        cell_range = f"A{next_row}"
        sheet_by_name.update(cell_range, [row])

        #next_row_backup = len(sheet_backup.get_all_values()) + 1
        #cell_range_backup = f"A{next_row_backup}"
        #sheet_backup.update(cell_range_backup, [row])

    #sheet_by_name.append_row(row)
        st.success("✅ Thank you! Your response has been recorded.")

# --- Footer ------------------------------------------------------------------
st.markdown("---")


