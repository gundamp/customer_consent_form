# app.py

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# --- Page config -------------------------------------------------------------
st.set_page_config(page_title="Tattoo & Piercing - Customer Consent & Release Form", page_icon="🖊️")



st.title("🖊️ Tattoo & Piercing - Customer Consent & Release Form")


# --- DOB & Age calculation outside the form -------------------------
dob = st.date_input(
    "Date of Birth",
    value=datetime.today(),
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    key="dob"
)

service  = st.selectbox("Select a Service", ["Tattoo", "Piercing"], key = "service")

# calculate age immediately whenever dob changes
today = date.today()
age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
st.markdown(f"**Age (last birthday):** {age}")

underage_tattoo = service == "Tattoo" and age < 18
underage_other  = service != "Tattoo" and age < 16

    # Show the appropriate warning
if underage_tattoo:
        st.warning("⚠️ You must be at least 18 years old for this service.")
elif underage_other:
        st.warning("⚠️ You must be at least 16 years old for this service.")


st.markdown("""
I hereby give consent to the Artist named in this form of Little Art Tattoo & Piercing studio to perform a tattoo and in consideration of doing so, I hereby release the tattoo studio, and its employees and agents from all manner of liabilities, claims, actions and demands in law or in equity, which I or my heirs might now or hereafter have by reason of complying with my request to be tattooed.

I fully understand that any employee or agent of this Tattoo Studio when performing a tattoo does not act in the capacity of a medical professional. The suggestions made by any employee or agent of this studio are just suggestions. They are not to be construed as, or substituted for, advice from a medical professional.

I UNDERSTAND THAT I WILL BE TATTOOED USING appropriate techniques, instruments and pigments. To ensure proper healing of my tattoo, I agree to follow the written and verbal Tattoo Aftercare instructions that will be provided until healing is complete. I understand that a tattoo may take two weeks or more to heal.

I WILLINGLY SUBMIT TO THESE PROCEDURES with a full understanding of possible complications such as but not limited to infection, allergic reason or rejection of the ink.
            Neither the Artist named in this form nor Little Art Tattoo & Piercing studio is responsible for the meaning or spelling of the symbol that I have provided to them or chosen from the flash design sheets.           

I HAVE RECEIVED A COPY OF THE WRITTEN TATTOO AFTERCARE INSTRUCTIONS which I have read and fully understood and hereby assume full responsibility for aftercare and cleanliness. I understand that by having this tattoo performed that I am making a permanent change to my body and no claims have been made regarding the ability to undo the changes made.            

""")



# --- Build the form ---------------------------------------------------------
with st.form("consent_form"):
    full_name = st.text_input("Full Name")
   #dob       = st.date_input("Date of Birth", datetime.today(), min_value = date(1900, 1, 1), max_value = date.today(), key = "dob")

    #today = date.today()
    #age = (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))
    #st.markdown(f"**Age:** {age}")

    email     = st.text_input("Email Address")
    suburb    = st.text_input("Suburb")
    phone     = st.text_input("Phone Number")
    id_type  = st.selectbox("ID Type", ["Driver's License", "Passport", "Other"])
    id_number = st.text_input("ID Number")
    id_expiry_date = st.date_input("ID Expiry Date", datetime.today())
    ## include a field for service which is either Tattoo or Piercing
    

     # conditional warnings


    ## include a field for Price but make it integer only
    price = st.number_input("Price", min_value = 0, format = "%d", step = 1)

   


    st.markdown("""
    <u><strong>PLEASE ANSWER THE FOLLOWING QUESTIONS</strong></u><br>
    <i>ANSWERING "YES" TO ANY OF THESE QUESTIONS DOES NOT NECESSARILY PRECLUDE THE PERSON FROM RECEIVING A TATTOO:</i>
                
                """, unsafe_allow_html=True)
    

    # Yes/No as mutually exclusive radios

    q_eat     = st.radio("Have you eaten within the last four (4) hours>?", options=["Yes", "No"])
    q_alcohol = st.radio("Have you had any alcoholic beverages in the last eight (8) hours?", options=["Yes", "No"])
    q_med     = st.radio("Have you taken aspirin, ibuprofen or blood thinners in the last twenty four (24) hours?", options=["Yes", "No"])
    q_bleed   = st.radio("Are you prone to heavy bleeding?", options=["Yes", "No"])
    q_faint   = st.radio("Are you prone to fainting?", options=["Yes", "No"])
    q_breastfeed = st.radio("Are you pregnant or breastfeeding?", options=["Yes", "No"])
    q_bloodpressure = st.radio("Do you have high blood pressure?", options=["Yes", "No"])
    q_latex = st.radio("Do you have a latex allergy?", options=["Yes", "No"])
    q_allergy = st.radio("Do you have any other known allergies?", options=["Yes", "No"])

    # only show this line if they answered Yes
    if q_allergy == "Yes":
        allergy_details = st.text_input("If yes, please advise:",  key="allergy_details")
    else:
        allergy_details = ""
    
    q_other = st.radio("Do you have any other conditions which might affect the healing of this tattoo?", options=["Yes", "No"])

        # only show this line if they answered Yes
    if q_other == "Yes":
        other_details = st.text_input("If yes, please advise:", key="other_details")
    else:
        other_details = ""


    st.markdown("""
                I acknowledge that the sterilisation method used was explained to my full satisfaction. I had the opportunity to ask questions
                regarding this procedure. All questions were answered to my satisfaction. All equipments during the procedure was opened in front of me.
                I witnessed the disposal of the tattoo needle(s) into regulated sharps container. Both written and verbal Tattoo Aftercare Instructions
                were provided to me. I have read this Tattoo and Piercing Consent and Release Form and confirm that all the information I have given is correct.
                I understand that this is a release form and I agree to be legally bound by it.

                I confirm that I'm 18 years of age or older.
                
                """)
  
    date_of_consent = st.date_input("Date of Consent", datetime.today())
    signature       = st.text_area("Signature (please print your name)")


    #underage_tattoo = service == "Tattoo" and age < 18
    #underage_other  = service != "Tattoo" and age < 16

    disabled = underage_tattoo or underage_other
  
    submitted = st.form_submit_button("Submit", disabled = disabled)

# --- Handle submissions -----------------------------------------------------
if submitted:
    # Validate all required fields have been populated, otherwise raise an error

    if not full_name or not dob or not email or not phone or not suburb or not id_type or not id_number or not id_expiry_date or not service or not price or not q_eat or not q_alcohol or not q_med or not q_bleed or not q_faint or not q_breastfeed or not q_bloodpressure or not q_latex or not q_allergy:
        st.error("Please answer all questions")
    else:
        # Prepare response record
        response = {
            "timestamp":       datetime.now().isoformat(),
            "full_name":       full_name,
            "dob":             dob.isoformat(),
            "age":             age,
            "email":           email,
            "phone":           phone,
            "suburb":          suburb,
            "id_type":         id_type,
            "id_expiry_date":  id_expiry_date.isoformat(),
            "id_number":       id_number,
            "service":         service,
            "price":           price,
            #"agree_marketing": agree_marketing,
            "date_of_consent": date_of_consent.isoformat(),
            "signature":       signature,
            "other_details":   q_other,
        }

        # Determine where to save
        csv_file = "consent_responses.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([response])], ignore_index=True)
        else:
            df = pd.DataFrame([response])

        # Write back to disk
        df.to_csv(csv_file, index=False)

        st.success("✅ Thank you! Your response has been recorded.")
        
        # (Optional) show submissions
        if st.checkbox("Show all responses"):
            st.dataframe(df)


# --- Footer ------------------------------------------------------------------
st.markdown("---")
#st.caption("Built with ❤️ using Streamlit")
